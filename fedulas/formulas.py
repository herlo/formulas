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

# GitPython
import git
from git import InvalidGitRepositoryError, NoSuchPathError, GitCommandError

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
        pass


    def apply_formula(self, name):
        """Apply the named Formula"""

        pass
