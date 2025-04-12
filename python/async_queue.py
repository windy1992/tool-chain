import asyncio
from collections import deque
import time
import functools

def async_block_call(executor=None):
    """将阻塞函数包裹为异步调用"""
    def outer_wraps(block_call):
        @functools.wraps(block_call)
        async def wrapper(*args):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(executor, block_call, *args)

        return wrapper
    return outer_wraps

class SyncCoroCall(object):
    """实现异步调用的序列化，避免异步调用的竞争条件, 如异步文件写入"""

    def __init__(self):
        self._queue = deque()

    async def emit(self, coro):
        """将协程对象coro添加到队列中, 同步调度; 返回coro的执行结果"""
        ft = asyncio.Future()

        async def wrapper():
            try:
                result = await coro
                ft.set_result(result)
            except Exception as e:
                ft.set_exception(e)

        self._queue.append(wrapper)
        if len(self._queue) == 1:
            asyncio.create_task(self._run_next())

        return await ft
        

    async def _run_next(self):
        while self._queue:
            task = self._queue[0]
            # 注意 popleft 调用应在 await 之前，避免竞争
            self._queue.popleft()
            await task()
        


if __name__ == "__main__":
    async def test(i):
        await asyncio.sleep(i)
        print(f"test {i} done")
        return i
    
    @async_block_call(None)
    def block_sleep(s):
        time.sleep(s)
    
    async def main():
        c1 = time.time()
        t3 = asyncio.create_task(test(3))
        t2 = asyncio.create_task(test(2))
        t1 = asyncio.create_task(test(1))

        print(await t3)
        print(await t2)
        print(await t1)
        c2 = time.time()
        print(f"async test cost {c2-c1:.2f} sec")

        s = SyncCoroCall()
        t3 = asyncio.create_task(s.emit(test(3)))
        t2 = asyncio.create_task(s.emit(test(2)))
        t1 = asyncio.create_task(s.emit(test(1)))

        print(await t1)
        print(await t2)
        print(await t3)
        c3 = time.time()
        print(f"sync test cost {c3-c2:.2f} sec")


        s = asyncio.create_task(block_sleep(5))
        print("async sleep has committed")
        await s

    asyncio.run(main())
        
            

        



    