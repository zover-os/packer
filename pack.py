"""Packer main"""
import sys
import os
from pathlib import Path

from functions import zipdir, ziptob64, genunpackfile, gencompressedunpackfile

if len(sys.argv)<2:
    print(f"usage: {sys.argv[0]} <directory-for-pack>")
    sys.exit(1)

if not sys.argv[1].endswith("/"):
    sys.argv[1]+="/"

dirPack=Path(sys.argv[1])
if not dirPack.exists():
    print(f"directory {sys.argv[1]} don't exists")

dist=Path("dist")
if not dist.exists():
    os.mkdir("dist")

dirPackName=os.path.dirname(sys.argv[1])
zipdir(sys.argv[1], f"dist/{dirPackName}.zip")
ziptob64(f"dist/{dirPackName}.zip", f"dist/{dirPackName}.zip.base64")
genunpackfile(f"dist/{dirPackName}.py", f"dist/{dirPackName}.zip.base64")
gencompressedunpackfile(f"dist/{dirPackName}.compressed.py", f"dist/{dirPackName}.py")
