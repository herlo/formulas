# Main class for formulas

import os
import re
import sys
import rpm
import time
import glob
import stat
import shutil
import hashlib
import logging
import tempfile
import argparse
import subprocess
import ConfigParser

from fedulas.configmanager import ConfigManager

class FormulasError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        repr(self.value)

class Formulas:
    """
    Support class for Formulas. Provides tooling for managing and applying
    Formulas.
    """

    def __init__(self):
        """Constructor for Formulas, will create self.cfgs and self.logger
        """
        # config_manager object handles calls for chosen
        # configuration management software

        self.cfgs = {}

        for path in ['/etc/formulas', '~/.formulas']:
            expanded_path = "%s/%s" % (os.path.expanduser(path), 'formulas.conf')
            print "expanded_path {0}".format(expanded_path)
            if os.path.exists(expanded_path):
                self._load_config(expanded_path)

        self.logger = logging.getLogger('formulas')
#        self.logger.setLevel(eval(self.cfgs['logger']['loglevel']))

        cmModuleName = self.cfgs['cm']['module']
        cmClassName = self.cfgs['cm']['class']

        #remoteModule = __import__(remoteModuleName,
        #                          globals(),
        #                          locals(),
        #                          [remoteClassName])
        #self.gitremote = GitRemote(remoteModule.__dict__[remoteClassName], self.cfgs, self.logger)

        try:
            cmModule = __import__('plugins.{0}'.format(cmModuleName),
                                      globals(),
                                      locals(),
                                      [cmClassName])
            self.config_module = ConfigManager(cmModule.__dict__[cmClassName], self.cfgs, self.logger)
        except ImportError, e:
            self.logger.debug("Class %s in module %s not found: %s" % (cmClassName, 'plugins.{0}'.format(cmModuleName), e))
            print "Class {0} in module {1} not found: {2}".format(cmClassName, 'plugins.{0}'.format(cmModuleName), e)
            raise FormulasError("Class %s in module %s not found: %s" % (cmClassName, 'plugins.{0}'.format(cmModuleName), e))

    def _load_config(self, path):
        """Will create self.cfgs

        :param str path: formulas.conf path
        """

        config = ConfigParser.SafeConfigParser()
        try:
            f = open(path)
            config.readfp(f)
            f.close()
        except ConfigParser.InterpolationSyntaxError as e:
            raise FormulasError("Unable to parse configuration file properly: %s" % e)

        for section in config.sections():
            if not self.cfgs.has_key(section):
                self.cfgs[section] = {}

            for k, v in config.items(section):
                self.cfgs[section][k] = v


    def apply_formula(self, name):
        """Apply the named Formula"""

        pass
