# -*- coding: utf-8 -*-
""" #+begin_org
* ~[Summary]~ :: The library of an LCNT document's audio/ directory (audioProc.spcs, seed lcntAudio-seed.cs):
the frames and their narration (pnote), text-to-speech into tts-<label>.*, recordings as rec-<label>.*, and
the selection of what plays as relative symlinks <label>.mp3 and <label>.length. No side effects at import.
#+end_org """

if 'csInfo' not in globals(): import typing ; csInfo: typing.Dict[str, typing.Any] = { 'moduleName': ['loadAs'], }
csInfo['version'] = '202611170001'
csInfo['status']  = 'inDev'

import dataclasses
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
import typing

from bisos.csSeed import seedsLib

from bisos.lcnt import lcntTtsInfo

#
# Decided with the user, 2026-11-17 (aiActivity_EmacsConf26 AI-WorkPlan.org 3.2):
#   - A frame's full narration is its pnote. Reveal plays audio/<label>.mp3 (frameaudio -> data-audio-src);
#     the player stays as it is.
#   - Two sources per frame side by side: tts-<label>.{mp3,length,textHash} (written by ttsGenerate, always)
#     and rec-<label>.{wav,mp3,length,textHash} (the author's recording). What plays is a relative symlink
#     <label>.mp3 -> <source>-<label>.mp3, with <label>.length beside it. Switching is relinking.
#   - <source>-<label>.textHash: the first word is the hash of the narration the audio was made from, so a
#     recording older than its narration is reported stale. The tts line also names voice, engine and the
#     spoken text, and ttsGenerate redoes a frame when any of these change.
#   - .length is in milliseconds, one value with no newline (as mmUniteAudio.sh and impressive read it).
#

sources = ("rec", "tts")
spcsName = "audioProc.spcs"
seedName = "lcntAudio-seed.cs"
lexiconName = "ttsLexicon"
wordsPerMinute = 140          # for estimates only, before any audio exists
sentenceSilence = "0.3"       # seconds after each sentence (piper)


@dataclasses.dataclass
class LcntAudioSeedInfo:
    """ The singleton audioProc.spcs fills with setup(). """
    docSrc: typing.Optional[str] = None     # the document source; None: the docSrc file-var of ../curBuild
    voice: typing.Optional[str] = None      # one of lcntTtsInfo.voices; None: lcntTtsInfo.defaultVoice

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


lcntAudioSeedInfo = LcntAudioSeedInfo()


def setup(
        docSrc: typing.Optional[str] = None,
        voice: typing.Optional[str] = None,
) -> None:
    lcntAudioSeedInfo.docSrc = docSrc
    lcntAudioSeedInfo.voice = voice


@dataclasses.dataclass
class AudioParams:
    audioDir: pathlib.Path
    docDir: pathlib.Path
    docSrc: pathlib.Path
    voice: str


def paramsFromPlantPath(plantPath: typing.Optional[str] = None) -> AudioParams:
    """ The audio directory is that of the planted audioProc.spcs (by the path it is planted at, not its
    target), and the document is its parent. """
    if plantPath is None:
        plantPath = seedsLib.seededCsxuInfo.plantOfThisSeed
    if plantPath is None:
        raise ValueError(f"not planted: run this as <docDir>/audio/{spcsName}")
    audioDir = pathlib.Path(plantPath).absolute().parent
    docDir = audioDir.parent
    docSrc = lcntAudioSeedInfo.docSrc or curBuildDocSrc(docDir)
    if not docSrc:
        raise ValueError(f"no document source: {docDir}/curBuild/docSrc is missing; or give setup(docSrc=...)")
    voice = lcntAudioSeedInfo.voice or lcntTtsInfo.defaultVoice
    lcntTtsInfo.voiceNamed(voice)
    return AudioParams(audioDir=audioDir, docDir=docDir, docSrc=docDir / docSrc, voice=voice)


def curBuildDocSrc(docDir: pathlib.Path) -> typing.Optional[str]:
    try:
        lines = (docDir / "curBuild" / "docSrc").read_text().split()
    except OSError:
        return None
    return lines[0] if lines else None


#
# The frames and their narration
#

_inputRe = re.compile(r"\\input\{([^}]+)\}")
_tokenRe = re.compile(r"\\begin\{frame\}\[[^\]]*label=([A-Za-z0-9_:-]+)|\\pnote\{")


def _uncommented(text: str) -> str:
    """ TeX comments dropped: from an unescaped % to the end of its line. """
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.split("\n"))


