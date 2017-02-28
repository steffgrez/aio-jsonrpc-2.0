
import inspect


def is_valid_params(func, params):
    # inspect method
    spec = inspect.getargspec(func)
    if spec.defaults:
        required = spec.args[:-len(spec.defaults)]
    else:
        required = spec.args

    # checks params validity
    if not params:
        if required:
            return False
    elif isinstance(params, list):
        if len(params) < len(required) or len(params) > len(spec.args):
            return False
    else:
        params_keys = set(params.keys())
        if (
                len(params_keys) > len(spec.args) or
                len(set(params_keys) & set(required)) != len(required) or
                len(set(params_keys) - set(spec.args)) > 0
        ):
            return False

    return True
