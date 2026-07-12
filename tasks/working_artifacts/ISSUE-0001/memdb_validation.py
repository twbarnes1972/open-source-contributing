"""Track B validation: interleaved-session shapes from repro_staticpool.py on
memdb URLs (separate real connections, one shared in-memory DB).

Success criterion is NOT "no interference" — memdb serializes (a pending write
blocks readers, no WAL). Success = NO SILENT LOSS: committed work survives, and
any interference surfaces as a loud OperationalError instead of vanished rows.
"""
import asyncio
import sys

from sqlalchemy import Column, Integer, Text, create_engine, select, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Row(Base):
    __tablename__ = "rows"
    id = Column(Integer, primary_key=True)
    v = Column(Text)


def variant_a_original_repro_shape():
    """Exact repro ordering. On StaticPool: s2's rollback silently destroys
    s1's flushed INSERT. On memdb: s2 can't touch s1's transaction — its read
    either fails loudly (locked) or succeeds; s1's commit always lands."""
    eng = create_engine(
        "sqlite:///file:/memdb_a?vfs=memdb&uri=true",
        connect_args={"timeout": 0.3},
    )
    Base.metadata.create_all(eng)

    s1 = Session(eng)
    s1.add(Row(v="s1-row"))
    s1.flush()                    # INSERT pending on s1's OWN connection

    s2 = Session(eng)             # QueuePool -> different connection
    interference = "none"
    try:
        s2.execute(select(Row))   # writer pending -> expect loud lock error
    except OperationalError as e:
        interference = f"loud ({str(e.orig).strip()})"
    s2.rollback()                 # rolls back only s2's connection

    s1.commit()                   # s1's work survives regardless
    s1.close(); s2.close()

    with Session(eng) as s3:
        n = len(s3.execute(select(Row)).scalars().all())
    eng.dispose()
    ok = n == 1
    print(f"A repro shape on memdb: committed rows = {n} (expected 1); "
          f"reader interference: {interference} -> "
          f"{'OK - no silent loss' if ok else '*** LOSS ***'}")
    return ok


async def variant_b_async_concurrent():
    """Concurrent asyncio writer+reader (one session per task, recommended
    pattern). Reader retries on lock; writer's commit must survive."""
    eng = create_async_engine(
        "sqlite+aiosqlite:///file:/memdb_b?vfs=memdb&uri=true",
        connect_args={"timeout": 0.3},
    )
    async with eng.begin() as c:
        await c.run_sync(Base.metadata.create_all)
    sf = async_sessionmaker(eng, class_=AsyncSession)
    lock_hits = 0

    async def writer():
        async with sf() as s:
            s.add(Row(v="w"))
            await s.flush()
            await asyncio.sleep(0.05)   # hold the write tx open briefly
            await s.commit()

    async def reader():
        nonlocal lock_hits
        for _ in range(20):
            try:
                async with sf() as s:
                    (await s.execute(select(Row))).scalars().all()
                return
            except OperationalError:
                lock_hits += 1
                await asyncio.sleep(0.05)

    await asyncio.gather(writer(), reader())
    async with sf() as s:
        n = len((await s.execute(select(Row))).scalars().all())
    await eng.dispose()
    ok = n == 1
    print(f"B async concurrent on memdb: committed rows = {n} (expected 1), "
          f"reader lock retries = {lock_hits} -> "
          f"{'OK - no silent loss' if ok else '*** LOSS ***'}")
    return ok


def variant_c_write_conflict():
    """Two concurrent writers: second must fail LOUDLY, not silently win/lose."""
    eng = create_engine(
        "sqlite:///file:/memdb_c?vfs=memdb&uri=true",
        connect_args={"timeout": 0.3},
    )
    Base.metadata.create_all(eng)
    c1 = eng.connect()
    c1.execute(text("insert into rows (v) values ('c1')"))  # write tx open
    c2 = eng.connect()
    try:
        c2.execute(text("insert into rows (v) values ('c2')"))
        ok, outcome = False, "*** second concurrent write silently allowed ***"
    except OperationalError as e:
        ok, outcome = True, f"OK - loud error: {str(e.orig).strip()}"
    c1.rollback(); c1.close(); c2.close(); eng.dispose()
    print(f"C concurrent writers on memdb: {outcome}")
    return ok


if __name__ == "__main__":
    a = variant_a_original_repro_shape()
    b = asyncio.run(variant_b_async_concurrent())
    c = variant_c_write_conflict()
    sys.exit(0 if (a and b and c) else 1)
