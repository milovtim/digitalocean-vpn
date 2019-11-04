from vpn import actions

if __name__ == '__main__':
    d = actions.create_vpn_droplet()
    actions.wait_droplet_state(d.id, 'create', 'completed')
    print("Check ip: %s" % d.load().ip_address)
