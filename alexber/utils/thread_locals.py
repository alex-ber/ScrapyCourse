import threading


#inspired by https://stackoverflow.com/questions/1408171/thread-local-storage-in-python
thread_locals = threading.local()

#TODO: Alex add tests

def threadlocal_var(varname, factory, *args, **kwargs):
  v = getattr(thread_locals, varname, None)
  if v is None:
    v = factory(*args, **kwargs)
    setattr(thread_locals, varname, v)
  return v

def get_threadlocal_var(varname):
    v = threadlocal_var(varname, lambda : None)
    if v is None:
        raise ValueError(f"threadlocal's {varname} is not initilized")
    return v

def del_threadlocal_var(varname):
    try:
        delattr(thread_locals, varname)
    except AttributeError:
        pass