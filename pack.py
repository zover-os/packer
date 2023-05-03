"""Packer main"""
import sys
import os
from pathlib import Path

from functions import zipdir, ziptob64, genunpackfile, gencompressedunpackfile

if len(sys.argv)<2:
    print(f"usage: {sys.argv[0]} <directory-for-pack>")
    sys.exit(1)
dirPackStr=sys.argv[1]
if not dirPackStr.endswith("/"):
    dirPackStr+="/"

dirPack=Path(dirPackStr)
if not dirPack.exists():
    print("directory {} don't exists".format(dirPackStr))

dist=Path("dist")
if not dist.exists():
    os.mkdir("dist")

dirPackName=os.path.dirname(dirPack)
zipdir(dirPackStr, f"dist/{dirPackName}.zip")
ziptob64(f"dist/{dirPackName}.zip", f"dist/{dirPackName}.zip.base64")
genunpackfile(f"dist/{dirPackName}.py", f"dist/{dirPackName}.zip.base64")
gencompressedunpackfile(f"dist/{dirPackName}.compressed.py", f"dist/{dirPackName}.py")
