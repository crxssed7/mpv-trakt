import os
import re
import urllib.parse

def clean_file_name(file_path):
    basename = os.path.basename(file_path)
    name_without_ext, _ = os.path.splitext(basename)
    decoded = urllib.parse.unquote(name_without_ext)
    without_brackets = re.sub(r"\[.*?\]", "", decoded)
    return without_brackets.strip()
