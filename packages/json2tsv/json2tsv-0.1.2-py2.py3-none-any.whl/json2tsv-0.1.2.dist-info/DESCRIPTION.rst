json2tsv
========

Convert json to tab-separated format. Read from STDIN and write to
STDOUT. E.g.

::

    $ echo '[{"id":"123", "user":{"name":"mary", "gender":"female"}}, {"id":"124", "user":{"name":"mark", "gender":"male"}}]' | json2tsv id user.name user.gender
    123     mary    female
    124     mark    male

-  Free software: BSD license
-  Documentation: http://json2tsv.rtfd.org.





History
-------
0.1.2 (2016-09-28)
++++++++++++++++++

* Adds type decoding to tsv2json
* Light refactoring

0.1.1 (2016-07-11)
++++++++++++++++++

* Bugfixes; unicode support
* py2 / py3 support

0.1.0 (2014-01-11)
++++++++++++++++++

* First release on PyPI.


