pretix ticket data importer for c4sh
====================================

Usage
-----

* Use pretix' JSON export to export all your tickets
* Place ``pretix-import.py`` inside the ``c4sh/`` folder
* Execute ``python pretix-import.py path/to/exported-file.json``

Limitations
-----------

* Currently, the importer tells c4sh that all tickets have a tax rate 
  of 0. As you normally use your data from pretix for creating invoices
  and financial reports for your preorders, this should not matter.

License
-------

Copyright by Raphael Michel

Released under the terms of the Apache License (see LICENSE file)
