# -*- coding: utf-8 -*-
""" #+begin_org
* ~[Summary]~ :: The single source of facts of LCNT's text-to-speech: the Piper engine, its isolated venv
and its hash-pinned set, and the voices LCNT may use. Pure: no side effects at import.
#+end_org """

import dataclasses
import hashlib
import os
import pathlib
import typing

#
# Decided with the user, 2026-11-17 (aiActivity_EmacsConf26 AI-WorkPlan.org, Stage 3):
#   - Piper (OHF-Voice/piper1-gpl, GPL-3.0-or-later), not Kokoro: long-term maintenance (the Open Home
#     Foundation; Home Assistant depends on it), a small runtime (onnxruntime), and voices whose
#     provenance can be stated. Kokoro-82M's training data includes synthetic audio from closed models.
#   - Only voices trained from scratch on public-domain recordings. A voice fine-tuned from another one
#     (most are fine-tuned from lessac, whose Blizzard 2013 data has its own licence) carries that
#     voice's terms: en_US-libritts_r is excluded for this reason.
#   - Not near real time: speed is not a driver.
#

# Piper is an exception to asc, in a venv of its own under /bisos/venv/py3/isolated/: onnxruntime and
# numpy are large binary wheels nothing in asc needs, and the set is pinned as a whole.
venv = pathlib.Path("/bisos/venv/py3/isolated/piperTts")
venvPython = "/usr/bin/python3.13"   # asc's base (asc/pyvenv.cfg)
piperVersion = "1.8.0"

# The whole resolved set of piper-tts 1.8.0 (2026-11-17), each sha256 checked against PyPI's published
# digest. onnxruntime and numpy are binary (CPython 3.13, x86_64): the set is for amd64 + Python 3.13 only.
reqsArch = "amd64"
reqs: typing.Tuple[typing.Tuple[str, str, str], ...] = (
    ("flatbuffers", "25.12.19", "7634f50c427838bb021c2d66a3d1168e9d199b0607e6329399f04846d42e20b4"),
    ("numpy", "2.5.5", "824025655df929268bfe6b47ed91a00d14209a6f760847cf150be446829e1ce4"),
    ("onnxruntime", "1.32.0", "02ea12a28c069ea8510093d95a7f6ff8126bfd9fc5c0d3381c03b80fb2b424ba"),
    ("packaging", "26.3", "d7193f7c8e4e93f444fde0262bf90af30e16fa0ad0ad44cb553c87339b23cd1c"),
    ("pathvalidate", "3.3.1", "5263baab691f8e1af96092fa5137ee17df5bdfbd6cff1fcac4d6ef4bc2e1735f"),
    ("piper-tts", piperVersion, "25b4d3f31ff70c8fa7151908e00aaa5650cbdf16bca8fcf21299f3941b89a7d3"),
    ("protobuf", "7.36.2", "89f23aa53c24553a2416fd4fd1ec06f74fa42b14b546d8883128813f775bbfd2"),
)

piperBin = venv / "bin" / "piper"

# The voices: fetched from the rhasspy/piper-voices repository at one pinned revision, never by name at
# run time. Each file is checked against its sha256 (the .onnx digests are also Hugging Face's LFS oids).
# The MODEL_CARD is kept beside each voice as the record of its data and licence.
voicesRepo = "https://huggingface.co/rhasspy/piper-voices"
voicesRevision = "0ca208afc2a2ee102b1e961e72e0a7e4907be3d0"   # main, 2026-11-17
voicesDir = pathlib.Path("/bisos/var/lcnt/piperVoices")


@dataclasses.dataclass(frozen=True)
class Voice:
    name: str            # e.g. en_US-ljspeech-high: the file names are <name>.onnx and <name>.onnx.json
    repoDir: str         # its directory in voicesRepo
    data: str            # the recordings it was trained on, as its MODEL_CARD says
    onnxSha256: str
    jsonSha256: str
    cardSha256: str

    def files(self) -> typing.List[typing.Tuple[str, str, str]]:
        """(the file's name in voicesDir, its path in voicesRepo, its sha256)"""
        return [
            (f"{self.name}.onnx", f"{self.repoDir}/{self.name}.onnx", self.onnxSha256),
            (f"{self.name}.onnx.json", f"{self.repoDir}/{self.name}.onnx.json", self.jsonSha256),
            (f"{self.name}.MODEL_CARD", f"{self.repoDir}/MODEL_CARD", self.cardSha256),
        ]

    @property
    def onnxPath(self) -> pathlib.Path:
        return voicesDir / f"{self.name}.onnx"


