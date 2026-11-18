# -*- coding: utf-8 -*-
""" #+begin_org
* *[[elisp:(org-cycle)][| Particulars |]]* :: The audio of an LCNT document: narration, text-to-speech, recordings, selection
** This File: /bisos/git/bxRepos/bisos-pip/lcnt/py3/bisos/lcnt/lcntAudio_csu.py
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
csInfo['version'] = '202611170001'
csInfo['status']  = 'inDev'
csInfo['panel'] = 'lcntAudio_csu-Panel.org'
csInfo['groupingType'] = 'IcmGroupingType-pkged'
csInfo['cmndParts'] = 'IcmCmndParts[common] IcmCmndParts[param]'
####+END:

""" #+begin_org
* [[elisp:(org-cycle)][| ~Description~ |]] :: The commands of <docDir>/audio/audioProc.spcs
Each labelled frame of the document has a narration, the text of its pnote. Reveal plays =audio/<label>.mp3=
(frameaudio). Two sources are kept side by side and a link selects what plays:
| =tts-<label>.mp3 .length .textHash=      | written by ttsGenerate (Piper), redone when the narration changes |
| =rec-<label>.wav .mp3 .length .textHash= | the author's recording; recFinalize makes the mp3 and the rest    |
| =<label>.mp3 <label>.length=             | relative links to one source, set by audioSelect                  |
A recording whose =.textHash= differs from the narration is reported stale. The library is lcntAudio_seedInfo.
Commands that take labels act on those frames only; with none, on every frame.
** Status: In development
#+end_org """

####+BEGIN: b:py3:cs:framework/imports :basedOn "classification"
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CsFrmWrk   [[elisp:(outline-show-subtree+toggle)][||]] *Imports* =Based on Classification=cs-u=
#+end_org """
from bisos import b  # noqa: E402
from bisos.b import cs
from bisos.b import b_io

import collections
####+END:

import pathlib
import typing

from bisos.lcnt import lcntAudio_seedInfo as info


def commonParamsSpecify(
        csParams: cs.param.CmndParamDict,
) -> None:
    pass


def framesFor(argsList: typing.Optional[list[str]]) -> typing.Tuple[info.AudioParams, typing.List[info.Frame]]:
    """ The params of this plant and its frames, narrowed to the labels given. Raises ValueError. """
    p = info.paramsFromPlantPath()
    frames = info.framesOf(p.docSrc)
    if argsList:
        known = {frame.label: frame for frame in frames}
        unknown = [label for label in argsList if label not in known]
        if unknown:
            raise ValueError(f"not frame labels of {p.docSrc.name}: {' '.join(unknown)}")
        frames = [known[label] for label in argsList]
    return p, frames


