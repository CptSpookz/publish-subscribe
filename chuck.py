import asyncio

from linda.client import LindaClient

async def main():
    blog = LindaClient()
    await blog.connect()
    r1 = await blog._rd(("bob","distsys",str))
    r2 = await blog._rd(("alice","gtcn",str))
    r3 = await blog._in(("bob","gtcn",str))
    await blog.close()
    print(r1)
    print(r2)
    print(r3)


if __name__ == '__main__':
    asyncio.run(main())
