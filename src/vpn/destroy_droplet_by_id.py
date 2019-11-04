from vpn import actions
from sys import argv

if __name__ == '__main__':
    if len(argv) >= 2 and str(argv[1]).isdigit():
        print("Destroying droplet id:%s" % argv[1])
        actions.destroy_droplet(argv[1])
