

import hashlib
import logging
import os
import re
import sys

from send2trash import send2trash

from decorators import count_calls, func_runner

log = logging.getLogger(__name__)

# Copies are names using the following pattern 
PATTERN = re.compile(r"(\(\d\)|copia|copy|-\d{3})\s*\.\w{3,4}$")

def eval_image_hash(image_path):
  ''' Evaluates hash of a given image file'''
  image_hash = None
  with open(image_path) as fh:
    image_file = fh.read()
    image_hash = hashlib.md5(image_file).hexdigest()
  return image_hash

def search_pattern(top):
  for root, dirs, files in os.walk(top):
    for name in files:
      m = PATTERN.search(name)
      if m:
        _, ext = os.path.splitext(name)
        renamed = name[0:m.start()].strip() + ext

        duplicate = os.path.join(root, name)
        original = os.path.join(root, renamed)
        
        yield original, duplicate

        log.debug("%s --> %s", os.path.join(root,name), renamed)
    dirs[:] = [dirname for dirname in dirs if not dirname.startswith(".")]

@count_calls
def delete_file(file_path, dry_run):
  func_runner(send2trash, file_path,
              dry_run=dry_run, 
              extra_msg=f"{os.path.basename(file_path)} ...")

@count_calls
def rename_file(from_path, to_path, dry_run):
  func_runner(os.rename, from_path, to_path,
              dry_run=dry_run,
              extra_msg=f"{os.path.basename(from_path)} -> {os.path.basename(to_path)} ...")

def main(top_path, *, dry_run=False):
  """
    Deletes or renames files found as duplicates under top_path
  """
  for original, duplicate in search_pattern(top_path):
    if os.path.exists(original):
      if os.stat(duplicate).st_size == os.stat(original).st_size:
          delete_file(duplicate, dry_run)
    else:
      rename_file(duplicate, original, dry_run)

  log.info("Deleted", delete_file.counts())
  log.info("Renamed", rename_file.counts())


if __name__ == "__main__":
  if len(sys.argv) == 1:
    print("delete_duplicates [--dry-run] path/to/top/folder")
    exit(1)

  top = sys.argv[-1]
  ops = sys.argv[1:-1]
  main(top, dry_run="--dry-run" in ops)
  #search_pattern(top)
