import asyncio
import threading
import time

from endstone.asyncio import run


def test_run_task():
    """Ensure run returns a Future whose result comes from a different thread."""
    timestamps = {}

    async def task():
        timestamps["start"] = time.time()
        await asyncio.sleep(0.5)
        timestamps["end"] = time.time()
        return threading.get_ident()

    # Record before scheduling
    before = time.time()
    fut = run(task())
    after = time.time()

    # Immediately after scheduling, nearly no time has passed
    assert (after - before) < 0.05, "run() should not block the caller"

    # Must be a concurrent.futures.Future
    assert hasattr(fut, "result"), "run() should return a Future-like object"

    # Main thread ID
    main_id = threading.get_ident()

    # Block for at most 1s waiting for the result
    result_thread_id = fut.result(timeout=1.0)

    # Check that the coroutine ran on a different thread
    assert result_thread_id != main_id

    # The timestamp inside the coroutine must be ≥ when we scheduled it,
    # and also significantly after `before` (due to the sleep delay)
    assert "start" in timestamps and "end" in timestamps
    assert timestamps["start"] >= before
    assert (timestamps["end"] - timestamps["start"]) >= 0.5


def test_run_concurrent_tasks():
    """
    Schedule two coroutines with different sleep times and ensure they
    can run concurrently (total time < sum of sleeps).
    """

    async def s(n):
        await asyncio.sleep(n)
        return n

    t0 = time.time()
    fut1 = run(s(0.5))
    fut2 = run(s(0.7))

    # Wait for them both
    r1 = fut1.result(timeout=1.0)
    r2 = fut2.result(timeout=1.0)
    t1 = time.time()

    # They should return the expected values
    assert {r1, r2} == {0.5, 0.7}

    elapsed = t1 - t0
    # If they ran in parallel, elapsed should be just over the max(0.5,0.7),
    # not their sum.
    assert 0.7 <= elapsed < (0.5 + 0.7), f"Tasks didn’t overlap; took {elapsed:.2f}s"
