import pkg_resources
pkg_resources.declare_namespace(__name__)

import logging
_loggerDict = logging.root.manager.loggerDict

#if logger is not configured
if _loggerDict is None or not _loggerDict: #is None or {}
    raise ValueError('Please configure logger first. '+\
                     'This library is useless without proper logger configuration.\n'+\
                     'See https://docs.python.org/3/howto/logging.html#configuring-logging '+\
                     'for details')

