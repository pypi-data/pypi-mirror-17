Merge parties
=============

.. image:: https://travis-ci.org/fulfilio/trytond-party-merge.svg?branch=develop
  :target: https://travis-ci.org/fulfilio/trytond-party-merge
  :alt: Build Status
.. image:: https://pypip.in/download/fio_party_merge/badge.svg
  :target: https://pypi.python.org/pypi/fio_party_merge/
  :alt: Downloads
.. image:: https://pypip.in/version/fio_party_merge/badge.svg
  :target: https://pypi.python.org/pypi/fio_party_merge/
  :alt: Latest Version
.. image:: https://pypip.in/status/fio_party_merge/badge.svg
  :target: https://pypi.python.org/pypi/fio_party_merge/
  :alt: Development Status

Any tool is dangerous in the hands of a fool. - Will Spencer
============================================================

The feature introduced by this module is quite handy, but at
the same time enough to literally screw yourself over. The
source parties are completely **dropped** from the database and
all records that refer to the party are moved to new party.

Some important consequences:

* All past invoices will now show up in the target party's history
* Payment profiles (credit cards, ACH etc) are merged.
* All nereid users (if you use nereid) will be merged. Yeh,
  shared wishlists, shared credit cards,  shared cart and shared
  order history. Not the best result if you merge two parties
  who are completely different.

So I hope, it should now be quite obvious to you now that using
this module requires great responsibility and should be limited
to power users who know what they are doing.

Professional Support
====================

This module is professionally supported by `Fulfil.IO <http://www.fulfil.io>`_.
If you are looking for on-site teaching or consulting support, contact our
`sales <mailto:sales@fulfil.io>`_ and `support
<mailto:support@fulfil.io>`_ teams.
