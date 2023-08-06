# Setup tools for the SWIG GRT python bindings
from distutils.core import setup, Extension
import sys

class get_numpy_include(object):
    """Defer numpy.get_include() until after numpy is installed."""

    def __str__(self):
        import numpy
        return numpy.get_include()


include_dirs = [sys.prefix + "/include"]

# Assume libgrt has been installed as a conda package, and that it is available in the conda environment.
# Create an extension module for the swig wrapper
grt_module = Extension(
    "_GRT",
    sources=["GRT.i"],
    swig_opts=["-python", "-py3", "-c++", "-Wall", "-verbose"] + ["-I" + d for d in include_dirs],
    include_dirs=include_dirs + [get_numpy_include()],
    library_dirs=[sys.prefix + "/lib"],
    libraries=["grt"],
)


# Create the setup
setup(
    name="blackhc.GRT",
    version="0.2.5.dev0",
    author="Nick Gillian",
    description="""Python bindings for the Gesture Recognition Toolkit (GRT)""",
    ext_modules=[grt_module],
    py_modules=["GRT"],
    install_requires=["numpy", "swig", "libgrt"],
)