def mmss(ms: int) -> str:
    return f"{ms // 60000}:{ms // 1000 % 60:02d}"


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "narrationList" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<narrationList>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class narrationList(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  The frames in document order: label, words of narration, and the time at 140 words a minute.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        totalWords = 0
        print(f"{'label':28} {'words':>5} {'est':>5}  {p.docSrc.name}")
        for frame in frames:
            totalWords += frame.words
            est = mmss(frame.words * 60000 // info.wordsPerMinute)
            print(f"{frame.label:28} {frame.words:>5} {est:>5}  {'' if frame.words else '(no narration)'}")
        print(f"{'total ' + str(len(frames)) + ' frames':28} {totalWords:>5} {mmss(totalWords * 60000 // info.wordsPerMinute):>5}")
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "narrationText" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<narrationText>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class narrationText(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  The text a frame's tts speaks: its pnote as plain text, with the ttsLexicon applied.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        print(info.lexiconApplied(frames[0].narration, info.lexiconOf(p.audioDir)))
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "ttsGenerate" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<ttsGenerate>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class ttsGenerate(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  tts-<label>.mp3, .length and .textHash for each frame with narration, redone only where the narration, lexicon, voice or engine changed. A frame playing nothing is then linked to its recording, else its tts. Links already set are left as they are.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        lexicon = info.lexiconOf(p.audioDir)
        print(f"voice {p.voice}, piper-tts {info.lcntTtsInfo.piperVersion}, lexicon {len(lexicon)} terms")
        allWell = True
        for frame in frames:
            state, detail = info.ttsGenerateOne(p.audioDir, frame, p.voice, lexicon)
            print(f"{frame.label:28} {state:10} {detail or ''}")
            if state == "failed":
                allWell = False
                continue
            if info.playing(p.audioDir, frame.label) in ("none", "dangling"):
                source = info.preferred(p.audioDir, frame.label, "rec")
                if source and info.select(p.audioDir, frame.label, source) is None:
                    print(f"{'':28} {'linked':10} {frame.label}.mp3 -> {source}-{frame.label}.mp3")
        if not allWell:
            return failed(cmndOutcome)
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "audioSelect" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<audioSelect>>  =verify= argsMin=1 argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class audioSelect(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  audioSelect rec|tts [label ...]: link <label>.mp3 and .length to that source. Named frames must have it. With no labels, every frame: the source where it exists, else the other one; a frame with neither plays nothing. Stale recordings are used, and reported.
        #+end_org """)
        source = argsList[0]
        if source not in info.sources:
            b_io.eh.problem_usageError(f"Usage: audioSelect {'|'.join(info.sources)} [label ...]")
            return failed(cmndOutcome)
        labels = argsList[1:]
        try:
            p, frames = framesFor(labels)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        allWell = True
        for frame in frames:
            chosen = source if labels else info.preferred(p.audioDir, frame.label, source)
            if chosen is None:
                print(f"{frame.label:28} {'nothing':8} no rec- and no tts- audio")
                continue
            reason = info.select(p.audioDir, frame.label, chosen)
            if reason:
                b_io.eh.problem_usageError(f"{frame.label}: {reason}")
                allWell = False
                continue
            stale = " (stale: older than its narration)" if info.isStale(p.audioDir, chosen, frame) else ""
            print(f"{frame.label:28} {chosen:8} {frame.label}.mp3 -> {chosen}-{frame.label}.mp3{stale}")
        if not allWell:
            return failed(cmndOutcome)
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "audioReport" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<audioReport>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class audioReport(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Per frame: what plays, the tts and the recording (time, or stale), and the total time that plays by source. Read-only.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)

        def sourceCell(source: str, frame: info.Frame) -> str:
            if not info.has(p.audioDir, source, frame.label):
                return "-"
            ms = info.lengthMs(info.path(p.audioDir, source, frame.label, "length"))
            cell = mmss(ms) if ms is not None else "?"
            return cell + (" stale" if info.isStale(p.audioDir, source, frame) else "")

        totals: typing.Dict[str, int] = collections.Counter()
        counts: typing.Dict[str, int] = collections.Counter()
        print(f"{'label':28} {'plays':8} {'tts':11} {'rec':11}")
        for frame in frames:
            plays = info.playing(p.audioDir, frame.label)
            counts[plays] += 1
            if plays in info.sources:
                totals[plays] += info.lengthMs(info.path(p.audioDir, None, frame.label, "length")) or 0
            note = "" if frame.words else "no narration"
            print(f"{frame.label:28} {plays:8} {sourceCell('tts', frame):11} {sourceCell('rec', frame):11} {note}")
        playsStr = ", ".join(f"{source} {counts[source]} frames {mmss(totals[source])}" for source in info.sources)
        others = ", ".join(f"{kind} {n}" for kind, n in counts.items() if kind not in info.sources)
        print(f"plays: {playsStr}; total {mmss(sum(totals.values()))}" + (f"; {others}" if others else ""))
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "recordCmnds" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<recordCmnds>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class recordCmnds(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Print, per frame with narration, the command to record it into rec-<label>.wav (audacity), then recFinalize. Runs nothing: recording needs a sound device, which a container lacks.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        for frame in frames:
            if frame.words:
                print(f"audacity {info.path(p.audioDir, 'rec', frame.label, 'wav')}")
        print(f"{p.audioDir / info.spcsName} -i recFinalize      # then: -i audioSelect rec")
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "recFinalize" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<recFinalize>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class recFinalize(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  For each recording: rec-<label>.wav into .mp3 when the wav is newer (or record straight to the mp3), then .length, and .textHash as the narration is now, which marks the recording current. Selects nothing.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        allWell = True
        for frame in frames:
            state, detail = info.recFinalizeOne(p.audioDir, frame)
            if state == "skipped" and not argsList:
                continue
            print(f"{frame.label:28} {state:10} {detail or ''}")
            allWell = allWell and state != "failed"
        if not allWell:
            return failed(cmndOutcome)
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "ttsClean" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 0 :argsMax 9999 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<ttsClean>>  =verify= argsMax=9999 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class ttsClean(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 0, 'Max': 9999,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  Delete what ttsGenerate makes again: tts-<label>.*, the links to them, dangling links, leftovers and __pycache__ (with labels: those frames' tts and links only). Recordings, links to them, audioProc.spcs, .gitignore and ttsLexicon are kept.
        #+end_org """)
        try:
            p, frames = framesFor(argsList)
        except (ValueError, OSError) as err:
            b_io.eh.problem_usageError(str(err))
            return failed(cmndOutcome)
        found = info.ttsCleanPaths(p.audioDir, [frame.label for frame in frames] if argsList else None)
        allWell = True
        for each in found:
            try:
                info.remove(each)
                print(f"removed {each.name}")
            except OSError as err:
                b_io.eh.problem_usageError(f"{each}: {err}")
                allWell = False
        print(f"{len(found)} removed; ttsGenerate makes them again")
        if not allWell:
            return failed(cmndOutcome)
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


####+BEGIN: b:py3:cs:cmnd/classHead :cmndName "audioPlant" :extent "verify" :ro "cli" :comment "" :parsMand "" :parsOpt "" :argsMin 1 :argsMax 1 :pyInv ""
""" #+begin_org
*  _[[elisp:(blee:menu-sel:outline:popupMenu)][±]]_ _[[elisp:(blee:menu-sel:navigation:popupMenu)][Ξ]]_ [[elisp:(outline-show-branches+toggle)][|=]] [[elisp:(bx:orgm:indirectBufOther)][|>]] *[[elisp:(blee:ppmm:org-mode-toggle)][|N]]*  CmndSvc-   [[elisp:(outline-show-subtree+toggle)][||]] <<audioPlant>>  =verify= argsMin=1 argsMax=1 ro=cli   [[elisp:(org-cycle)][| ]]
#+end_org """
class audioPlant(cs.Cmnd):
    cmndParamsMandatory = [ ]
    cmndParamsOptional = [ ]
    cmndArgsLen = {'Min': 1, 'Max': 1,}

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
####+END:
        self.cmndDocStr(f""" #+begin_org
** [[elisp:(org-cycle)][| *CmndDesc:* | ]]  audioPlant <docDir>: <docDir>/audio/ with audioProc.spcs, .gitignore (the audio stays out of git) and an empty ttsLexicon. A file already there is left alone.
        #+end_org """)
        docDir = pathlib.Path(argsList[0]).absolute()
        if not (docDir / "LCNT-INFO").is_dir():
            b_io.eh.problem_usageError(f"{docDir} is not an LCNT document (no LCNT-INFO)")
            return failed(cmndOutcome)
        audioDir = docDir / "audio"
        audioDir.mkdir(exist_ok=True)
        for name, text, mode in ((info.spcsName, info.spcsTemplate, 0o775),
                                 (".gitignore", info.gitignoreTemplate, 0o664),
                                 (info.lexiconName, info.lexiconTemplate, 0o664)):
            target = audioDir / name
            if target.exists():
                print(f"{target} -- in place")
                continue
            target.write_text(text)
            target.chmod(mode)
            print(f"{target} -- planted")
        return cmndOutcome.set(opError=b.OpError.Success, opResults=None)


def examples_csu(planted: bool = True) -> None:
    """ The menu of audioProc.spcs (planted), or of the seed itself (how to plant). """
    cmnd = cs.examples.cmndEnter
    literal = cs.examples.execInsert
    if not planted:
        cs.examples.menuChapter('*Plant audio/ in an LCNT document*')
        cmnd('audioPlant', args=".", comment=" # in the document's directory: audio/audioProc.spcs, .gitignore, ttsLexicon")
        return
    cs.examples.menuChapter('*Narration (the pnote of each frame)*')
    cmnd('narrationList', comment=" # frames, words, estimated time")
    cmnd('narrationText', args="<label>", comment=" # what tts speaks for one frame")
    literal("emacs ttsLexicon   # term = how to say it")
    cs.examples.menuChapter('*Text-to-speech: tts-<label>.**')
    cmnd('ttsGenerate', comment=" # changed frames only; links frames that play nothing")
    cmnd('ttsGenerate', args="<label>", comment=" # one frame")
    cmnd('ttsClean', comment=" # delete all that ttsGenerate makes again; recordings are kept")
    cmnd('ttsClean', args="<label>", comment=" # one frame's tts and its links")
    cs.examples.menuChapter('*Recordings: rec-<label>.**')
    cmnd('recordCmnds', comment=" # audacity commands, one per frame")
    cmnd('recFinalize', comment=" # wav -> mp3, .length, .textHash")
    cs.examples.menuChapter('*What plays: <label>.mp3 -> rec- or tts-*')
    cmnd('audioSelect', args="rec", comment=" # recordings where there are some, tts elsewhere")
    cmnd('audioSelect', args="tts", comment=" # tts everywhere")
    cmnd('audioSelect', args="rec <label>", comment=" # one frame")
    cmnd('audioReport', comment=" # per frame: plays, tts, rec, stale; total time")
    literal("ls -l *.mp3")


####+BEGIN: b:py3:cs:framework/endOfFile :basedOn "classification"
""" #+begin_org
* [[elisp:(org-cycle)][| *End-Of-Editable-Text* |]] :: emacs and org variables and control parameters
#+end_org """

#+STARTUP: showall

### local variables:
### no-byte-compile: t
### end:
####+END:
