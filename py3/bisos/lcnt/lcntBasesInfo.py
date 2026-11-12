# -*- coding: utf-8 -*-
""" #+begin_org
* ~[Summary]~ :: The single source of facts of the lcntBases capability: where the bases BXO is, and what
is linked from /de/sys/lcnt into it. Pure: no side effects at import.
#+end_org """

import os
import typing

#
# Decided with the user, 2026-11-12 (lcnt AI-WorkPlan.org, Stage 3):
#   - rawBisos: the bases BXO is the clone bxlcnt/bro_lcntBases-rawBisos. (bpoActivate.sh and the usgBpos
#     model are for the sited BISOS only; the leaf stays "available" there.)
#   - /de/sys/lcnt is a real directory; /lcnt is a link to it; inside it are links into the BXO.
#   - var and outputs are not created. Nothing is ever linked inside the clone.
#

bxoOverrideName = "LCNT_BASES_BXO"
defaultBxo = "/bisos/git/bxRepos/bxlcnt/bro_lcntBases-rawBisos"

deSys = "/de/sys"
deSysLcnt = "/de/sys/lcnt"
lcntShortcut = "/lcnt"

# (name in /de/sys/lcnt, path in the BXO)
links: typing.List[typing.Tuple[str, str]] = [
    ("bxdpt", "bxdpt"),
    ("BIB", "BIB"),
    ("CENTRAL", "CENTRAL"),
    ("REGISTRY", "REGISTRY"),
    ("lgpc", "lcnt/lgpc"),
]

# Linked when the BXO has it, reported as absent (never required) when it does not.
optionalLinks: typing.List[typing.Tuple[str, str]] = [
    ("lgcc", "lcnt/lgcc"),
]


def bxoPath() -> str:
    """The override (LCNT_BASES_BXO, for tests) if set, else the rawBisos clone."""
    return os.environ.get(bxoOverrideName) or defaultBxo


def linkSpecs(bxo: str = "") -> typing.List[typing.Tuple[str, str, str]]:
    """(name, link path in /de/sys/lcnt, target in the BXO) of the required links."""
    bxo = bxo or bxoPath()
    return [(name, os.path.join(deSysLcnt, name), os.path.join(bxo, rel)) for name, rel in links]


def optionalLinkSpecs(bxo: str = "") -> typing.List[typing.Tuple[str, str, str]]:
    bxo = bxo or bxoPath()
    return [(name, os.path.join(deSysLcnt, name), os.path.join(bxo, rel)) for name, rel in optionalLinks]


def linkState(linkPath: str, target: str) -> str:
    """One of: ok (a link to the target, which exists), dangling, wrong (a link to elsewhere),
    notALink (something real is there), absent."""
    if not os.path.lexists(linkPath):
        return "absent"
    if not os.path.islink(linkPath):
        return "notALink"
    if os.readlink(linkPath) != target:
        return "wrong"
    return "ok" if os.path.isdir(linkPath) else "dangling"
