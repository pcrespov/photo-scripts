

import hashlib
import os
import re
import sys
from send2trash import send2trash

from decorators import count_calls, func_runner

# Like 
DUPLICATE_PATTERN = re.compile(r"(.+)\s*\(\d\)")
PATTERN = re.compile(r"(.+)\s*(\(\d\)|copia|-\d{3})")


def eval_image_hash(image_path):
  ''' Evaluates hash of a given image file'''
  image_hash = None
  with open(image_path) as fh:
    image_file = fh.read()
    image_hash = hashlib.md5(image_file).hexdigest()
  return image_hash


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

def process_duplicates(top_path, *, dry_run=False):

  for root, dirs, files in os.walk(top_path):
    for filename in files:
      name, ext = os.path.splitext(filename)
      for suffix in [' (2)', '-001', ' - copia']:
        if filename.endswith(suffix + ext):
          suffixless = name[:-len(suffix)] + ext # without suffix
          # print good, name
          original = os.path.join(root, suffixless)
          duplicate = os.path.join(root, filename)

          if os.path.exists(original):
            if os.stat(duplicate).st_size == os.stat(original).st_size:
              delete_file(duplicate, dry_run)
          else:
            rename_file(duplicate, original, dry_run)

    dirs[:] = [ dirname for dirname in dirs if not dirname.startswith(".") ]


if __name__ == "__main__":
  if len(sys.argv) == 1:
    print("delete_duplicates [--dry-run] path/to/top/folder")
    exit(1)

  top = sys.argv[-1]
  ops = sys.argv[1:-1]
  process_duplicates(top, dry_run="--dry-run" in ops)

  print("Deleted", delete_file.counts())
  print("Renamed", rename_file.counts())