def sourceExpanded(src: pathlib.Path, depth: int = 0) -> str:
    """ The document source with its input files inlined, comments dropped. """
    text = _uncommented(src.read_text())
    if depth > 8:
        return text

    def inline(match: re.Match) -> str:
        name = match.group(1).strip()
        path = (src.parent / name)
        if not path.suffix:
            path = path.with_suffix(".tex")
        return sourceExpanded(path, depth + 1) if path.is_file() else ""
    return _inputRe.sub(inline, text)


def _braced(text: str, start: int) -> typing.Tuple[str, int]:
    """ The content of the group whose { is just before start, and the index after its closing }. """
    level = 1
    i = start
    while i < len(text) and level:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            level += 1
        elif c == "}":
            level -= 1
        i += 1
    return text[start:i - 1], i


@dataclasses.dataclass
class Frame:
    label: str
    narration: str          # spoken text, before the lexicon

    @property
    def words(self) -> int:
        return len(self.narration.split())

    @property
    def narrationHash(self) -> str:
        return hashlib.sha256(self.narration.encode()).hexdigest()[:16]


def framesOf(src: pathlib.Path) -> typing.List[Frame]:
    """ Every labelled frame in document order (each label once), with the text of the pnotes that follow it
    up to the next frame. A frame appears twice in the source (htmlonly and verblatex); its pnote is in one. """
    text = sourceExpanded(src)
    frames: typing.Dict[str, typing.List[str]] = {}
    current = None
    pos = 0
    while True:
        match = _tokenRe.search(text, pos)
        if match is None:
            break
        if match.group(1):
            current = match.group(1)
            frames.setdefault(current, [])
            pos = match.end()
        else:
            body, pos = _braced(text, match.end())
            if current is not None:
                frames[current].append(body)
    return [Frame(label, spoken(" \n\n ".join(bodies))) for label, bodies in frames.items()]


def spoken(tex: str) -> str:
    """ TeX of a pnote as plain text to speak: one paragraph per line. """
    t = tex.replace("\\\\", " ").replace("~", " ")
    t = t.replace("---", ", ").replace("--", ", ")
    t = t.replace("\\&", "and").replace("\\%", " percent").replace("\\$", "$").replace("\\_", "_")
    for _ in range(4):                                       # \cmd{x} -> x, innermost first
        t = re.sub(r"\\[A-Za-z]+\*?\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\[A-Za-z]+\*?", " ", t)
    t = t.replace("{", "").replace("}", "")
    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", t)]
    return "\n".join(p for p in paragraphs if p)


#
# Pronunciation
#

def lexiconOf(audioDir: pathlib.Path) -> typing.List[typing.Tuple[str, str]]:
    """ audio/ttsLexicon: lines "term = spoken"; # starts a comment. Whole words, case-sensitive. """
    try:
        lines = (audioDir / lexiconName).read_text().splitlines()
    except OSError:
        return []
    pairs = []
    for line in lines:
        line = line.split("#", 1)[0]
        if "=" in line:
            term, say = (part.strip() for part in line.split("=", 1))
            if term:
                pairs.append((term, say))
    return pairs


def lexiconApplied(text: str, lexicon: typing.List[typing.Tuple[str, str]]) -> str:
    for term, say in lexicon:
        text = re.sub(rf"(?<![\w.-]){re.escape(term)}(?![\w-])", say, text)
    return text


#
# The files of a frame
#

def path(audioDir: pathlib.Path, source: typing.Optional[str], label: str, ext: str) -> pathlib.Path:
    """ <source>-<label>.<ext>, or the played <label>.<ext> when source is None. """
    return audioDir / (f"{source}-{label}.{ext}" if source else f"{label}.{ext}")


def readWords(p: pathlib.Path) -> typing.List[str]:
    try:
        return p.read_text().split()
    except OSError:
        return []


def lengthMs(p: pathlib.Path) -> typing.Optional[int]:
    try:
        return int(p.read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def probeMs(audio: pathlib.Path) -> typing.Optional[int]:
    """ The duration of an audio file in milliseconds (ffprobe). """
    run = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(audio)],
        capture_output=True, text=True, check=False)
    try:
        return round(float(json.loads(run.stdout)["format"]["duration"]) * 1000)
    except (ValueError, KeyError, TypeError):
        return None


