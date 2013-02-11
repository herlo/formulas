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

    def __init__(self, config_file=None):
        """Constructor for Formulas, will create self.cfgs and self.logger
        """
        self.cfgs = {}

        for path in config_file.split(':'):
            expanded_path = "{0}".format(os.path.expanduser(path))
#            print "expanded_path: {0}".format(expanded_path)
            if os.path.exists(expanded_path):
                self._load_config(expanded_path)

#        print "self.cfgs: {0}".format(self.cfgs)

        self.logger = logging.getLogger('formulas')
        self.logger.setLevel(eval(self.cfgs['logger']['loglevel']))

        # create file handler which logs even debug messages
        fh = logging.FileHandler(self.cfgs['logger']['file'])
        fh.setLevel(eval(self.cfgs['logger']['loglevel']))

        # create formatter and add it to the handlers
        formatter = logging.Formatter(self.cfgs['logger']['format'])
        fh.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)

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

    def load_plugin(self):

        print "self.cfgs: {0}".format(self.cfgs)
        # config_manager object handles calls for chosen
        # configuration management software
#        self.logger.setLevel(eval(self.cfgs['logger']['loglevel']))

        cmModuleName = self.cfgs['cm']['module']
        cmClassName = self.cfgs['cm']['class']

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


    def apply_formula(self, args):
        """Apply the named Formula"""

        pass

