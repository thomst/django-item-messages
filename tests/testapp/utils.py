
def flatten_dict(thing):
    if isinstance(thing, dict):
        return flatten_dict(thing.values())
    try:
        return flatten_dict([v for subdict in thing for v in subdict.values()])
    except AttributeError:
        return [v for v in thing]
