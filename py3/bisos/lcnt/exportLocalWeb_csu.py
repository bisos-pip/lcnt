# -*- coding: utf-8 -*-
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Export a released LCNT document to web sites on this system
** This File: /bisos/git/bxRepos/bisos-pip/lcnt/py3/bisos/lcnt/exportLocalWeb_csu.py
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """

####+BEGIN: b:py3:cs:file/dblockControls :classification "cs-u"
""" #+begin_org
* [[elisp:(org-cycle)][| /Control Parameters Of This File/ |]] :: dblk ctrls classifications=cs-u
#+BEGIN_SRC emacs-lisp
(setq-local b:dblockControls t) ; (setq-local b:dblockControls nil)
(put 'b:dblockControls 'py3:cs:Classification "cs-u") ; one of cs-mu, cs-u, cs-lib, bpf-lib, pyLibPure
#+END_SRC
#+RESULTS:
: cs-u
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
if 'csInfo' not in globals(): import typing ; csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['loadAs'], }
csInfo['version'] = '202611143855'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'exportLocalWeb_csu-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: The =localWeb= export method of lcntProc.sh
An LCNT export spec (=LCNT-INFO/Exports/<spec>/=) with =exportMethod= =localWeb= names its destinations in
the file-var =destinations=: FQDNs of web sites on this same system (whence "local"), whitespace separated. Each
FQDN is turned into the site's base directory by a resolver command run as a subprocess: the file-var
=siteResolver= of the spec (default =astroSite.cs -i siteBase=, which reads nginx), printing "<fqdn> <base>".
The export copies nothing. It writes a *pointer* to the document's release (=Release/<relTag>/=, always made
before an export) into the site's own repository: =<base>/lcntSpecs/<pubcategory>-<lcntNu>-<relTag>.pyl=, one
Python literal (formatted by black; read with ast.literal_eval), one file per release, replaced on re-export:
| =releaseDir=, =lcntInfo=      | the release and LCNT-INFO by their canonical paths (=/de/sys/lcnt/...=)    |
| =bxoKind=, =bxo=, =bxoPath=   | the BXO holding the release (=bro= <org>/<repo>, or =bpo= <id>), the path in it |
| =bxoCommit=                   | the last commit of the release directory at export                         |
| =release=                     | its files: pdfs (with their build), the html directory and entry, bibs     |
| =meta=                        | what an access page shows, from LCNT-INFO (titles, authors, date, ...)     |
<class> (lgcc, lgpc, ...) is the one the document is in, taken from its path (=.../lcnt/<class>/...=). The
site (bisos.webCap) lands the files in its =var/lcnt/= from these specs at each contentBuild; the contract is
=/bisos/asc/web/astro/lcntLibrary/README.org=. One destination failing does not stop the others. After writing
the spec, the site is rebuilt: =<base>/astroProc.spcs -i siteBuild=, or the spec's =siteGenerator= file-var (a
command run with the site's base as its last argument).
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
#+end_org """

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] *Imports* =Based on Classification=cs-u=
#+end_org """
from bisos import b  # noqa: E402
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

import datetime
import os
import pathlib
import re
import shlex
import shutil
import subprocess

defaultResolver = "astroSite.cs -i siteBase"
specsDirName = "lcntSpecs"
specVersion = 1
deSysLcnt = pathlib.Path("/de/sys/lcnt")
# Where an activated BXO is: a BRO by its <org>/<repo> under the first, a BPO by its id under the second.
bxoRoots = {"bro": pathlib.Path("/bisos/git/bxRepos"), "bpo": pathlib.Path("/bxo")}

####+BEGIN: b:py3:cs:orgItem/section :title "Common Parameters Specification" :comment "based on cs.param.CmndParamDict -- As expected from CSU-s"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *Common Parameters Specification* based on cs.param.CmndParamDict -- As expected from CSU-s  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:func/typing :funcName "commonParamsSpecify" :comment "~CSU Specification~" :funcType "ParSpc" :deco ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-T-ParSpc [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/  ~CSU Specification~  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
####+END:
        csParams: cs.param.CmndParamDict,
) -> None:
    pass

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Library" :anchor ""  :extraInfo "A release's spec"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Library_: |]]  A release's spec  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:


