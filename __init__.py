#!/usr/bin/env python
import json
import os
import sys


def str_to_args(s):
    """
    First tries to de-serialize the string as JSON.  If that fails, we eval() it.

    >>> str_to_args("{'msg': 'woot'}")
    {'msg': 'woot'}

    >>> str_to_args("{'one': 1, 'two': 2}")
    {'two': 2, 'one': 1}

    """
    d = None

    try:
        d = json.loads(s)

    except:
        try:
            d = eval("{s}".format(s=s))
        except:
            pass

    return d


def package_for_path(path):
    """
    >>> package_for_path('foo')
    ('foo', None)

    >>> package_for_path('foo.py')
    ('foo', None)

    >>> package_for_path('foo.bar')
    ('foo', 'bar')

    >>> package_for_path('foo/bar/test.py')
    ('foo.bar', 'test')

    >>> package_for_path('jobs/0148-create-default-policy-group.py')
    ('jobs', '0148-create-default-policy-group')

    """
    path = str(path)

    if path[-3:] == '.py':
        path, ext = os.path.splitext(path)

    bits = path.replace('/', '.').split('.')

    if len(bits) == 0:
        return '', None

    elif len(bits) == 1:
        return bits[0], None

    else:
        return '.'.join(bits[0:-1]), bits[-1]


# --------------------------------------------------
def run(package=None, function='run', args=None, path_extras=None, verbose=False):
    if verbose:
        print("---- pyrun.run() ----")
        print("package: {0}".format(package))
        print("function: {0}".format(function))
        print("args: {0}".format(args))
        print("path_extras: {0}".format(path_extras))
        print("------------------------")

    if package is None:
        return None

    if args is None:
        args = dict()

    for p in path_extras:
        if p not in sys.path:
            sys.path.extend(path_extras)

    # Now we're ready to try dynamically loading and running this code
    result = None
    pkg = None

    pkg_base, pkg_name = package_for_path(package)

    if verbose:
        print('  pkg_base: {0}'.format(pkg_base))
        print('  pkg_name: {0}'.format(pkg_name))

    if isinstance(pkg_name, str):
        if verbose:
            print('Hopefully doing something like: from {0} import {1}'.format(pkg_base, pkg_name))

        __import__('{0}.{1}'.format(pkg_base, pkg_name))
        pkg = sys.modules['{0}.{1}'.format(pkg_base, pkg_name)]

        if verbose:
            print('  pkg: {0} {1}'.format(pkg, type(pkg)))
            print('  pkg.__file__: {0}'.format(pkg.__file__))
            print('  pkg.__name__: {0}'.format(pkg.__name__))
            print("-----------------------")

    else:
        if verbose:
            print('Importing \'{0}\''.format(pkg_base))

        __import__(pkg_base)
        pkg = sys.modules[pkg_base]

        if verbose:
            print('  pkg: {0} {1}'.format(pkg, type(pkg)))
            print('  pkg.__file__: {0}'.format(pkg.__file__))
            print('  pkg.__name__: {0}'.format(pkg.__name__))
            print("-----------------------")
            # print('  pkg.__path__: {0}'.format(pkg.__path__))
            # print('  pkg.__package__: {0}'.format(pkg.__package__))

    if pkg:
        # if verbose:
        #     print('  dir({0})'.format(dir(pkg)))

        try:
            function_ptr = getattr(pkg, function)

        except AttributeError:
            if verbose:
                print("####")
                print("\nERROR: `{m}` doesn't seem to exist!".format(m=function))

                print("\nPerhaps you wanted one of these:\n")

                still_in_imports = True
                for m in dir(pkg):
                    if m.startswith('_'):
                        still_in_imports = False

                    else:
                        if not still_in_imports:
                            print("    {m}".format(m=m))

                print("\n####")

        else:
            if callable(function_ptr):
                result = function_ptr(**args)

            else:
                if verbose:
                    print("####")
                    print("\nERROR: `{m}` isn't callable!".format(m=function))

    return result


# --------------------------------------------------
# --------------------------------------------------
if __name__ == "__main__":
    import doctest
    print "Testing..."
    doctest.testmod()
    print "Done."

