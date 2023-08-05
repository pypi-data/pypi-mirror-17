import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue

import pytest

from concurrently import concurrently, AsyncIOExecutorEngine


def process(data):
    time.sleep(data)
    return time.time()


paramz_executor = pytest.mark.parametrize(
    'executor', [None, ThreadPoolExecutor()],
    ids=lambda v: 'exec %s' % type(v).__name__
)


@pytest.mark.asyncio(forbid_global_loop=True)
@pytest.mark.parametrize(
    'conc_count', range(1, 5), ids=lambda v: 'counc %s' % v
)
@pytest.mark.parametrize(
    'data_count', range(1, 5), ids=lambda v: 'data %s' % v
)
@paramz_executor
async def test_concurrently(conc_count, data_count, executor, event_loop):
    data = range(data_count)
    q_data = Queue()
    for d in data:
        q_data.put(d)
    q_results = Queue()
    start_time = time.time()

    @concurrently(
        conc_count, engine=AsyncIOExecutorEngine, loop=event_loop,
        executor=executor
    )
    def _parallel():
        while not q_data.empty():
            d = q_data.get()
            res = process(d)
            q_results.put({d: res})

    await _parallel()

    results = {}
    while not q_results.empty():
        results.update(q_results.get())

    def calc_delta(n):
        if n // conc_count == 0:
            return n
        return n + calc_delta(n - conc_count)

    assert len(results) == data_count
    for n, v in results.items():
        delta = v - start_time
        assert int(delta) == calc_delta(n)


@pytest.mark.asyncio(forbid_global_loop=True)
@paramz_executor
async def test_stop(executor, event_loop):
    data = range(3)
    i_data = iter(data)
    results = {}
    start_time = time.time()

    @concurrently(
        2, engine=AsyncIOExecutorEngine, loop=event_loop, executor=executor
    )
    def _parallel():
        for d in i_data:
            r = process(d)
            results[d] = r

    await asyncio.sleep(0.5, loop=event_loop)
    await _parallel.stop()

    assert len(results) == 1
    assert int(results[0]) == int(start_time)


@pytest.mark.asyncio(forbid_global_loop=True)
@paramz_executor
async def test_exception(executor, event_loop):
    data = range(2)
    i_data = iter(data)
    results = {}
    start_time = time.time()

    @concurrently(
        2, engine=AsyncIOExecutorEngine, loop=event_loop, executor=executor
    )
    def _parallel():
        for d in i_data:
            if d == 1:
                raise RuntimeError()
            res = process(d)
            results[d] = res

    await _parallel()

    assert len(results) == 1
    assert int(results[0]) == int(start_time)

    exc_list = _parallel.exceptions()
    assert len(exc_list) == 1
    assert isinstance(exc_list[0], RuntimeError)


@pytest.mark.asyncio(forbid_global_loop=True)
async def test_processpool_isnot_supported(event_loop):

    with pytest.raises(AssertionError) as exc:
        @concurrently(
            engine=AsyncIOExecutorEngine, loop=event_loop,
            executor=ProcessPoolExecutor()
        )
        def _parallel():
            pass

    assert str(exc.value) == 'ProcessPoolExecutor is not supported'