def fv(path: pathlib.Path) -> typing.Optional[str]:
    """ One LCNT-INFO file-var: the first line of the file, or None when it is missing or empty. """
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return None
    return lines[0].strip() if lines and lines[0].strip() else None


def authorName(value: typing.Optional[str]) -> typing.Optional[str]:
    """ author1 holds a registry reference (REGISTRY/author/<id>): its Name file, else the id. """
    if not value or not value.startswith('REGISTRY/'):
        return value
    name = fv(pathlib.Path('/lcnt') / value / 'Name')
    return name or value.rsplit('/', 1)[-1]


def unset(value: typing.Any) -> bool:
    """ A file-var that says nothing: empty, or one of lcnt's placeholders ("NA", UnspecifiedDescription, a http://NA/ url). """
    if value in (None, '', [], 'NA', 'UnspecifiedDescription'):
        return True
    return isinstance(value, str) and value.startswith('http://NA/')


def fvWords(path: pathlib.Path) -> typing.List[str]:
    try:
        return path.read_text().split()
    except OSError:
        return []


def classOf(docDir: pathlib.Path) -> typing.Optional[str]:
    """ The lcnt class (lgcc, lgpc, ...) a document is in: the component after the last "lcnt" of its path. """
    found = re.findall(r'/lcnt/(lg[a-z]+)(?=/)', str(docDir) + '/')
    return found[-1] if found else None


def siteBaseOf(fqdn: str, resolver: str) -> typing.Tuple[typing.Optional[pathlib.Path], str]:
    """ (base, "") or (None, reason): the base directory of the web site served as fqdn, from the resolver command.

    The resolver runs as a subprocess and prints "<fqdn> <base>" for a site it knows. A PyCS command exits 0 even when
    it refuses, so the output is what counts: the reason is its EH_Problem line.
    """
    try:
        out = subprocess.run(shlex.split(resolver) + [fqdn], capture_output=True, text=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired) as err:
        return None, f"{fqdn}: the resolver '{resolver}' did not run: {err}"
    for line in out.stdout.splitlines():
        words = line.split(None, 1)
        if len(words) == 2 and words[0] == fqdn and words[1].startswith('/'):
            return pathlib.Path(words[1].strip()), ""
    problems = [line.split(':', 1)[-1].strip() for line in (out.stdout + out.stderr).splitlines() if 'EH_Problem' in line]
    return None, problems[0] if problems else f"{fqdn}: the resolver '{resolver}' found no site"


def generateFor(base: pathlib.Path, generator: typing.Optional[str]) -> str:
    """ Rebuild the site at base, as a subprocess; "" when it built, else the reason.

    The generator is the spec's file-var siteGenerator (run with base as its last argument); without one, the
    site's own <base>/astroProc.spcs -i siteBuild, which lands var/lcnt from lcntSpecs/ and builds the site.
    Its output is read, since a PyCS command exits 0 even when it fails.
    """
    cmd = shlex.split(generator) + [str(base)] if generator else [str(base / 'astroProc.spcs'), '-i', 'siteBuild']
    try:
        out = subprocess.run(cmd, cwd=base, capture_output=True, text=True, timeout=1800)
    except (OSError, subprocess.TimeoutExpired) as err:
        return f"'{' '.join(cmd)}' did not run: {err}"
    text = out.stdout + out.stderr
    if out.returncode != 0 or re.search(r'Traceback|SyntaxError|CRITICAL|EH_Problem|Operation Failed', text):
        lines = [line.strip() for line in text.splitlines() if re.search(r'EH_Problem|Error|PROBLEM|No ', line)]
        return f"'{' '.join(cmd)}' failed: " + (lines[0] if lines else "see its output")
    return ""


def canonicalOf(path: pathlib.Path) -> typing.Optional[pathlib.Path]:
    """ path as seen through /de/sys/lcnt (the same on every host where its BXO is activated), or None.

    The links of /de/sys/lcnt (and of its real directories, e.g. lgpc/rawBisos) are matched by where they resolve.
    """
    real = path.resolve()
    if not deSysLcnt.is_dir():
        return None
    candidates = []
    for each in deSysLcnt.iterdir():
        candidates += [each] if each.is_symlink() else list(each.iterdir()) if each.is_dir() else []
    for link in candidates:
        if not link.is_symlink():
            continue
        try:
            rest = real.relative_to(link.resolve())
        except ValueError:
            continue
        return link / rest
    return None


