from importlib import import_module


def smart_import(name):
    components = name.split('.')
    mod = import_module(".".join(components[0:-1]))
    mod = getattr(mod, components[-1])
    return mod
