
def open(name, maxver=10, extra=()):
    return _Mod()


def libc():
    return _Mod()


class _Mod():
    def func(self, ret_type, name, arg_types):
        return _universal_func


def _universal_func(*args, **kwargs):
    pass
