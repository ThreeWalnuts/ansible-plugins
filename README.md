# ansible-plugins
ansible_logger_plugin.py is used for recording log data from ansible execution.
The log data files are kept under /var/log/ansible/hosts/ folder.
In each file, the data format is:
\<time\> - \<node IP\> - \<ansible_task_name\> - \<task OK/Failed status\> - \<task duration\> - \<module data\>

Before using this plugin, please configure it into /etc/ansible.cfg like this:
1. Uncomment "callback_plugins   = /usr/share/ansible_plugins/callback_plugins"
2. Put this ansible_logger_plugin.py under "/usr/share/ansible_plugins/callback_plugins"

After running ansible, you would find log files under /var/log/ansible/hosts/, the number of files depends on how many nodes
your ansible would deploy to.

If you want to collect above ansible data into logstash, please configure your logstash.conf by using the content from the file logstash_ansible.conf. The version of your logstash should be 2.0.0. Meanwhile, please put the pattern file ansible_log_pattern under your logstash pattern folder. "pattern" folder and your logstash.conf must be in the same parent folder, otherwise, your logstash wouldn't find proper defined patterns. After that, restart your logstash server.

Please make sure you have already installed the elasticsearch 2.0.0, as you run the ansible, the logstash will grap the data from the ansible log file above and send them to elasticsearch accordingly.

If you want to present the ansible log data to Kibana 4.2.1, please import ansible_statistic_dashboard.json file to your Kibana 4.2.1 from your web browser.

