

import hashlib
import os
import re
import sys
from functools import wraps, lru_cache
from send2trash import send2trash

# Like 
DUPLICATE_PATTERN = re.compile(r"(.+)\s*\(\d\)")
PATTERN = re.compile(r"(.+)\s*(\(\d\)|copia|-\d{3})")


def count_calls(func):
  calls_count = 0
  success_count = 0
  failed_count = 0

  @wraps(func)
  def wrapper(*args, **kargs):
    nonlocal calls_count, success_count, failed_count
    try:
      calls_count +=1
      result = func(*args, **kargs)
      success_count +=1
    except:
      failed_count+=1
      raise
    return result

  def counts():
    return success_count, failed_count, calls_count

  wrapper.counts = counts

  return wrapper


def eval_image_hash(image_path):
  ''' Evaluates hash of a given image file'''
  image_hash = None
  with open(image_path) as fh:
    image_file = fh.read()
    image_hash = hashlib.md5(image_file).hexdigest()
  return image_hash


@count_calls
def delete_file(path, dry_run):
  msg = "Would delete" if dry_run else "Deleting"
  print(msg, os.path.basename(path), "...")
  if not dry_run:
    send2trash(duplicate)

def process_duplicates(top_path, *, dry_run=False):
  num_hits = 0
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
            msg = "Would rename" if dry_run else "Renaming"
            print(msg, os.path.basename(
                duplicate), "->", os.path.basename(original))
            if not dry_run:
              os.rename(duplicate, original)

    dirs[:] = [ dirname for dirname in dirs if not dirname.startswith(".") ]


if __name__ == "__main__":
  if len(sys.argv) == 1:
    print("delete_duplicates [--dry-run] path/to/top/folder")
    exit(1)

  top = sys.argv[-1]
  ops = sys.argv[1:-1]
  process_duplicates(top, dry_run="--dry-run" in ops)

  print("Deleted", delete_file.counts())
