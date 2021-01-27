#!/usr/bin/env python3

# bake_all.py
# Bake all .odoc files into .html ones, preserving folder structure.

import os
import odoc
import shutil
from os.path import join

# In the future we can probably calculate changes based on hashes and file
# lists and such, but for now, we can make things in the blink of an eye,
# let's just remake it.
if os.path.exists("html_baked"):
    shutil.rmtree("html_baked")
    os.mkdir("html_baked")

for root,dirs,files in os.walk("docs"):
    baked_root = root.replace("docs", "html_baked")
    for dir in dirs:
        print(baked_root)
        path = join(baked_root, dir)
        # if os.path.exists(path):
        #     continue
        print(path)
        os.makedirs(path)

    for file_name in files:
        with open(join(root, file_name), "r") as file:
            html = odoc.to_html(file.read())
        with open(join(baked_root, file_name.replace(".odoc", ".html")), "w") as file:
            file.write(html)
