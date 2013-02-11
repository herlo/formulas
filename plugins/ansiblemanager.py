import os
import tempfile

from ansible import playbook, callbacks, utils

from fedulas.configmanager import ConfigManager


class AnsibleManager(ConfigManager):
    """
    First ConfigManager proxy class. Applies ansbile playbooks
    as formulas to a local machine.
    """
    def __init__(self, cfgs, logger):
        self.name = 'Ansible'
        self.cfgs = cfgs
        self.logger = logger

    def _make_hosts_file(self, tmp_file, hosts=['localhost']):

        for host in hosts:
            tmp_file.write(host)
            tmp_file.flush()

        return tmp_file.name

    def apply(self, name, path=None, hosts=['localhost']):
        """Apply an ansible playbook"""
        pass

        tmp_file = tempfile.NamedTemporaryFile(suffix=".tmp")
        hosts_file = self._make_hosts_file(tmp_file, hosts)
        transport = self.cfgs['formulas']['transport']

        if not path:
            path = os.path.expanduser(self.cfgs['formulas']['base_path'])
        else:
            path = os.path.expanduser(path)

        if not os.path.exists(path):
            os.makedirs(path, 0750)

        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        stats = callbacks.AggregateStats()
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)


        pb = playbook.PlayBook(playbook='{0}/{1}.yml'.format(path, name),
                                    host_list=hosts_file, transport=transport,
                                    callbacks=playbook_cb, runner_callbacks=runner_cb,
                                    stats=stats)

        pb.run()

        tmp_file.close()

