import re
import pystache


def named_value(d):
    return next(iter(d.items()))


def ensure_keys(dict_obj, *keys):
    if len(keys) == 0:
        return dict_obj
    else:
        first, rest = keys[0], keys[1:]
        if first not in dict_obj:
            dict_obj[first] = {}
        dict_obj[first] = ensure_keys(dict_obj[first], *rest)
        return dict_obj


def camel_case_to_underscore(name):
    """
    Converts name from CamelCase to snake_case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def pystache_render(*args, **kwargs):
    render = pystache.Renderer(missing_tags='strict')
    return render.render(*args, **kwargs)
