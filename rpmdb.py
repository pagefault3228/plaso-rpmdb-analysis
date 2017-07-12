# -*- coding: utf-8 -*-
"""Analysis plugin to look up files in rpmdb and compare to events."""

import collections

from plaso.analysis import interface
from plaso.analysis import manager
from plaso.containers import reports
import rpm


class rpmEntry:
    def __init__(self, _package, _installationdate, _path, _sha256):

        self.package = _package
        self.installationdate = _installationdate
        self.path = _path.decode('utf-8')
        self.sha256 = _sha256
        self.event_sha256 = None



class RPMDBAnalysisPlugin(interface.AnalysisPlugin):
    """An analysis plugin for comparing original file hashes from the rpm database."""

    NAME = u'rpmdb'
    ENABLE_IN_EXTRACTION = False


    def __init__(self):
        """Initializes an rpmdb analysis plugin."""
        super(RPMDBAnalysisPlugin, self).__init__()
        self._number_of_event_tags = 0
        self._rpmdb_file_name = None
        self._rpmdb_dict = None


    def CompileReport(self, mediator):
        """Compiles an analysis report.
        Args:
          mediator (AnalysisMediator): mediates interactions between
              analysis plugins and other components, such as storage and dfvfs.
        Returns:
          AnalysisReport: analysis report.
        """
        different_hashes = 0
        different_list = []

        for rpm_entries in self._rpmdb_dict:
            rpmentrylist = self._rpmdb_dict[rpm_entries]
            for rpmitem in rpmentrylist:
                if rpmitem.sha256 != rpmitem.event_sha256:
                    different_hashes += 1
                    entry = u"filename:{0}\n\tevent_sha256_sum:{1}\n\trpmdb_sha256_sum:{2}".format(rpmitem.path, rpmitem.event_sha256, rpmitem.sha256)
                    different_list.append(entry)

        different_list.insert(0, u"RPMDB plugin determined {0} sha256 hashes differ from the rpm database.\n".format(different_hashes))
        report_text = u'\n'.join(different_list)

        analysis_report = reports.AnalysisReport(plugin_name=self.NAME, text=report_text)
        return analysis_report


    def ExamineEvent(self, mediator, event):
        try:
            rpmentries = self._rpmdb_dict[event.filename]
            upd_rpmentries = []
            for rpmentry in rpmentries:
                try:
                    rpmentry.event_sha256 = event.sha256_hash
                except:
                    pass
                finally:
                    upd_rpmentries.append(rpmentry)
            self._rpmdb_dict[event.filename] = upd_rpmentries
            self._number_of_event_tags += 1
        except:
            pass


    def generateinternaldatabase(self):

        rpmdb = collections.defaultdict(list)
        rpmdb_path = self._rpmdb_file_name

        try:
            rpm.addMacro("_dbpath", rpmdb_path)
            ts = rpm.TransactionSet()
            mi = ts.dbMatch()
        except Exception as e:
            print("Error opening rpmdb -> {0}".format(e))
            return

        for header in mi:

            _package = "{0}-{1}-{2}".format(header['name'], header['version'], header['release'])
            _installdate = header.sprintf("%{INSTALLTID:date}")

            for _fileinfo in header.fiFromHeader():
                _path = _fileinfo[0]
                _sha256 = _fileinfo[12]
                _rpmentry = rpmEntry(_package, _installdate, _path, _sha256)

                if _sha256 == "0000000000000000000000000000000000000000000000000000000000000000":
                    continue
                try:
                    rpmdb[_path].append(_rpmentry)
                except:
                    pass

        return rpmdb


    def SetAndLoadRPMDBPath(self, rpmdb):
        """Sets the directory path to the extracted RPM DB.
        Args:
            rpmdb (str): Directory Path/
        """
        self._rpmdb_file_name = rpmdb
        self._rpmdb_dict = self.generateinternaldatabase()


manager.AnalysisPluginManager.RegisterPlugin(RPMDBAnalysisPlugin)