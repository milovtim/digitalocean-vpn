from vpn import actions

if __name__ == '__main__':
    d = actions.create_vpn_droplet()
    actions.wait_droplet_state(d.id, 'create', 'completed')
    ip_addr = d.load().ip_address
    with open('vpn_ip.txt', 'w') as ip_file:
        ip_file.write(ip_addr)
    print("Check ip: %s" % ip_addr)
