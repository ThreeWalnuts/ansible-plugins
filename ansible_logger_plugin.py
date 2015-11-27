import os
import time
import datetime
import json
    
FIELDS = ['cmd', 'command', 'start', 'end', 'delta', 'msg', 'stdout', 'stderr']

class CallbackModule(object):

    TIME_FORMAT="%b %d %Y %H:%M:%S"
    MSG_FORMAT="%(now)s - %(node_IP)s - %(task_name)s - %(category)s - %(task_duration)f - %(data)s\n"
    
    def __init__(self):
        # For storing timings
        self.stats = {}
        # For storing the name of the current task
        self.current = None


        if not os.path.exists("/var/log/ansible/hosts"):
            os.makedirs("/var/log/ansible/hosts")

    def log(self, host, category, data):
            if self.current is not None:
                duration = self.stats[self.current] = time.time() - self.stats[self.current]
                
            if '_ansible_verbose_override' in data:
                # avoid logging extraneous data
                data = 'omitted'
            else:
                data = data.copy()
                data = json.dumps(data)
                
                if str(data).find("verbose_override") != -1:
                    data="omitted as setup log"
                else:
                    print "----------------------------------------------------------------------------------"
                    print data
                    print "----------------------------------------------------------------------------------"
                    path = os.path.join("/var/log/ansible/hosts", host)
                    now = time.strftime(self.TIME_FORMAT, time.localtime())
                    msg = str(self.MSG_FORMAT % dict(now=now, node_IP = host, task_name = self.current, category=category, task_duration = duration, data=data))
                    with open(path, "ab") as fd:
                        fd.write(msg)

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        #human_log(res)
        self.log(host,"FAILED",res)
    def runner_on_ok(self, host, res):
        #human_log(res)
        self.log(host,"OK",res)
    def runner_on_error(self, host, msg):
        pass
    
    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        self.log(host,"UNREACHABLE",res)
    
    def runner_on_no_hosts(self):
        pass
    
    def runner_on_async_poll(self, host, res, jid, clock):
        pass

    def runner_on_async_ok(self, host, res, jid):
        pass

    def runner_on_async_failed(self, host, res, jid):
        pass
    
    def playbook_on_start(self):
        pass
    
    def playbook_on_notify(self, host, handler):
        pass
    
    def playbook_on_no_hosts_matched(self):
        pass
    
    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        """
        Logs the start of each task
        """
        self.current = name
        # Record the start time of the current task
        self.stats[self.current] = time.time()
        
    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass
    
    def playbook_on_setup(self):
        pass
    
    def playbook_on_import_for_host(self, host, imported_file):
        pass
    
    def playbook_on_not_import_for_host(self, host, missing_file):
        pass
    
    def playbook_on_play_start(self, pattern):
        pass

    def playbook_on_stats(self, stats):
            
        # Sort the tasks by their running time
        results = sorted(
            self.stats.items(),
            key=lambda value: value[1],
            reverse=True,
        )

        # Just keep the top 10
        #results = results[:10]

        # Print the timings
        print "---------------------------------------------------------------------"
        print results
        print "---------------------------------------------------------------------"

        d=dict()

        for name, elapsed in results:
            d[name]=elapsed
        print d


        j=json.dumps(d)
        print "---------------------------------------------------------------------"
        print j
        print "---------------------------------------------------------------------"




        for name, elapsed in results:
            print(
                "{0:-<70}{1:->9}".format(
                    '{0} '.format(name),
                    ' {0:.02f}s'.format(elapsed),
                )
            )

        total_seconds = sum([x[1] for x in self.stats.items()])
        print("\nPlaybook finished: {0}, {1} total tasks.  {2} elapsed. \n".format(
                time.asctime(),
                len(self.stats.items()),
                datetime.timedelta(seconds=(int(total_seconds)))
                )
          )