# All four: trained from scratch, on public-domain recordings (MODEL_CARDs read 2026-11-17).
voices: typing.Tuple[Voice, ...] = (
    Voice("en_US-ljspeech-high", "en/en_US/ljspeech/high", "LJ Speech (LibriVox), public domain",
          "5d4f08ba6a2a48c44592eed3ce56bf85e9de3dd4e20df90541ae68a8310c029a",
          "7e1f4634af596d83cca997fb7a931ba80b70f8a316a2655ee69c55365e0ace14",
          "289f7421072d689a3d91f6c632f486af46f9b8b04417536104a4ea667b8a394b"),
    Voice("en_GB-cori-high", "en/en_GB/cori/high", "LibriVox, public domain",
          "470b4dd634c98f8a4850d7626ffc3dfc90774628eeef6605a6dd8f88f30a5903",
          "9e7fb5b5671612c22f3c81cbe46c1ae87b031a4632bcb509e499dad6f1e2adec",
          "136e7bd168b6c35b4a5df01a0253297e5773b5775ceae0af5160f264aa58208f"),
    Voice("en_US-norman-medium", "en/en_US/norman/medium", "LibriVox, public domain",
          "b9739443232a80a59c7d18810dd856899bf16a7964725f5ab81ea49b1351cb71",
          "6c2db7f558a4a8deb9fe822583c1c5105f6c4e834dd0f9de8ad17a888ee9fe1d",
          "60eaf4d10009d1bd4a1aa555d337dae00f60421d72fee415b9139a021e7cb5d0"),
    Voice("en_US-kristin-medium", "en/en_US/kristin/medium", "LibriVox, public domain",
          "5849957f929cbf720c258f8458692d6103fff2f0e3d3b19c8259474bb06a18d4",
          "5681426d4aead22195de70531eeeeddb46493cfaffc5764b2ea3db73428b651c",
          "8c181b1d5f7d8152b914faab941fcbe6b8f0495e63e5189d6f27b8c68c8393fc"),
)

defaultVoice = "en_US-ljspeech-high"


def voiceNamed(name: str) -> Voice:
    for each in voices:
        if each.name == name:
            return each
    raise ValueError(f"{name} is not one of the allowed voices: {[each.name for each in voices]}")


def reqsContent() -> str:
    """The hashed requirements file of Piper's isolated venv."""
    return "".join(f"{n}=={v} --hash=sha256:{h}\n" for n, v, h in reqs)


def venvSetupScript() -> str:
    """Bash: the isolated venv, created once, then the hashed set installed into it. Idempotent.

    pip --require-hashes --no-deps: every file is checked against its pinned sha256, and nothing outside
    the set is pulled in. Satisfied pins are a no-op; a bumped set is applied. Refused on an architecture
    the hashes do not cover. (As bisos.devpi's isolatedVenvSetupScript.)
    """
    return f"""
set -e
a=$(dpkg --print-architecture)
[ "$a" = "{reqsArch}" ] || {{ echo "{venv.name}: hashed set covers {reqsArch} only, not $a" >&2; exit 1; }}
if [ ! -x {venv}/bin/pip ] ; then
    mkdir -p {venv.parent}
    {venvPython} -m venv {venv}
fi
reqs=$(mktemp)
trap 'rm -f "$reqs"' EXIT
cat > "$reqs" <<'ISOLATED_REQS_EOF'
{reqsContent()}ISOLATED_REQS_EOF
{venv}/bin/pip install --quiet --disable-pip-version-check --require-hashes --no-deps -r "$reqs"
{venv}/bin/pip check
"""


def voiceFetchScript(voice: Voice) -> str:
    """Bash: the files of one voice into voicesDir at voicesRevision, each checked. Idempotent.

    A file already there with the right sha256 is left alone; a download is checked before it is moved
    into place, so a bad or changed file never lands.
    """
    lines = ["set -e", f"mkdir -p {voicesDir}"]
    for fileName, repoPath, sha in voice.files():
        dest = voicesDir / fileName
        url = f"{voicesRepo}/resolve/{voicesRevision}/{repoPath}"
        lines.append(f"""
if echo "{sha}  {dest}" | sha256sum --check --status 2>/dev/null ; then
    echo "{fileName} -- in place"
else
    tmp=$(mktemp {voicesDir}/.fetch.XXXXXX)
    curl -fsSL -o "$tmp" {url}
    if echo "{sha}  $tmp" | sha256sum --check --status ; then
        chmod 644 "$tmp"
        mv "$tmp" {dest}
        echo "{fileName} -- fetched"
    else
        rm -f "$tmp"
        echo "{fileName}: sha256 differs from the pin; not installed" >&2
        exit 1
    fi
fi""")
    return "\n".join(lines) + "\n"


def fileSha256(path: pathlib.Path) -> typing.Optional[str]:
    try:
        digest = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def voicePresent(voice: Voice) -> bool:
    """Every file of the voice is in voicesDir with its pinned sha256."""
    return all(fileSha256(voicesDir / fileName) == sha for fileName, _, sha in voice.files())


def piperPresent() -> bool:
    return os.access(piperBin, os.X_OK)
