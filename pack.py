"""Packer main"""
import sys
import os
from pathlib import Path

from functions import zipdir, ziptob64, genunpackfile, gencompressedunpackfile

if len(sys.argv)<2:
    print("usage: {} <directory-for-pack>".format(sys.argv[0]))
    sys.exit(1)
dir_to_pack=sys.argv[1]
if not dir_to_pack.endswith("/"):
    dir_to_pack+="/"

dtp=Path(dir_to_pack)
if not dtp.exists():
    print("directory {} don't exists".format(dir_to_pack))

p=Path("dist")
if not p.exists():
    os.mkdir("dist")

dtb_name=os.path.dirname(dir_to_pack)
zipdir(dir_to_pack, f"dist/{dtb_name}.zip")
ziptob64(f"dist/{dtb_name}.zip", f"dist/{dtb_name}.zip.base64")
genunpackfile(f"dist/{dtb_name}.py", f"dist/{dtb_name}.zip.base64")
gencompressedunpackfile(f"dist/{dtb_name}.compressed.py", f"dist/{dtb_name}.py")
