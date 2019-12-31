import os
import sys
import logging

from send2trash import send2trash

log = logging.getLogger(__name__)

def main(top_path, *, dry_run=False):
  """
    Deletes empty folders under top_path
  """
  del_dirs = []
  for root, dirs, files in os.walk(top_path):
    if len(dirs) == 0 and len(files) <= 1:
      if not files or files == [".picasa.ini"]:
        del_dirs.append(root)

    dirs[:] = [dirname for dirname in dirs if not dirname.startswith(".")]

  for dir in del_dirs:
    log.info("deleting", dir, "...")
    if not dry_run:
      send2trash(dir)

if __name__ == "__main__":
  if len(sys.argv)==1:
    print(f"delete_empty_folders [--dry-run] path/to/top/folder")
    exit(1)
  
  top = sys.argv[-1]
  ops = sys.argv[1:-1]
  main(top, dry_run="--dry-run" in ops)
