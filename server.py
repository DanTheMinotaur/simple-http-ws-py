import asyncio
import os
import aiohttp.web
import datetime
import random

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))
index = None
with open('index.html', 'r') as f:
    index = f.read()

async def testhandle(request):
    return aiohttp.web.Response(text=index, content_type='text/html')

async def websocket_time_handle(request):
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print(f"Send ws message: '{now}'")
        await ws.send_str(now)
        await asyncio.sleep(random.random() * 3)

def main():
    app = aiohttp.web.Application()
    app.router.add_route('GET', '/', testhandle)
    app.router.add_route('GET', '/ws', websocket_time_handle)
    aiohttp.web.run_app(app, host=HOST, port=PORT)


if __name__ == '__main__':
    main()
