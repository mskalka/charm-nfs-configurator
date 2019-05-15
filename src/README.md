# Charm Usage

Deploy the charm:

juju deploy nfs-configurator

Set the desired configuration options. Note the double quotes, this string
must be valid JSON:

juju config nfs-configurator nfs-common-options='NEED_GSSD=yes'

Relate the charm to the desired units:

juju add-relation my-service nfs-configurator
