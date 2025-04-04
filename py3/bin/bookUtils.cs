#!/bin/env python
# -*- coding: utf-8 -*-

""" #+begin_org
* ~[Summary]~ :: A =CmndSvc= for
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

####+BEGIN: b:prog:file/proclamations :outLevel 1
""" #+begin_org
* *[[elisp:(org-cycle)][| Proclamations |]]* :: Libre-Halaal Software --- Part Of BISOS ---  Poly-COMEEGA Format.
** This is Libre-Halaal Software. © Neda Communications, Inc. Subject to AGPL.
** It is part of BISOS (ByStar Internet Services OS)
** Best read and edited  with Blee in Poly-COMEEGA (Polymode Colaborative Org-Mode Enhance Emacs Generalized Authorship)
#+end_org """
####+END:

####+BEGIN: b:prog:file/particulars :authors ("./inserts/authors-mb.org")
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: Authors, version
** This File: /bisos/git/auth/bxRepos/bisos/bpip1/bin/bookSpineCalc.cs
** Authors: Mohsen BANAN, http://mohsen.banan.1.byname.net/contact
#+end_org """
####+END:

####+BEGIN: b:py3:file/particulars-csInfo :status "inUse"
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars-csInfo |]]*
#+end_org """
import typing
csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['bookSpineCalc'], }
csInfo['version'] = '202303180147'
csInfo['status']  = 'inUse'
csInfo['panel'] = 'bookSpineCalc-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: [[file:/bisos/git/auth/bxRepos/blee-binders/bisos-core/COMEEGA/_nodeBase_/fullUsagePanel-en.org][BISOS COMEEGA Panel]]
Module description comes here.
** Relevant Panels: /bisos/git/auth/bxRepos/blee-binders/bisos-apps/lcnt/lcntArtTypes/books/bookCovers/_nodeBase_/fullUsagePanel-en.org
** Status: In use with BISOS
** /[[elisp:(org-cycle)][| Planned Improvements |]]/ :
*** TODO complete fileName in particulars.
#+end_org """

####+BEGIN: b:prog:file/orgTopControls :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Controls |]] :: [[elisp:(delete-other-windows)][(1)]] | [[elisp:(show-all)][Show-All]]  [[elisp:(org-shifttab)][Overview]]  [[elisp:(progn (org-shifttab) (org-content))][Content]] | [[file:Panel.org][Panel]] | [[elisp:(blee:ppmm:org-mode-toggle)][Nat]] | [[elisp:(bx:org:run-me)][Run]] | [[elisp:(bx:org:run-me-eml)][RunEml]] | [[elisp:(progn (save-buffer) (kill-buffer))][S&Q]]  [[elisp:(save-buffer)][Save]]  [[elisp:(kill-buffer)][Quit]] [[elisp:(org-cycle)][| ]]
** /Version Control/ ::  [[elisp:(call-interactively (quote cvs-update))][cvs-update]]  [[elisp:(vc-update)][vc-update]] | [[elisp:(bx:org:agenda:this-file-otherWin)][Agenda-List]]  [[elisp:(bx:org:todo:this-file-otherWin)][ToDo-List]]

#+end_org """
####+END:

####+BEGIN: b:py3:file/workbench :outLevel 1
""" #+begin_org
* [[elisp:(org-cycle)][| Workbench |]] :: [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pyclbr %s" (bx:buf-fname))))][pyclbr]] || [[elisp:(python-check (format "/bisos/venv/py3/bisos3/bin/python -m pydoc ./%s" (bx:buf-fname))))][pydoc]] || [[elisp:(python-check (format "/bisos/pipx/bin/pyflakes %s" (bx:buf-fname)))][pyflakes]] | [[elisp:(python-check (format "/bisos/pipx/bin/pychecker %s" (bx:buf-fname))))][pychecker (executes)]] | [[elisp:(python-check (format "/bisos/pipx/bin/pycodestyle %s" (bx:buf-fname))))][pycodestyle]] | [[elisp:(python-check (format "/bisos/pipx/bin/flake8 %s" (bx:buf-fname))))][flake8]] | [[elisp:(python-check (format "/bisos/pipx/bin/pylint %s" (bx:buf-fname))))][pylint]]  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
** Imports Based On Classification=cs-u
#+end_org """
from bisos import b
from bisos.b import cs
from bisos.b import b_io
from bisos.common import csParam

import collections
####+END:

from checkdigit import isbn

