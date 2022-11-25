from src.startup import init_parser, get_args

import src.mongo.mongo_manager as mongomg
import src.neo.neo_manager as neomg


def boot():
    init_parser()
    args = get_args()

    exec(args.ignore or [])

def exec(ignore: tuple):
    if 'mongo' not in ignore:
        print("EXEC MONGO")

    if 'neo' not in ignore:
        print("EXEC NEO")

if __name__ == '__main__':
    boot()
