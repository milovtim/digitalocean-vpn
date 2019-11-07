from digitalocean import Manager, Droplet
from json import load
from time import time_ns, sleep


def load_config():
    with open('conf.json') as f:
        return load(f)

def manager(config = None):
    conf_dict = config if config else load_config()
    token = conf_dict['token']
    return Manager(token=token)


def create_vpn_droplet():
    conf_dict = load_config()
    token = conf_dict['token']
    mngr = manager(conf_dict)
    ssh_key = mngr.get_ssh_key(conf_dict['sshKeyId'])

    droplet = Droplet(token=token,
                name=('vpn-%s' % time_ns()),
                region=conf_dict['region'],
                image='openvpn-18-04',
                size_slug='s-1vcpu-1gb',
                ssh_keys=[ssh_key],
                tags=['vpn'],
                backups=False)
    droplet.create()
    print("Droplet: %s(id:%s) created. Ip addr: %s" % (droplet.name, droplet.id, droplet.ip_address))
    return droplet


def get_first_droplet_by_tag(tag):
    token = load_config()['token']
    mngr = Manager(token=token)
    droplet = mngr.get_all_droplets(tag_name=tag)
    if droplet:
        droplet = droplet[0]
        print('droplet "%s"(%s): ip=%s' % (droplet.name, droplet.id, droplet.ip_address))
        return droplet
    return None


def wait_droplet_state(droplet_id, action_type, action_status, check_interval=5):
    man = manager()
    droplet = man.get_droplet(droplet_id)
    actions = droplet.get_actions()
    while actions:
        a = actions[-1]
        print("Action=`%s` in status=`%s` (%s with id=%s)" % (a.type, a.status, a.resource_type, a.resource_id))
        if a.type == action_type and a.status == action_status:
            break
        sleep(check_interval)
        actions = droplet.get_actions()


def destroy_droplet(droplet_id):
    m = manager()
    droplet_to_destroy = m.get_droplet(droplet_id)
    if droplet_to_destroy:
        droplet_to_destroy.destroy()
        print("Droplet %s(id:%s) destroyed" % (droplet_to_destroy.name, droplet_to_destroy.id))


if __name__ == '__main__':
    d = create_vpn_droplet()
    wait_droplet_state(d.id, 'create', 'completed')
