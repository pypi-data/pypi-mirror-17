import inspect
import typing
import functools
from functools import wraps

from wrapt import decorator

from .settings import Settings
from .enforcers import apply_enforcer, Parameters, GenericProxy
from .types import is_type_of_type


def runtime_validation(data=None, *, enabled=None, group=None):
    """
    This decorator enforces runtime parameter and return value type checking validation
    It uses the standard Python 3.5 syntax for type hinting declaration
    """
    if enabled is not None and not isinstance(enabled, bool):
        raise TypeError('Enabled parameter must be boolean')

    if group is not None and not isinstance(group, str):
        raise TypeError('Group parameter must be string')

    if enabled is None and group is None:
        enabled = True

    # see https://wrapt.readthedocs.io/en/latest/decorators.html#decorators-with-optional-arguments
    if data is None:
        return functools.partial(runtime_validation, enabled=enabled, group=group)

    configuration = Settings(enabled=enabled, group=group)

    @decorator
    def build_wrapper(wrapped, instance, args, kwargs):
        if instance is None:
            if inspect.isclass(wrapped):
                # Decorator was applied to a class
                root = None
                if is_type_of_type(wrapped, typing.Generic, covariant=True):
                    wrapped = GenericProxy(wrapped)
                    root = wrapped.__enforcer__.validator

                for attr_name in dir(wrapped):
                    try:
                        if attr_name == '__class__':
                            raise AttributeError
                        old_attr = getattr(wrapped, attr_name)
                        new_attr = decorate(old_attr, configuration, obj_instance=None, parent_root=root)
                        setattr(wrapped, attr_name, new_attr)
                    except AttributeError:
                        pass
                return wrapped
            else:
                # Decorator was applied to a function or staticmethod.
                if issubclass(type(wrapped), staticmethod):
                    return staticmethod(decorate(wrapped.__func__, configuration, None))
                return decorate(wrapped, configuration, None)
        else:
            if inspect.isclass(instance):
                # Decorator was applied to a classmethod.
                print('class method')
                return decorate(wrapped, configuration, None)
            else:
                # Decorator was applied to an instancemethod.
                print('instance method')
                return decorate(wrapped, configuration, instance)

    generate_decorated = build_wrapper(data)
    return generate_decorated()


def decorate(data, configuration, obj_instance=None, parent_root=None) -> typing.Callable:
    """
    Performs the function decoration with a type checking wrapper

    Works only if '__annotations__' are defined on the passed object
    """
    if not hasattr(data, '__annotations__'):
        return data

    apply_enforcer(data, parent_root=parent_root, settings=configuration)

    @decorator
    def universal(wrapped, instance, args, kwargs):
        """
        This function will be returned by the decorator. It adds type checking before triggering
        the original function and then it checks for the output type. Only then it returns the
        output of original function.
        """
        enforcer = data.__enforcer__
        skip = False

        # In order to avoid problems with TypeVar-s, validator must be reset
        enforcer.reset()

        instance_method = False
        if instance is not None and not inspect.isclass(instance):
            instance_method = True

        if hasattr(wrapped, '__no_type_check__'):
            skip = True

        if instance_method:
            parameters = Parameters([instance, *args], kwargs, skip)
        else:
            parameters = Parameters(args, kwargs, skip)

        # First, check argument types (every key not labelled 'return')
        _args, _kwargs, _ = enforcer.validate_inputs(parameters)

        if instance_method:
            if len(_args) > 1:
                _args = _args[1:]
            else:
                _args = tuple()

        result = wrapped(*_args, **_kwargs)

        # we *only* return result if all type checks passed
        if skip:
            return result
        else:
            return enforcer.validate_outputs(result)

    return universal(data)
