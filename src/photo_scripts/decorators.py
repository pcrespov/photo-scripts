import functools
import logging
from collections import Counter, namedtuple
from copy import deepcopy

log = logging.getLogger(__name__)

def func_runner(func, *args, dry_run=False, extra_msg="", **kargs):
  if dry_run:
    print(f"Would run {func.__name__}", extra_msg)
    res = None
  else:
    log.debug("Running %s %s", func.__name__, extra_msg)
    res = func(*args, **kargs)
  return res

def dry_runnable(msg):
  def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kargs):
      dry_run = kargs.pop('dry_run', False)
      result = func_runner(func, args, kargs, dry_run=dry_run)
      return result
    return wrapper
  return decorator


_CounterInfo = namedtuple("CountCalls", "total success failed")

def count_calls(func):
  total = 0
  success = 0
  failed = 0

  @functools.wraps(func)
  def wrapper(*args, **kargs):
    nonlocal total, success, failed
    try:
      total += 1
      result = func(*args, **kargs)
      success +=1
    except:
      failed += 1
      raise
    return result

  def counts():
    return _CounterInfo(total, success, failed)

  wrapper.counts = counts

  return wrapper