def writeText(p: pathlib.Path, text: str) -> None:
    """ Written beside, then moved into place. """
    tmp = p.with_name(f".{p.name}.tmp")
    tmp.write_text(text)
    os.replace(tmp, p)


def ttsKey(frame: Frame, spokenText: str, voice: str) -> str:
    """ The tts .textHash line: narration hash first (as for a recording), then what else made the audio. """
    spokenHash = hashlib.sha256(spokenText.encode()).hexdigest()[:16]
    return f"{frame.narrationHash} {voice} piper-{lcntTtsInfo.piperVersion} spoken-{spokenHash}"


def mp3FromWav(wav: pathlib.Path, mp3: pathlib.Path) -> typing.Optional[str]:
    """ None, or why not. Written beside, then moved into place. """
    tmp = mp3.with_name(f".{mp3.stem}.tmp.mp3")
    run = subprocess.run(
        ["ffmpeg", "-loglevel", "error", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-qscale:a", "4", str(tmp)],
        capture_output=True, text=True, check=False)
    if run.returncode != 0:
        tmp.unlink(missing_ok=True)
        return f"ffmpeg: {run.stderr.strip()}"
    os.replace(tmp, mp3)
    return None


def ttsGenerateOne(audioDir: pathlib.Path, frame: Frame, voice: str,
                   lexicon: typing.List[typing.Tuple[str, str]]) -> typing.Tuple[str, typing.Optional[str]]:
    """ ("unchanged" | "generated" | "skipped" | "failed", detail). Redone only when the .textHash line differs
    or a file is missing. """
    if not frame.narration:
        return "skipped", "no narration"
    spokenText = lexiconApplied(frame.narration, lexicon)
    key = ttsKey(frame, spokenText, voice)
    mp3 = path(audioDir, "tts", frame.label, "mp3")
    length = path(audioDir, "tts", frame.label, "length")
    hashFile = path(audioDir, "tts", frame.label, "textHash")
    if mp3.is_file() and length.is_file() and " ".join(readWords(hashFile)) == key:
        return "unchanged", None
    if not lcntTtsInfo.piperPresent():
        return "failed", f"{lcntTtsInfo.piperBin} missing: run piperTts-sbom.pcs -i sbom_fullUpdate"
    voiceSpec = lcntTtsInfo.voiceNamed(voice)
    if not lcntTtsInfo.voicePresent(voiceSpec):
        return "failed", f"voice {voice} missing: run piperTts-sbom.pcs -i sbom_fullUpdate"
    with tempfile.TemporaryDirectory(prefix=".tts-", dir=audioDir) as tmpDir:
        wav = pathlib.Path(tmpDir) / "out.wav"
        run = subprocess.run(
            [str(lcntTtsInfo.piperBin), "-m", str(voiceSpec.onnxPath), "-f", str(wav),
             "--sentence-silence", sentenceSilence],
            input=spokenText, capture_output=True, text=True, check=False)
        if run.returncode != 0 or not wav.is_file():
            return "failed", f"piper: {run.stderr.strip()[-300:]}"
        reason = mp3FromWav(wav, mp3)
        if reason:
            return "failed", reason
    ms = probeMs(mp3)
    if ms is None:
        return "failed", f"no duration for {mp3.name}"
    writeText(length, str(ms))
    writeText(hashFile, key + "\n")
    return "generated", f"{ms / 1000:.1f}s"


def recFinalizeOne(audioDir: pathlib.Path, frame: Frame) -> typing.Tuple[str, typing.Optional[str]]:
    """ rec-<label>.wav (if newer) into .mp3, then .length, and .textHash as the narration now. """
    wav = path(audioDir, "rec", frame.label, "wav")
    mp3 = path(audioDir, "rec", frame.label, "mp3")
    if wav.is_file() and (not mp3.is_file() or wav.stat().st_mtime > mp3.stat().st_mtime):
        reason = mp3FromWav(wav, mp3)
        if reason:
            return "failed", reason
    elif not mp3.is_file():
        return "skipped", "no recording"
    ms = probeMs(mp3)
    if ms is None:
        return "failed", f"no duration for {mp3.name}"
    writeText(path(audioDir, "rec", frame.label, "length"), str(ms))
    writeText(path(audioDir, "rec", frame.label, "textHash"), frame.narrationHash + "\n")
    return "finalized", f"{ms / 1000:.1f}s"


def has(audioDir: pathlib.Path, source: str, label: str) -> bool:
    return path(audioDir, source, label, "mp3").is_file() and path(audioDir, source, label, "length").is_file()


def isStale(audioDir: pathlib.Path, source: str, frame: Frame) -> bool:
    words = readWords(path(audioDir, source, frame.label, "textHash"))
    return bool(words) and words[0] != frame.narrationHash


def playing(audioDir: pathlib.Path, label: str) -> str:
    """ What <label>.mp3 is: a source name, "none", "dangling", "file" (not a link: left alone) or "other". """
    played = path(audioDir, None, label, "mp3")
    if not played.is_symlink():
        return "file" if played.exists() else "none"
    target = os.readlink(played)
    if not played.exists():
        return "dangling"
    for source in sources:
        if target == f"{source}-{label}.mp3":
            return source
    return "other"


def _relink(link: pathlib.Path, target: str) -> None:
    """ link -> target (relative), replaced in one step. """
    tmp = link.with_name(f".{link.name}.lnk")
    tmp.unlink(missing_ok=True)
    os.symlink(target, tmp)
    os.replace(tmp, link)


def select(audioDir: pathlib.Path, label: str, source: str) -> typing.Optional[str]:
    """ <label>.mp3 and <label>.length -> <source>-<label>.*. None, or why not. """
    if not has(audioDir, source, label):
        return f"no {source}-{label}.mp3 with its .length"
    for ext in ("mp3", "length"):
        link = path(audioDir, None, label, ext)
        if link.exists() and not link.is_symlink():
            return f"{link.name} is a file, not a link: left alone"
    for ext in ("mp3", "length"):
        _relink(path(audioDir, None, label, ext), f"{source}-{label}.{ext}")
    return None


def preferred(audioDir: pathlib.Path, label: str, prefer: str) -> typing.Optional[str]:
    """ prefer if it is there, else the other source, else None. """
    for source in (prefer,) + tuple(s for s in sources if s != prefer):
        if has(audioDir, source, label):
            return source
    return None


def ttsCleanPaths(audioDir: pathlib.Path,
                  labels: typing.Optional[typing.List[str]] = None) -> typing.List[pathlib.Path]:
    """ What ttsGenerate can make again: tts-<label>.*, the links to them, dangling links, leftovers of an
    interrupted run, __pycache__. Never rec-* (a recording's .textHash says which narration it was made
    from), the links to them, or the planted files. With labels, only those frames' tts and links. """
    found: typing.List[pathlib.Path] = []
    if labels is None:
        found += sorted(audioDir.glob("tts-*"))
        for each in sorted(audioDir.iterdir()):
            if each.is_symlink() and (not each.exists() or os.readlink(each).startswith("tts-")):
                found.append(each)
        found += sorted(audioDir.glob(".*.tmp*")) + sorted(audioDir.glob(".*.lnk")) + sorted(audioDir.glob(".tts-*"))
        if (audioDir / "__pycache__").is_dir():
            found.append(audioDir / "__pycache__")
    else:
        for label in labels:
            for ext in ("mp3", "length", "textHash"):
                if path(audioDir, "tts", label, ext).exists():
                    found.append(path(audioDir, "tts", label, ext))
            for ext in ("mp3", "length"):
                link = path(audioDir, None, label, ext)
                if link.is_symlink() and os.readlink(link).startswith("tts-"):
                    found.append(link)
    return found


def remove(p: pathlib.Path) -> None:
    if p.is_dir() and not p.is_symlink():
        shutil.rmtree(p)
    else:
        p.unlink()


#
# Planting
#

spcsTemplate = '''#!/usr/bin/env python

""" #+begin_org
* audioProc.spcs --- the audio of this LCNT document (the parent directory).
* tts-<label>.* are written by ttsGenerate, rec-<label>.* are your recordings, and
* <label>.mp3 / <label>.length (what Reveal plays) are links selected with audioSelect.
#+end_org """

from bisos.lcnt import lcntAudio_seed  # noqa: F401  _atExit_

from bisos.lcnt import lcntAudio_seedInfo
lcntAudio_seedInfo.setup(
    docSrc=None,      # None: the docSrc of ../curBuild
    voice=None,       # None: the default voice of lcntTtsInfo
)
'''

gitignoreTemplate = """# Audio is regenerated (tts-) or kept elsewhere (rec-); the links say what plays.
*.mp3
*.wav
*.length
*.textHash
.*.tmp*
.tts-*
__pycache__/
"""

lexiconTemplate = """# term = how to say it  (whole words, case-sensitive; applied to tts only)
# LCNT = L C N T
"""
