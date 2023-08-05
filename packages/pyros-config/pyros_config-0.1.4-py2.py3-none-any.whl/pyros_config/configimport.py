# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import importlib
import logging
import os
import types
import sys

import errno
import six

from .confighandler import ConfigHandler


# class to allow (potentially infinite) delayed conditional import.
# this way it can work with or without preset environment
class ConfigImport(types.ModuleType):

    def __init__(self, import_name, import_desc, relay_import_dict, fix_imports,
                 instance_path=None, instance_relative_config=True, root_path=None, default_config=None):
        super(ConfigImport, self).__init__(import_name, import_desc)

        # we delegate config related behavior (including defaults)
        self.config_handler = ConfigHandler(
            import_name,
            instance_path=instance_path,
            instance_relative_config=instance_relative_config,
            root_path=root_path,
            default_config=default_config,
        )

        #: relay_import_dict is a dictionary of the following form:
        #: {
        #:  'symbol_name_1': 'absolute.module.name',
        #:  'symbol_name_2': ('absolute.module.name', 'unused'),
        #:  'symbol_name_3': ('.relative.module.name', 'package_anchor'),
        #: }
        #: Its content will be passed to importlib.import_module() to attempt importing the module
        self.relay_import_dict = relay_import_dict

        assert callable(fix_imports)
        #: _fix_imports should be set to a callable.
        #: it will be used to attempt fixing the environment if needed before retrying importing...
        self._fix_imports = fix_imports

    @property
    def name(self):
        return self.config_handler.name

    @property
    def import_name(self):
        return self.config_handler.import_name

    @property
    def config(self):
        return self.config_handler.config

    @property
    def instance_path(self):
        return self.config_handler.instance_path

    @property
    def instance_relative_config(self):
        return self.config_handler.instance_relative_config

    @property
    def root_path(self):
        return self.config_handler.root_path

    def configure(self, config=None, create_if_missing=None):
        # We default to using a config file named after the import_name:
        config = config or self.name + '.cfg'
        try:
            logging.info("Loading configuration from {0}".format(config))
            self.config_handler.configure(config)
        except IOError as e:
            if e.errno not in (errno.EISDIR, ):
                cfg_filename = os.path.join(self.config_handler.config.root_path, config)

                if create_if_missing:
                    if not os.path.exists(os.path.dirname(cfg_filename)):
                        try:
                            os.makedirs(os.path.dirname(cfg_filename))
                        except OSError as exc:  # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise

                    with open(cfg_filename, 'w+') as cfg_file:
                        cfg_file.write(create_if_missing)
                    logging.warning("Default configuration has been generated in {cfg_filename}".format(**locals()))
        return self

    def activate(self):
        # TODO : put that in context to allow deactivation...

        symbols = {}

        # The actual trick
        try:
            # Try in case we don't need the fix
            for n, m in six.iteritems(self.relay_import_dict):
                if isinstance(m, tuple):
                    symbols[n] = importlib.import_module(m[0], m[1])
                else:
                    symbols[n] = importlib.import_module(m)
        except ImportError:
            # fix because it seems we need it
            self._fix_imports()
            # Try again and be explicit when it breaks
            for n, m in six.iteritems(self.relay_import_dict):
                try:
                    if isinstance(m, tuple):
                        symbols[n] = importlib.import_module(m[0], m[1])
                    else:
                        symbols[n] = importlib.import_module(m)
                except ImportError as ie:
                    logging.error("importlib.import_module{m} FAILED : {msg}".format(
                        m=m if isinstance(m, tuple) else "(" + m + ")",  # just to get the correct code in log output
                        msg=str(ie))
                    )
                    mod = str(ie).split()[-1]
                    logging.error("Make sure you have installed the {mod} python package".format(mod=mod))
                    logging.error("sys.path: {0}".format(sys.path))
                    raise

        for n in symbols.keys():
            # establishing internal relays:
            setattr(self, n, symbols[n])

        # Main relay
        # CAREFUL this doesn't work sometimes (had problem when using from celery bootstep...)
        sys.modules[self.import_name] = self
        return self
