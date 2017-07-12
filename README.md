# plaso-rpmdb-analysis
Plaso RPMDB Analysis Plugin for generating a report of hashes that differ between a plaso container and the rpmdb

This plaso analysis plugin compares event sha256 hashes with those from the exracted rpm database and reports those that differ.
Tested against build 1.5.1.


##INSTALLATION:
(Replace the path with the path to your plaso installation)

```
sudo install -m 0755 rpmdb_analysis.py /usr/local/lib/python2.7/dist-packages/plaso-1.5.1-py2.7.egg/plaso/cli/helpers/rpmdb_analysis.py
sudo sed -i "\$afrom plaso.cli.helpers import rpmdb_analysis" /usr/local/lib/python2.7/dist-packages/plaso-1.5.1-py2.7.egg/plaso/cli/helpers/__init__.py

sudo install -m 0755 rpmdb.py /usr/local/lib/python2.7/dist-packages/plaso-1.5.1-py2.7.egg/plaso/analysis/rpmdb.py
sudo sed -i "\$afrom plaso.analysis import rpmdb" /usr/local/lib/python2.7/dist-packages/plaso-1.5.1-py2.7.egg/plaso/analysis/__init__.py
```

##TODO:

exclude hashes of configuration files marked set to change in the rpm database.

enable filtering of l2tcsv output from the original rpm database to remove files where the hashes match.
