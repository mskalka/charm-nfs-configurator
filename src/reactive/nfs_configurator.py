from charms.reactive import when
from charmhelpers.core.hookenv import config
from jinja2 import Template


@when('config.changed')
def config_changed():
    ctxt = {}
    ctxt['nfs_options'] = config('nfs-common-options')
    with open('templates/nfs-common', 'r') as t:
        nfs_template = Template(t.read())
    with open('/etc/default/nfs-common', 'w') as f:
        f.write(nfs_template.render(ctxt))
