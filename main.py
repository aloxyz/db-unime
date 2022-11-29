from src.startup import init_parser, get_args
import src.datasetgen as generator

import src.mongo.mongo_manager as mongomg
import src.neo.neo_manager as neomg

DEFAULT_SETSIZE = 100000

def boot():
    init_parser()
    args = get_args()

    assert args.load, 'per favore, indica il carico del dataset.'

    load = int(args.load[0])
    refresh = (args.g or args.r) is not False

    print(args.g, args.r)

    if args.g is True:
        generator.generate(load)
        pass

    exec(args.ignore or [], load, refresh)

def exec(ignore: tuple, load: int, refresh: bool):
    print(refresh)

    if 'mongo' not in ignore:
        mongomg.exec(load, refresh)

    if 'neo' not in ignore:
        neomg.exec(load, refresh)

if __name__ == '__main__':
    boot()
