import asyncio
from linda import server

if __name__ == '__main__':
    try:
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print('\nShutting down server...')
        exit(0)
