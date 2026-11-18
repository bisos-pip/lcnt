# -*- coding: utf-8 -*-
""" #+begin_org
* ~[Summary]~ :: The single source of facts of the lcntMultiMedia capability: the environment (Container,
VM or Box) and what each environment gets. Pure: no side effects at import.
#+end_org """

import json
import os
import shutil
import subprocess
import typing

#
# Decided with the user, 2026-11-11 (lcnt AI-WorkPlan.org, Stage 4):
#   - Container: only PDF creation and the HTML for reveal; display-only programs are fine.
#   - VM: the Container set plus audio record, play and edit; no video recording.
#   - Box (rawMetal): everything, video recording included.
#   - Deferred, in every environment: aeneas, whisper, subed, wdiff, the pdfpc viewer.
#

environmentOverrideName = "LCNT_MM_ENV"

envContainer = "Container"
envVm = "VM"
envBox = "Box"
environments = (envContainer, envVm, envBox)


def environmentDetect() -> str:
    """The override (LCNT_MM_ENV=Container|VM|Box) if set, else systemd-detect-virt:
    any container is a Container (a container on a VM is still a Container), else a VM, else a Box."""
    override = os.environ.get(environmentOverrideName, "")
    if override:
        if override not in environments:
            raise ValueError(f"{environmentOverrideName} must be one of {environments}, not {override}")
        return override
    for flag, env in (("--container", envContainer), ("--vm", envVm)):
        try:
            result = subprocess.run(["systemd-detect-virt", flag, "--quiet"], check=False)
        except FileNotFoundError:
            continue
        if result.returncode == 0:
            return env
    return envBox


def environmentVirtName() -> str:
    """What systemd-detect-virt says (for the report): the container, the vm, or none."""
    names = []
    for flag in ("--container", "--vm"):
        try:
            names.append(subprocess.run(["systemd-detect-virt", flag], check=False,
                                        capture_output=True, text=True).stdout.strip() or "none")
        except FileNotFoundError:
            names.append("unknown")
    return "container=%s vm=%s" % tuple(names)


# (aptPackage, [programs that must be on PATH once it is installed])
aptContainer: typing.List[typing.Tuple[str, typing.List[str]]] = [
    ("mpv", ["mpv"]),                      # displays video
    ("gimp", ["gimp"]),                    # displays and edits images
    ("imagemagick", ["convert"]),
    ("pdftk-java", ["pdftk"]),             # pdftk is pdftk-java in Debian 13
]

aptVm: typing.List[typing.Tuple[str, typing.List[str]]] = [
    ("sox", ["sox"]),
    ("ffmpeg", ["ffmpeg"]),
    ("audacity", ["audacity"]),
    ("pavucontrol", ["pavucontrol"]),
    ("vlc", ["vlc"]),
    ("lame", ["lame"]),
    ("flac", ["flac"]),
    ("vorbis-tools", ["oggenc"]),
    ("mp3info", ["mp3info"]),
    ("gifsicle", ["gifsicle"]),
    ("scrot", ["scrot"]),
    ("impressive", ["impressive"]),        # plays a PDF presentation for the narrator: mmUnite play/record
]

aptBox: typing.List[typing.Tuple[str, typing.List[str]]] = [
    ("obs-studio", ["obs"]),
    ("kdenlive", ["kdenlive"]),
    ("v4l2loopback-dkms", []),             # a kernel module: boxModulesCheck, not a program
]


def aptFor(env: str) -> typing.List[typing.Tuple[str, typing.List[str]]]:
    """The apt packages of an environment (cumulative), with the programs each one provides."""
    if env == envContainer:
        return list(aptContainer)
    if env == envVm:
        return aptContainer + aptVm
    if env == envBox:
        return aptContainer + aptVm + aptBox
    raise ValueError(f"environment must be one of {environments}, not {env}")


def aptNamesFor(env: str) -> typing.List[str]:
    return [each[0] for each in aptFor(env)]


def programsFor(env: str) -> typing.List[str]:
    return [prog for each in aptFor(env) for prog in each[1]]


def programsSkippedFor(env: str) -> typing.List[str]:
    """Programs of the other environments: not required here, reported as skipped, never as missing."""
    return [prog for prog in programsFor(envBox) if prog not in programsFor(env)]


# reveal.js: every environment (a container builds the HTML for reveal). Installed by revealJs-sbom.pcs,
# which replaced /bisos/core/bsip/bin/lcaJsRevealBinsPrep.sh (2026-11-16, with the user). reveal.js is a
# library the HTML loads by path, not a command: it stays global under /usr/local (stable across Node
# versions, readable by nginx), installed by the system's npm under sudo, never by nvm's npm.
revealSbom = "revealJs-sbom.pcs"
revealNpm = "/usr/bin/npm"
revealPrefix = "/usr/local"
revealNodeModules = "/usr/local/lib/node_modules"
# (npm package, pinned version), in install order
revealNpmPkgs: typing.List[typing.Tuple[str, str]] = [
    ("reveal.js", "6.0.2"),
    ("reveal.js-plugins", "4.6.0"),
    ("reveal.js-menu", "2.1.0"),
]
# The HTML loads the menu as reveal.js-plugins/menu/: (the link, its relative target)
revealMenuLink = (os.path.join(revealNodeModules, "reveal.js-plugins", "menu"), "../reveal.js-menu")
revealCommands = ["node", "npm"]


def revealInstalledVersion(pkg: str) -> typing.Optional[str]:
    """The version in the global node_modules' package.json, or None when it is not installed."""
    try:
        with open(os.path.join(revealNodeModules, pkg, "package.json"), encoding="utf-8") as f:
            return json.load(f).get("version")
    except (OSError, ValueError):
        return None


def revealPresent() -> typing.List[typing.Tuple[str, str, typing.Optional[str]]]:
    """(npm package, pinned version, installed version or None) for each reveal npm package."""
    return [(pkg, ver, revealInstalledVersion(pkg)) for pkg, ver in revealNpmPkgs]


def revealMenuLinkOk() -> bool:
    link, target = revealMenuLink
    return os.path.islink(link) and os.readlink(link) == target and os.path.isdir(link)


def commandPresent(command: str) -> bool:
    return shutil.which(command) is not None
