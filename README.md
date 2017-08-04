# monitoring-plugins-crm
Python Nagios-compatible cluster check.

## Description

This nagios-compatible check aims to replace `crm_mon -s` and `check_cluster` provided in `monitoring-plugins-cluster`. It gives a better monitoring than the existing ones.

This script checks the state of resources and nodes. An alert is emitted if
some nodes are offline or if some resources are in the 'failed' state.

## Usage
This plugin can be run using an unprivileged user but requires a sudo configuration, such as:

```
User_Alias NAGIOS = nagios
Cmd_Alias NAGIOS_CMD = /usr/sbin/crm_mon --as-xml
NAGIOS ALL = (root) NOPASSWD: NOEXEC: NAGIOS_CMD
```

Checks the state of nodes: ```/usr/lib/nagios/plugins/check_cluster --nodes=yes --resources=no --perfdata=yes```

Checks the state of ressources: ```/usr/lib/nagios/plugins/check_cluster --nodes=no --resources=yes --perfdata=yes```

Checks the state of both nodes and ressources: ```/usr/lib/nagios/plugins/check_cluster --nodes=yes --resources=yes --perfdata=yes```

The 'warning' and 'critical' thresholds deal with the number of failed resources.

Perfdata provide two metrics: 'offline_nodes' and 'failed_resources'.

## Help

```/usr/lib/nagios/plugins/check_cluster --help```