####+BEGIN: bx:dblock:python:func :funcName "commonParamsSpecify" :funcType "ParSpec" :retType "" :deco "" :argsList "csParams"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  F-ParSpec  [[elisp:(outline-show-subtree+toggle)][||]] /commonParamsSpecify/ retType= argsList=(csParams)  [[elisp:(org-cycle)][| ]]
#+end_org """
def commonParamsSpecify(
    csParams,
):
####+END:
    csParams.parDictAdd(
        parName='nuOfPages',
        parDescription="Number of pages",
        parDataType=None,
        parDefault=None,
        parChoices=["any"],
        # parScope=icm.CmndParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--nuOfPages',
    )
    csParams.parDictAdd(
        parName='gsm',
        parDescription="Paper Weight (gsm) grams per square meter -- usually between 70 and 90",
        parDataType=None,
        parDefault=70,
        parChoices=["any"],
        # parScope=icm.CmndParamScope.TargetParam,
        argparseShortOpt=None,
        argparseLongOpt='--gsm',
    )

""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] ~csuList emacs-list Specifications~  [[elisp:(blee:org:code-block/above-run)][ /Eval Below/ ]] [[elisp:(org-cycle)][| ]]
#+BEGIN_SRC emacs-lisp
(setq  b:py:cs:csuList
  (list
   "bisos.b.cs.ro"
   "blee.icmPlayer.bleep"
 ))
#+END_SRC
#+RESULTS:
| bisos.b.cs.ro | blee.icmPlayer.bleep |
#+end_org """

####+BEGINNOT: b:py3:cs:framework/csuListProc :pyImports t :csuImports t :csuParams t
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] =Process CSU List= with /2/ in csuList pyImports=t csuImports=t csuParams=t
#+end_org """

from bisos.b.cs import ro
from blee.icmPlayer import bleep


csuList = [ 'bisos.b.cs.ro', 'blee.icmPlayer.bleep', ]

g_importedCmndsModules = cs.csuList_importedModules(csuList)

def g_extraParams():
    csParams = cs.param.CmndParamDict()
    commonParamsSpecify(csParams)
    cs.csuList_commonParamsSpecify(csuList, csParams)
    cs.argsparseBasedOnCsParams(csParams)

####+END:

####+BEGIN: b:py3:cs:main/exposedSymbols :classes ()
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] ~Exposed Symbols List Specification~ with /0/ in Classes List
#+end_org """
####+END:

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "CmndSvcs" :anchor ""  :extraInfo "Command Services Section"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _CmndSvcs_: |]]  Command Services Section  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "examples" :extent "verify" :ro "noCli" :comment "FrameWrk: CS-Main-Examples" :parsMand "" :parsOpt "" :argsMin "0" :argsMax "0" :asFunc "" :interactiveP ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<examples>>  *FrameWrk: CS-Main-Examples*  =verify= argsMin=0 argsMax=0 ro=noCli   [[elisp:(org-cycle)][| ]]
#+end_org """
class examples(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}
    rtInvConstraints = cs.rtInvoker.RtInvoker.new_noRo() # NO RO From CLI

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:
        """FrameWrk: CS-Main-Examples"""
        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
***** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Conventional top level example.
        #+end_org """)

        def cpsInit(): return collections.OrderedDict()
        def menuItem(verbosity): cs.examples.cmndInsert(cmndName, cps, cmndArgs, verbosity=verbosity) # 'little' or 'none'
        def execLineEx(cmndStr): cs.examples.execInsert(execLine=cmndStr)

        #logControler = b_io.log.Control()
        #logControler.loggerSetLevel(20)

        cs.examples.myName(cs.G.icmMyName(), cs.G.icmMyFullName())

        cs.examples.commonBrief()

        bleep.examples_icmBasic()

        cs.examples.menuChapter('=ISBN=  *Facilities*')

        cmndName = 'isbnCalculate13' ; cmndArgs = '978-1-960957-00' ;
        cps=cpsInit() ;  menuItem(verbosity='little')

        cmndName = 'isbnValidate13' ; cmndArgs = '978-1-960957-00-9' ;
        cps=cpsInit() ;  menuItem(verbosity='little')

        cs.examples.menuChapter('=PDF=  *Facilities*')

        cmndName = 'pdfNuOfPages' ; cmndArgs = '/lcnt/lgpc/bystar/permanent/facilities/marmee/marmeeEmacsConf22/presentationEnFa.pdf' ;
        cps=cpsInit() ;  menuItem(verbosity='little')

        cs.examples.menuChapter('=Spine=  *Facilities*')

        cmndName = 'spineWidthSoft' ; cmndArgs = '' ;
        cps=cpsInit() ; cps['nuOfPages'] = 250 ; cps['gsm'] = 80 ;  menuItem(verbosity='little')

        cmndName = 'spineWidthHard' ; cmndArgs = '' ;
        cps=cpsInit() ; cps['nuOfPages'] = 250 ; cps['gsm'] = 80 ;  menuItem(verbosity='little')

        cmndName = 'pdfSpineWidthSoft' ; cmndArgs = '/lcnt/lgpc/bystar/permanent/facilities/marmee/marmeeEmacsConf22/presentationEnFa.pdf' ;
        cps=cpsInit() ; cps['gsm'] = 80 ; menuItem(verbosity='little')

        cmndName = 'pdfSpineWidthHard' ; cmndArgs = '/lcnt/lgpc/bystar/permanent/facilities/marmee/marmeeEmacsConf22/presentationEnFa.pdf' ;
        cps=cpsInit() ; cps['gsm'] = 80 ; menuItem(verbosity='little')

        # execLineEx(f"""echo sudo apt -y install gnupg""")

        b.ignore(ro.__doc__,)  # We are not using these modules, but they are auto imported.

        return(cmndOutcome)

