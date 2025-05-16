import argparse
import asyncio
import os
import sys

from WebsocketServer import WebsocketServer
from game import GameMaster
from player import Player
from viewer.Viewer import Viewer


def main(client_port, viewer_port):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server = WebsocketServer(loop, port=client_port)
    view_server = WebsocketServer(loop, port=viewer_port)
    viewer = Viewer()

    loop.run_until_complete(server.start())
    loop.run_until_complete(view_server.start())

    try:
        viewer.wait_for_connection(view_server, loop)
        master = loop.run_until_complete(GameMaster.Master.create_game(server, viewer, loop))
        loop.run_until_complete(master.start_match())
    except SystemExit:
        print('game close')
    except Exception as e:
        print(e)

    finally:
        server.stop()
        loop.stop()


def set_debug():
    GameMaster.DEBUG = True
    Player.DEBUG = True


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    parser = argparse.ArgumentParser()
    parser.add_argument("--no-timeout", action="store_true")
    parser.add_argument("--wait", type=int, default=0)
    parser.add_argument("-v", action="store_true")
    args = parser.parse_args()

    GameMaster.GAME_WAIT = args.wait
    if args.no_timeout:
        GameMaster.TIMEOUT_SEC = None
        print("timeout disabled")

    if args.v:
        set_debug()
        print("DEBUG enabled")

    main(8088, 8089)
