from argparse import ArgumentParser

parser = ArgumentParser(
    prog="Progetto Database NoSQL",
    description="Progetto creato per Database NoSQL")

def init_parser():
    parser.add_argument('-clear', nargs="?", default=0, type=int, choices=[0, 1], help="Effettua il reset del database")
    parser.add_argument('-i', '--ignore', nargs="*", choices=["mongo", "neo"], help="ignora un database [NEO-MONGO]")
    parser.add_argument('--g', action="store_true", help="genera il dataset")
    parser.add_argument('-l', '--load', nargs=1, type=int, choices=[25, 50, 75, 100], help="indica il carico del dataset")
    parser.add_argument('-r', action="store_true", help='resetta i database')

def get_args():
    return parser.parse_args()