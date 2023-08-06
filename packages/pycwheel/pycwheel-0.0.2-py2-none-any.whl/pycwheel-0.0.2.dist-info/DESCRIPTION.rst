Convert all py files in a whl to pyc.

The package version information is changed to append .compiled to the end.

If you want the pyc only version of the wheel, specify the .compiled version in your
requirements file.

Usage:
    pycwheel your_wheel-1.0.0-py2-none-any.whl
    # Output: your_wheel-1.0.0.compiled-py2-none-any.whl

References:
    https://www.python.org/dev/peps/pep-0427/