def git(directory: pathlib.Path, *args: str) -> str:
    """ git's stdout in directory, stripped; "" when it fails. """
    try:
        out = subprocess.run(['git', '-C', str(directory), *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def bxoOf(releaseDir: pathlib.Path) -> typing.Dict[str, typing.Any]:
    """ The BXO holding releaseDir: bxoKind (bro or bpo), bxo, bxoPath and bxoCommit; None where unknown. """
    found: typing.Dict[str, typing.Any] = {'bxoKind': None, 'bxo': None, 'bxoPath': None, 'bxoCommit': None}
    top = git(releaseDir, 'rev-parse', '--show-toplevel')
    if not top:
        return found
    top = pathlib.Path(top).resolve()
    found['bxoPath'] = str(releaseDir.resolve().relative_to(top))
    found['bxoCommit'] = git(releaseDir, 'log', '-1', '--format=%H', '--', '.') or None
    # A BRO clone is <org>/<repo> under bxRepos (which is the auth or the anon tree); a BPO is the last part.
    places = [('bro', bxoRoots['bro'].resolve()), ('bro', pathlib.Path('/bisos/git/auth/bxRepos')),
              ('bro', pathlib.Path('/bisos/git/anon/bxRepos')), ('bpo', bxoRoots['bpo'].resolve())]
    for kind, under in places:
        try:
            rel = top.relative_to(under)
        except ValueError:
            continue
        found.update(bxoKind=kind, bxo=str(rel) if kind == 'bro' else rel.parts[-1])
        return found
    return found


def specOf(
        items: typing.Dict[str, typing.Any],
        docDir: pathlib.Path,
        specDir: pathlib.Path,
) -> typing.Tuple[typing.Dict[str, typing.Any], typing.List[str]]:
    """ The release's spec, for a site's lcntSpecs/: (spec, notes). Notes say what a rebuild elsewhere would miss. """
    releaseDir = items['releaseDir']
    notes = []
    canonical = canonicalOf(releaseDir)
    if canonical is None:
        notes.append(f"{releaseDir} is not under {deSysLcnt}: the spec points at it by its BXO only")
    spec: typing.Dict[str, typing.Any] = {
        'specVersion': specVersion,
        'lcntClass': items['lcntClass'], 'lcntNu': items['lcntNu'], 'relTag': items['relTag'],
        'docNumber': items['meta']['docNumber'],
        'releaseDir': str(canonical) if canonical else None,
        'lcntInfo': str(canonicalOf(docDir / 'LCNT-INFO') or ''),
        'exportSpec': specDir.name,
        'exportedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
        'release': {
            'pdfs': [{'name': p.name, 'build': items.get('pdfBuilds', {}).get(p.name)} for p in items['pdfs']],
            'html': items['html'].name if items['html'] is not None else None,
            'htmlEntry': items['htmlEntry'],
            'bibs': [bib.name for bib in items.get('bibs', [])],
        },
        'meta': {key: value for key, value in items['meta'].items() if not unset(value)},
    }
    spec.update(bxoOf(releaseDir))
    if not spec['bxo']:
        notes.append(f"{releaseDir} is not in a BXO's git repository: another host cannot find it")
    elif git(releaseDir, 'status', '--porcelain', '--', '.'):
        notes.append(f"{releaseDir} has uncommitted changes: commit and push them, or another host gets the older release")
    elif not spec['bxoCommit']:
        notes.append(f"{releaseDir} is not committed: another host cannot find it")
    return spec, notes


def specName(items: typing.Dict[str, typing.Any]) -> str:
    """ <pubcategory>-<lcntNu>-<relTag>.pyl, from LCNT-INFO's pubCategory (else the class): plpc-580003-0.1.pyl. """
    prefix = (items['meta'].get('pubCategory') or items['lcntClass']).lower()
    return f"{prefix}-{items['lcntNu']}-{items['relTag']}.pyl"


def specWrite(spec: typing.Dict[str, typing.Any], name: str, base: pathlib.Path) -> pathlib.Path:
    """ Write the spec as base/lcntSpecs/name (replacing an older one of the same release). Returns the file. """
    specs = base / specsDirName
    specs.mkdir(exist_ok=True)
    path = specs / name
    tmp = specs / f".{name}.new"
    tmp.write_text(metaText(spec))
    os.chmod(tmp, 0o644)
    os.replace(tmp, path)
    return path


def releaseItems(
        docDir: pathlib.Path,
        specDir: pathlib.Path,
) -> typing.Tuple[typing.Dict[str, typing.Any], typing.List[str]]:
    """ What the release holds for the build specs of an export spec: (items, problems).

    items: lcntNu, relTag, releaseDir, meta (title, author, date, version), pdfs (paths),
    html (the directory, or None), htmlEntry (the entry file's name in it, or None).
    """
    info = docDir / 'LCNT-INFO'
    problems: typing.List[str] = []
    items: typing.Dict[str, typing.Any] = {'pdfs': [], 'html': None, 'htmlEntry': None}

    lcntNu = fv(info / 'lcntNu')
    relTag = fv(info / 'Releases' / 'cur' / 'relTag')
    if not lcntNu:
        problems.append(f"{info}/lcntNu is missing")
    if not relTag:
        problems.append(f"{info}/Releases/cur/relTag is missing")
    if problems:
        return items, problems
    releaseBase = fv(info / 'Builds' / 'releaseBaseDir') or './Release'
    releaseDir = (docDir / releaseBase / str(relTag)).resolve()
    if not releaseDir.is_dir():
        return items, [f"no release: {releaseDir} does not exist (make the release first)"]

    lcntClass = classOf(docDir)
    if not lcntClass:
        return items, [f"cannot tell the lcnt class (lgcc, lgpc, ...) from the path {docDir}: expected .../lcnt/<class>/..."]
    pubCategory = fv(info / 'pubCategory')
    items.update(lcntNu=lcntNu, lcntClass=lcntClass, relTag=relTag, releaseDir=releaseDir,
                 bibs=sorted(releaseDir.glob('*.bib')), meta={
        'lcntClass': lcntClass,
        'pubCategory': pubCategory,
        'docNumber': f"{pubCategory}-{lcntNu}" if pubCategory else lcntNu,
        'title': fv(info / 'mainTitle'),
        'subTitle': fv(info / 'subTitle'),
        'subSubTitle': fv(info / 'subSubTitle'),
        'authors': [name for n in range(1, 10) if (name := authorName(fv(info / f'author{n}')))],
        'date': fv(info / 'date'),
        'version': fv(info / 'Releases' / 'cur' / 'versionNu'),
        'group': fv(info / 'docGroup'),
        'url': fv(info / 'url'),
        'description': fv(info / 'description'),
        'organization': fv(info / 'organization'),
        'seeAlso': fv(info / 'seeAlso'),
    })

    for buildSpec in fvWords(specDir / 'buildSpecs'):
        specPath = docDir / buildSpec
        buildName = fv(specPath / 'buildName')
        results = fvWords(specPath / 'results')
        if not buildName:
            problems.append(f"{specPath}/buildName is missing")
            continue
        if 'pdf' in results:
            pdf = releaseDir / f"c-{lcntNu}-{relTag}-{buildName}.pdf"
            if pdf.is_file():
                items['pdfs'].append(pdf)
                items.setdefault('pdfBuilds', {})[pdf.name] = buildName
            else:
                problems.append(f"not released: {pdf.name}")
        if 'html' in results and items['html'] is None:
            htmlDir = releaseDir / f"c-{lcntNu}-{buildName}-html"
            docSrc = fv(specPath / 'docSrc') or ''
            entry = pathlib.Path(docSrc).stem + '.html' if docSrc else None
            if htmlDir.is_dir():
                items['html'] = htmlDir
                items['htmlEntry'] = 'index.html' if (htmlDir / 'index.html').is_file() else entry
            else:
                problems.append(f"not released: {htmlDir.name}/")
    if not items['pdfs'] and items['html'] is None:
        problems.append("nothing to export: the build specs released no pdf and no html")
    return items, problems


def metaText(meta: typing.Dict[str, typing.Any]) -> str:
    """ The release's meta as the text of meta.pyl: one Python literal, formatted by black (pprint if black is missing). """
    text = repr(dict(sorted(meta.items())))
    try:
        import black
        return black.format_str(text, mode=black.Mode())
    except Exception:                                      # not importable, or black refused: still a valid literal
        import pprint
        return pprint.pformat(dict(sorted(meta.items()))) + "\n"


####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Direct Command Services" :anchor ""  :extraInfo "Examples and CSs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Direct Command Services_: |]]  Examples and CSs  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "examples_csu" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv "pyKwArgs"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<examples_csu>>  =verify= ro=cli pyInv=pyKwArgs   [[elisp:(org-cycle)][| ]]
#+end_org """
class examples_csu(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             pyKwArgs: typing.Any=None,   # pyInv Argument
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return failed(cmndOutcome)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Examples of the localWeb export of a released LCNT document.
        #+end_org """)

        cmnd = cs.examples.cmndEnter
        cs.examples.menuChapter('=localWebExport= -- point the web sites of its export spec at a document\'s release, and rebuild them')
        cmnd('localWebExport', args=". ./LCNT-INFO/Exports/localWeb", comment=" # run in the document's directory, after a release")
        return(cmndOutcome)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "localWebExport" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 2 :argsMax 2 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<localWebExport>>  =verify= argsMin=2 argsMax=2 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class localWebExport(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 2, 'Max': 2,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        failed = b_io.eh.badOutcome
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return failed(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Write a spec of the release of the LCNT document in docDir into the lcntSpecs/ of each web site named in the export spec's destinations, then rebuild that site. Prints "specified <lcntNu> <fqdn> <file>" and "rebuilt <fqdn> <base>" per success, a problem per failure, and notes on what a rebuild on another host would miss.
        #+end_org """)

        docArg = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        specArg = self.cmndArgsGet("1", cmndArgsSpecDict, argsList)
        if not docArg or not specArg:
            b_io.eh.problem_usageError("Usage: localWebExport <docDir> <exportSpecDir>")
            return failed(cmndOutcome)
        docDir = pathlib.Path(docArg).resolve()
        specDir = pathlib.Path(specArg)
        if not specDir.is_absolute():
            specDir = docDir / specDir
        if not specDir.is_dir():
            b_io.eh.problem_usageError(f"No export spec directory {specDir}")
            return failed(cmndOutcome)

        fqdns = fvWords(specDir / 'destinations')
        if not fqdns:
            b_io.eh.problem_usageError(f"{specDir}/destinations is missing or empty: list the FQDNs of the web sites on this system")
            return failed(cmndOutcome)

        items, problems = releaseItems(docDir, specDir)
        for problem in problems:
            b_io.eh.problem_usageError(problem)
        if 'releaseDir' not in items or (items['html'] is None and not items['pdfs']):
            return failed(cmndOutcome)

        spec, notes = specOf(items, docDir, specDir)
        for note in notes:
            print(f"note: {note}")
        resolver = fv(specDir / 'siteResolver') or defaultResolver
        allLanded = not problems
        for fqdn in fqdns:
            base, reason = siteBaseOf(fqdn, resolver)
            if base is None:
                b_io.eh.problem_usageError(reason)
                allLanded = False
                continue
            try:
                written = specWrite(spec, specName(items), base)
            except OSError as err:
                b_io.eh.problem_usageError(f"{fqdn}: cannot write the spec under {base}/{specsDirName}: {err}")
                allLanded = False
                continue
            print(f"specified {items['lcntNu']} {fqdn} {written}")
            reason = generateFor(base, fv(specDir / 'siteGenerator'))
            if reason:
                b_io.eh.problem_usageError(f"{fqdn}: specified, but the site was not rebuilt: {reason}")
                allLanded = False
            else:
                print(f"rebuilt {fqdn} {base}")

        if not allLanded:
            return failed(cmndOutcome)
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """
***** Cmnd Args Specification
"""
        cmndArgsSpecDict = cs.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="docDir",
            argDefault='.',
            argChoices=[],
            argDescription="The LCNT document's directory (holds LCNT-INFO and Release)"
        )
        cmndArgsSpecDict.argsDictAdd(
            argPosition="1",
            argName="exportSpecDir",
            argDefault='',
            argChoices=[],
            argDescription="The export spec, e.g. ./LCNT-INFO/Exports/localWeb (or ./curExport)"
        )

        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