####+BEGIN: bx:icm:py3:section :title "CS-Commands -- ISBN"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS-Commands*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "isbnCalculate13" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<isbnCalculate13>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class isbnCalculate13(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  arg0 is ~inFile~. Count nu of pages of ~inFile~ and calculate =spineWidth= based on ~gsm~

        [[spineWidthSoft]] does the actual caluculations.
        #+end_org """)

        inIsbn = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        if not inIsbn: return(b_io.eh.badOutcome(cmndOutcome))

        isbnCheckSum = isbn.calculate(inIsbn)

        # if rtInv.outs: print(isbnCheckSum)
        cmndOutcome.results = isbnCheckSum

        return(cmndOutcome)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] arg0 is ~inFile~
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="inIsbn",
            argChoices=[],
            argDescription="Input ISBN Number"
        )
        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "isbnValidate13" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<isbnValidate13>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class isbnValidate13(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  arg0 is ~inFile~. Count nu of pages of ~inFile~ and calculate =spineWidth= based on ~gsm~

        [[spineWidthSoft]] does the actual caluculations.
        #+end_org """)

        inIsbn = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        if not inIsbn: return(b_io.eh.badOutcome(cmndOutcome))

        isValid = isbn.validate(inIsbn)

        # if rtInv.outs: print(isValid)
        cmndOutcome.results = isValid

        return(cmndOutcome)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] arg0 is ~inFile~
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="inIsbn",
            argChoices=[],
            argDescription="Input ISBN Number"
        )
        return cmndArgsSpecDict

####+BEGIN: bx:icm:py3:section :title "CS-Commands -- PDF"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS-Commands -- PDF*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "pdfNuOfPages" :comment "" :extent "verify" :ro "cli" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<pdfNuOfPages>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class pdfNuOfPages(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        callParamsDict = {}
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  arg0 is ~inFile~. Count nu of pages of ~inFile~ and calculate =spineWidth= based on ~gsm~

        [[spineWidthSoft]] does the actual caluculations.
        #+end_org """)

        inFile = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        if not inFile: return(b_io.eh.badOutcome(cmndOutcome))

        if not (nuOfPages := b.subProc.Op(outcome=cmndOutcome, log=0).bash(
                f"""echo $(pdfinfo {inFile}  | grep ^Pages | cut -d ':' -f 2)""",
        ).stdout):  return(icm.EH_badOutcome(cmndOutcome))

        # if rtInv.outs: print(nuOfPages)
        cmndOutcome.results = nuOfPages

        return(cmndOutcome)


####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] arg0 is ~inFile~
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="inFile",
            argChoices=[],
            argDescription="Input File"
        )
        return cmndArgsSpecDict

