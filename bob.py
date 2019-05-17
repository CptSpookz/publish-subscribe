import asyncio

from linda.client import LindaClient

async def main():
    blog = LindaClient()
    await blog.connect()
    blog._out(("bob", "distsys", "I am studying chap 2"))
    blog._out(("bob", "distsys", "The linda example's pretty simple"))
    blog._out(("bob", "gtcn", "Cool book!"))
    await blog.close()


if __name__ == '__main__':
   asyncio.run(main()) 
