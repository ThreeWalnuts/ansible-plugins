# ansible-plugins
ansible_logger_plugin.py is used for recording log data from ansible execution.
The log data files are kept under /var/log/ansible/hosts/ folder.
In each file, the data format is:
<time> - <node IP> - <ansible_task_name> - <task OK/Failed status> - <task duration> - <module data>

Before using this plugin, please configure it into /etc/ansible.cfg like this:
1. Uncomment "callback_plugins   = /usr/share/ansible_plugins/callback_plugins"
2. Put this ansible_logger_plugin.py under "/usr/share/ansible_plugins/callback_plugins"

After running ansible, you would find log files under /var/log/ansible/hosts/, the number of files depends on how many nodes
your ansible would deploy to.