####+BEGIN: bx:icm:py3:section :title "CS-Commands --- Spine Width"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  /Section/    [[elisp:(outline-show-subtree+toggle)][||]] *CS-Commands*  [[elisp:(org-cycle)][| ]]
#+end_org """
####+END:

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "spineWidthSoft" :comment "" :extent "verify" :ro "cli" :parsMand "nuOfPages gsm" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<spineWidthSoft>>  =verify= parsMand=nuOfPages gsm ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class spineWidthSoft(cs.Cmnd):
    cmndParamsMandatory = [ 'nuOfPages', 'gsm', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             nuOfPages: typing.Optional[str]=None,  # Cs Mandatory Param
             gsm: typing.Optional[str]=None,  # Cs Mandatory Param
    ) -> b.op.Outcome:

        callParamsDict = {'nuOfPages': nuOfPages, 'gsm': gsm, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        nuOfPages = csParam.mappedValue('nuOfPages', nuOfPages)
        gsm = csParam.mappedValue('gsm', gsm)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Calculate =bookSpineWidthSoft= based on ~nuOfPages~ and ~gsm~

        Algorithm taken from Book Spine Calculator https://wiki.scribus.net/canvas/Book_Spine_Calculator

        The conventional design suggests that spine width is calculated as follows:
        10 divided by 176, multiplied by the number of pages of text within the book, divided by 90,
        multiplied by the weight of the paper in gsm (grams per square meter),
        add 1mm for the crease in the cover and this will give you a soft cover book thickness in millimetres.
        #+end_org """)

        nuOfPages = float(nuOfPages)
        weightInGsm = float(gsm)

        bookSpineWidthSoft = (float(10)/float(176)) * (nuOfPages/90) * weightInGsm + 1
        bookSpineWidthSoftStr = "{:.2f}".format(bookSpineWidthSoft)

        # if rtInv.outs: print(bookSpineWidthSoftStr)
        cmndOutcome.results = bookSpineWidthSoftStr

        return(cmndOutcome)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "spineWidthHard" :comment "" :extent "verify" :ro "cli" :parsMand "nuOfPages gsm" :parsOpt "" :argsMin 0 :argsMax 0 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<spineWidthHard>>  =verify= parsMand=nuOfPages gsm ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class spineWidthHard(cs.Cmnd):
    cmndParamsMandatory = [ 'nuOfPages', 'gsm', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 0,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             nuOfPages: typing.Optional[str]=None,  # Cs Mandatory Param
             gsm: typing.Optional[str]=None,  # Cs Mandatory Param
    ) -> b.op.Outcome:

        callParamsDict = {'nuOfPages': nuOfPages, 'gsm': gsm, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, None).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        nuOfPages = csParam.mappedValue('nuOfPages', nuOfPages)
        gsm = csParam.mappedValue('gsm', gsm)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Calculate =bookSpineWidthHard= based on ~nuOfPages~ and ~gsm~

        First obtain [[spineWidthSoft]], then
        Add 3mm to this figure and you have the spine thickness of a hard covered book
        #+end_org """)

        if not (spineWidthSoftStr := spineWidthSoft(cmndOutcome=cmndOutcome).cmnd(
                rtInv=cs.RtInvoker.new_py(), cmndOutcome=cmndOutcome,
                gsm=gsm,
                nuOfPages=nuOfPages,
        ).results): return(b_io.eh.badOutcome(cmndOutcome))

        bookSpineWidthHard = float(spineWidthSoftStr) + 3

        bookSpineWidthHardStr = "{:.2f}".format(bookSpineWidthHard)

        # if rtInv.outs: print (bookSpineWidthHardStr)
        cmndOutcome.results = bookSpineWidthHardStr

        return(cmndOutcome)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "pdfSpineWidthSoft" :comment "" :extent "verify" :ro "cli" :parsMand "gsm" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<pdfSpineWidthSoft>>  =verify= parsMand=gsm argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class pdfSpineWidthSoft(cs.Cmnd):
    cmndParamsMandatory = [ 'gsm', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             gsm: typing.Optional[str]=None,  # Cs Mandatory Param
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        callParamsDict = {'gsm': gsm, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
        gsm = csParam.mappedValue('gsm', gsm)
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  arg0 is ~inFile~. Count nu of pages of ~inFile~ and calculate =spineWidth= based on ~gsm~

        [[spineWidthSoft]] does the actual caluculations.
        #+end_org """)

        inFile = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        if not inFile: return(b_io.eh.badOutcome(cmndOutcome))

        if not (nuOfPages := pdfNuOfPages(cmndOutcome=cmndOutcome).cmnd(
                rtInv=cs.RtInvoker.new_py(), cmndOutcome=cmndOutcome,
                argsList=[inFile]
        ).results): return(b_io.eh.badOutcome(cmndOutcome))

        if not (spineWidth := spineWidthSoft(cmndOutcome=cmndOutcome).cmnd(
                rtInv=cs.RtInvoker.new_py(), cmndOutcome=cmndOutcome,
                gsm=gsm,
                nuOfPages=nuOfPages,
        ).results): return(b_io.eh.badOutcome(cmndOutcome))

        # if rtInv.outs: print(spineWidth)
        cmndOutcome.results = spineWidth

        return(cmndOutcome)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] arg0 is ~inFile~
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="inFile",
            argChoices=[],
            argDescription="Input File"
        )
        return cmndArgsSpecDict

####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "pdfSpineWidthHard" :comment "" :extent "verify" :ro "cli" :parsMand "gsm" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<pdfSpineWidthHard>>  =verify= parsMand=gsm argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class pdfSpineWidthHard(cs.Cmnd):
    cmndParamsMandatory = [ 'gsm', ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmnd(self,
             rtInv: cs.RtInvoker,
             cmndOutcome: b.op.Outcome,
             gsm: typing.Optional[str]=None,  # Cs Mandatory Param
             argsList: typing.Optional[list[str]]=None,  # CsArgs
    ) -> b.op.Outcome:

        callParamsDict = {'gsm': gsm, }
        if self.invocationValidate(rtInv, cmndOutcome, callParamsDict, argsList).isProblematic():
            return b_io.eh.badOutcome(cmndOutcome)
        cmndArgsSpecDict = self.cmndArgsSpec()
        gsm = csParam.mappedValue('gsm', gsm)
####+END:

        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  arg0 is ~inFile~. Count nu of pages of ~inFile~ and calculate =spineWidth= based on ~gsm~

        [[spineWidthHard]] does the actual caluculations.
        #+end_org """)

        inFile = self.cmndArgsGet("0", cmndArgsSpecDict, argsList)
        if not inFile: return(b_io.eh.badOutcome(cmndOutcome))

        if not (nuOfPages := pdfNuOfPages(cmndOutcome=cmndOutcome).cmnd(
                rtInv=cs.RtInvoker.new_py(), cmndOutcome=cmndOutcome,
                argsList=[inFile]
        ).results): return(b_io.eh.badOutcome(cmndOutcome))

        if not (spineWidth := spineWidthHard(cmndOutcome=cmndOutcome).cmnd(
                rtInv=cs.RtInvoker.new_py(), cmndOutcome=cmndOutcome,
                gsm=gsm,
                nuOfPages=nuOfPages,
        ).results): return(b_io.eh.badOutcome(cmndOutcome))

        # if rtInv.outs: print(spineWidth)
        cmndOutcome.results = spineWidth

        return(cmndOutcome)

####+BEGIN: b:py3:cs:method/args :methodName "cmndArgsSpec" :methodType "anyOrNone" :retType "bool" :deco "default" :argsList "self"
    """ #+begin_org
**  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  Mtd-T-anyOrNone [[elisp:(outline-show-subtree+toggle)][||]] /cmndArgsSpec/ deco=default  deco=default  [[elisp:(org-cycle)][| ]]
    #+end_org """
    @cs.track(fnLoc=True, fnEntry=True, fnExit=True)
    def cmndArgsSpec(self, ):
####+END:
        """  #+begin_org
*** [[elisp:(org-cycle)][| *cmndArgsSpec:* | ]] arg0 is ~inFile~
        #+end_org """

        cmndArgsSpecDict = cs.arg.CmndArgsSpecDict()
        cmndArgsSpecDict.argsDictAdd(
            argPosition="0",
            argName="inFile",
            argChoices=[],
            argDescription="Input File"
        )
        return cmndArgsSpecDict

####+BEGIN: blee:bxPanel:foldingSection :outLevel 0 :sep nil :title "Main" :anchor ""  :extraInfo "Framework Dblock"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*     [[elisp:(outline-show-subtree+toggle)][| _Main_: |]]  Framework Dblock  [[elisp:(org-shifttab)][<)]] E|
#+end_org """
####+END:

####+BEGIN: b:py3:cs:framework/main :csInfo "csInfo" :noCmndEntry "examples" :extraParamsHook "g_extraParams" :importedCmndsModules "g_importedCmndsModules"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] =g_csMain= (csInfo, _examples_, g_extraParams, g_importedCmndsModules)
#+end_org """

if __name__ == '__main__':
    cs.main.g_csMain(
        csInfo=csInfo,
        noCmndEntry=examples,  # specify a Cmnd name
        extraParamsHook=g_extraParams,
        importedCmndsModules=g_importedCmndsModules,
    )

####+END:

####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
