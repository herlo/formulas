from fedulas.configmanager import ConfigManager

class Ansible(ConfigManager):
    """
    First ConfigManager proxy class. Applies ansbile playbooks
    as formulas to a local machine.
    """
    def __init__(self, cfgs, logger):
        self.name = 'Ansible'
        self.cfgs = cfgs
        self.logger = logger
