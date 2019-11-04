from vpn import actions
from sys import argv

if __name__ == '__main__':
    if len(argv) >= 2:
        actions.get_first_droplet_by_tag(argv[1])
