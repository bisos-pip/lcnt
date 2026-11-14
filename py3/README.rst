=============================================================================================================================================================================
bisos.lcnt: Command Services (CS) and libraries to support ByStar Libre Content (LCNT) capabilities for impressive (pdf presentations), screenstudio (desktop recorder), etc.
=============================================================================================================================================================================


.. contents::
   :depth: 3
..

Overview
========

bisos.lcnt: Command Services (CS) and libraries to support ByStar Libre
Content (LCNT) capabilities for impressive (pdf presentations),
screenstudio (desktop recorder), etc.

Package Documentation At Github
===============================

The information below is a subset of the full of documentation for this
bisos-pip package. More complete documentation is available at:
https://github.com/bisos-pip/lcnt-cs

Realted Resources
=================

+--------------------------+------------------------------------------+
| bisos Capabilities Panel | file:/panels/capab                       |
|                          | ilities/_nodeBase_/fullUsagePanel-en.org |
+--------------------------+------------------------------------------+
|                          |                                          |
+--------------------------+------------------------------------------+

.. _table-of-contents:

Table of Contents TOC
=====================

-  `Overview <#overview>`__
-  `Package Documentation At
   Github <#package-documentation-at-github>`__
-  `Realted Resources <#realted-resources>`__
-  `Installation <#installation>`__

   -  `Installation With pip <#installation-with-pip>`__
   -  `Installation With pipx <#installation-with-pipx>`__

-  `Capability Bundles (CBM): lcntCore, lcntBases,
   lcntMultiMedia <#capability-bundles-cbm-lcntcore-lcntbases-lcntmultimedia>`__

   -  `lcntBases <#lcntbases>`__
   -  `lcntMultiMedia <#lcntmultimedia>`__

-  `Part of BISOS and ByStar — ByStar Internet Services Operating
   System <#part-of-bisos-and-bystar-----bystar-internet-services-operating-system>`__
-  `bisos.lcnt as a Standalone Piece of
   BISOS <#bisoslcnt-as-a-standalone-piece-of-bisos>`__
-  `Documentation and Blee-Panels <#documentation-and-blee-panels>`__

   -  `bisos.lcnt Blee-Panels <#bisoslcnt-blee-panels>`__

-  `Support <#support>`__

Installation
============

The sources for the bisos.lcnt pip package is maintained at:
https://github.com/bisos-pip/lcnt.

The bisos.lcnt pip package is available at PYPI as
https://pypi.org/project/bisos.lcnt

You can install bisos.lcnt with pip or pipx.

Installation With pip
---------------------

If you need access to bisos.lcnt as a python module, you can install it
with pip:

.. code:: bash

   pip install bisos.lcnt

Installation With pipx
----------------------

If you only need access to bisos.lcnt as a command on command-line, you
can install it with pipx:

.. code:: bash

   pipx install bisos.lcnt

The following commands are made available:
/usr/local/bin/beamerExternalExtensions.py
/usr/local/bin/screenstudioWebClientIcm.py

Capability Bundles (CBM): lcntCore, lcntBases, lcntMultiMedia
=============================================================

bisos.lcnt supplies the CBSs (capability bundle specifications), sboms
and assemble steps behind three CBM leaves of capabilityType ``induct``,
realm ``collective``, at ``sys/cbm/collective/induct/<name>/``. Each
leaf is a ``cbmProc.spcs`` that only points at the CBS (see
bisos.capability); it is gated by ``cbmProc.control`` (``available``,
``enabled``, ``disabled``). Materialize them in this order:

+----------------+----------------------------------------------------+
| Capability     | What it provides                                   |
+================+====================================================+
| lcntCore       | texlive-full, hevea, evince, the Persian fonts     |
|                | (nested fonts sbom)                                |
+----------------+----------------------------------------------------+
| lcntBases      | ``/de/sys/lcnt`` and ``/lcnt``, linked into the    |
|                | bases BXO (rawBisos only)                          |
+----------------+----------------------------------------------------+
| lcntMultiMedia | reveal.js, display tools; audio on a VM, video     |
|                | recording on a Box                                 |
+----------------+----------------------------------------------------+

Each has ``<name>-sbom.pcs``, ``<name>-assemble.cs`` and
``<name>-cbs.pcs`` in ``py3/bin/``, and a pointer
``cbmProc-<name>.spcs`` to copy to its leaf. Materialize and verify:

.. code:: bash

   cd /bisos/platform/sys/cbm/collective/induct/lcntCore
   ./cbmProc.spcs -i cbm_enable
   ./cbmProc.spcs -i cbm_materialize
   lcntCore-assemble.cs -i toolchainCheck       # the verdict: it fails loudly

The legacy scripts and the CBM walker exit 0 even when a step failed, so
only ``toolchainCheck`` (in each ``<name>-assemble.cs``) tells whether a
capability is complete.

lcntBases
---------

The bases BXO on rawBisos is the clone ``bxlcnt/bro_lcntBases-rawBisos``
(override for tests: ``LCNT_BASES_BXO``). The assemble step makes
``/de/sys`` and ``/lcnt`` with sudo, and links ``bxdpt``, ``BIB``,
``CENTRAL``, ``REGISTRY`` and ``lgpc`` (to ``lcnt/lgpc``) inside
``/de/sys/lcnt``; it never links inside the clone.
``lcntBases-assemble.cs -i fullUpdate`` repairs a broken link and
refuses to replace a real directory. On the sited BISOS the bases come
from a BPO instead and this leaf stays ``available``.

lcntMultiMedia
--------------

The environment decides what is installed: Container (PDF and the reveal
HTML; display-only tools), VM (adds audio), Box (adds video recording
and editing). It is detected with ``systemd-detect-virt``; override it
with ``LCNT_MM_ENV=Container|VM|Box``.
``lcntMultiMedia-assemble.cs -i environment`` reports it and
``-i toolchainCheck`` verifies it (and that lcntCore is complete, which
it never installs). The OBS profile and websocket, aeneas, whisper and
subed are not done.

Part of BISOS and ByStar — ByStar Internet Services Operating System
====================================================================

| Layered on top of Debian, **BISOS**: (By\* Internet Services Operating
  System) is a unified and universal framework for developing both
  internet services and software-service continuums that use internet
  services. See `Bootstrapping ByStar, BISOS and
  Blee <https://github.com/bxGenesis/start>`__ for information about
  getting started with BISOS.
| **BISOS** is a foundation for **The Libre-Halaal ByStar Digital
  Ecosystem** which is described as a cure for losses of autonomy and
  privacy in a book titled: `Nature of
  Polyexistentials <https://github.com/bxplpc/120033>`__

*bisos.lcnt* is part of BISOS.

bisos.lcnt as a Standalone Piece of BISOS
=========================================

bisos.lcnt is a standalone piece of BISOS. It can be used as a
self-contained Python package separate from BISOS. Follow the
installation and usage instructions below for your own use.

Documentation and Blee-Panels
=============================

bisos.lcnt is part of ByStar Digital Ecosystem http://www.by-star.net.

This module's primary documentation is in the form of Blee-Panels.
Additional information is also available in:
http://www.by-star.net/PLPC/180047

bisos.lcnt Blee-Panels
----------------------

bisos.lcnt Blee-Panels are in ./panels directory. From within Blee and
BISOS these panels are accessible under the Blee "Panels" menu.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact
