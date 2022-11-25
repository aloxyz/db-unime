from argparse import ArgumentParser

parser = ArgumentParser(
    prog="Progetto Database NoSQL",
    description="Progetto creato per Database NoSQL")

def init_parser():
    parser.add_argument('-clear', nargs="?", default=0, type=int, choices=[0, 1], help="Effettua il reset del database")
    parser.add_argument('-i', '--ignore', nargs="*", choices=["mongo", "neo"], help="ignora un database [NEO-MONGO]")

def get_args():
    return parser.parse_args()