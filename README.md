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

##USAGE:
```
psort.py -o null --analysis rpmdb --rpmdb-dir /home/damien/test/rpm output.plaso

****************************** Analysis report: 0 ******************************
String : Report generated from: rpmdb Generated on: 2017-07-12T06:59:23+00:00
         Report text: RPMDB plugin determined 82 sha256 hashes differ from the
         rpm database. filename:/usr/lib64/libnssckbi.so
         event_sha256_sum:9c751f528fc92377f5637e89077ec3b2623cbde68f96e55662ec02a5e2d34fcf
         rpmdb_sha256_sum:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
....(snip)....
filename:/etc/adjtime
         event_sha256_sum:9efeb3ab5a61932caf3d2032f0250576b38db181bebba53a23b8836ec45281b2
         rpmdb_sha256_sum:6aa92cacc25f30a7caacd8cf772d3626f5bd5b3a75ab2dc3e74a5119f56d12df
--------------------------------------------------------------------------------
```

##TODO:

exclude hashes of configuration files marked set to change in the rpm database.

enable filtering of l2tcsv output from the original rpm database to remove files where the hashes match.

