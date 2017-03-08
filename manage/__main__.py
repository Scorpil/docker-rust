import sys
from .create import create
from .build import build
from .readme import readme
from .push import push


def usage():
    print("Commands available: {}".format(', '.join(COMMANDS.keys())))

COMMANDS = {
    'create': create,
    'build': build,
    'push': push,
    'readme': readme,
    'help': usage,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        exit(0)

    COMMANDS.get(sys.argv[1], usage)()
