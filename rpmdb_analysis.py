# -*- coding: utf-8 -*-
"""The rpmdb analysis plugin CLI arguments helper."""

import os

from plaso.lib import errors
from plaso.cli.helpers import interface
from plaso.cli.helpers import manager
from plaso.analysis import rpmdb


class RPMDBAnalysisArgumentsHelper(interface.ArgumentsHelper):
    """RPMDB analysis plugin CLI arguments helper."""

    NAME = u'rpmdb'
    CATEGORY = u'analysis'
    DESCRIPTION = u'Argument helper for the RPMDB analysis plugin.'

    @classmethod
    def AddArguments(cls, argument_group):
        """Adds command line arguments the helper supports to an argument group.

        This function takes an argument parser or an argument group object and adds
        to it all the command line arguments this helper supports.

        Args:
            argument_group (argparse._ArgumentGroup|argparse.ArgumentParser):
                argparse group.
        """
        argument_group.add_argument(u'--rpmdb-dir', u'--rpmdb_dir', dest=u'rpmdb_dir', type=str, help=u'Specify a directory path to the rpm database.', action=u'store')


    @classmethod
    def ParseOptions(cls, options, analysis_plugin):
        """Parses and validates options.

        Args:
            options (argparse.Namespace): parser options.
            output_module (OutputModule): output module to configure.

        Raises:
            BadConfigObject: when the output module object is of the wrong type.
            BadConfigOption: when a configuration parameter fails validation.
        """
        if not isinstance(analysis_plugin, rpmdb.RPMDBAnalysisPlugin):
            raise errors.BadConfigObject(u'Analysis plugin is not an instance of RPMDBAnalysisPlugin')

        rpmdb_dir = cls._ParseStringOption(options, u'rpmdb_dir')
        if rpmdb_dir:
            try:
                if os.path.isdir(rpmdb_dir):
                    analysis_plugin.SetAndLoadRPMDBPath(rpmdb_dir)
                    return
            except Exception as e:
                raise errors.BadConfigOption(u"Error setting RPMDB Directory -> {0}".format(e))

        raise errors.BadConfigOption(u'RPMDB directory {0:s} does not exist.'.format(rpmdb_dir))

manager.ArgumentHelperManager.RegisterHelper(RPMDBAnalysisArgumentsHelper)
