
class ConfigManager:
    """
    Proxy class to allow implementations of . Applies ansbile playbooks
    as formulas to a local machine.
    """

    def __init__(self, cm_class, cfgs, logger):
        self.name = 'ConfigManager'
        self.cm = cm_class(cfgs, logger)

    def apply(self, name, path, hosts):
        return self.cm.apply(name, path, hosts)
