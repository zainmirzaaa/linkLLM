import asyncio
queue = asyncio.Queue()

async def worker():
    while True:
        doc = await queue.get()
        # TODO: real indexing
        print(f"[indexer] indexed len={len(doc)}")
        queue.task_done()
