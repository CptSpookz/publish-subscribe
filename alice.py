import asyncio
from linda.client import LindaClient

async def main():
    blog = LindaClient()
    await blog.connect()
    blog._out(("alice", "gtcn", "This graph theory stuff is not easy"))
    blog._out(("alice", "distsys", "I like systems more than graphs"))
    await blog.close()


if __name__ == '__main__':
    asyncio.run(main())
