import asyncio
import time

async def print_timeout(interval = 2, text = "Done"):
    await asyncio.sleep(interval)
    print(text)


async def main1():
    # await print_timeout()
    first_task = asyncio.create_task(print_timeout(text = "First task done"))
    print("First task created")
    second_task = asyncio.create_task(print_timeout(1, "Second task done"))
    print("Second task created")
    await first_task
    await second_task
    print("Tasks done")


async def get_delayed(timeout, text):
    await asyncio.sleep(timeout)
    return text


async def main2():
    print("Start", time.strftime("%X"))
    print(await get_delayed(1, "Hello 1"))
    print(await get_delayed(2, "Hello 2"))
    print("  End", time.strftime("%X"))


async def main3():
    print("Start", time.strftime("%X"))
    first = asyncio.create_task(get_delayed(2, "Hello 2"))
    second = asyncio.create_task(get_delayed(1, "Hello 1"))
    print(await second)
    print(await first)
    print("  End", time.strftime("%X"))


async def get_or_cancel(timeout, text):
    try:
        await asyncio.sleep(timeout)
        return text
    except asyncio.CancelledError:
        print("Task canceled")


async def main():
    print("Start", time.strftime("%X"))
    first = asyncio.create_task(get_or_cancel(2, "Hello 2"))
    second = asyncio.create_task(get_or_cancel(1, "Hello 1"))
    result = await second
    if result == "Hello 1":
        first.cancel()
    else:
        print(await first)        
    print("  End", time.strftime("%X"))

if __name__ == "__main__":
    asyncio.run(main())