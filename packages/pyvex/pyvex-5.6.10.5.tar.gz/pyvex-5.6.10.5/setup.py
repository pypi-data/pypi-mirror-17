import os
import urllib2
import subprocess
import sys
import shutil
import glob
from distutils.errors import LibError
from distutils.core import setup
from distutils.command.build import build as _build
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg

if sys.platform == 'darwin':
    library_file = "libpyvex.dylib"
else:
    library_file = "libpyvex.so"


VEX_LIB_NAME = "vex" # can also be vex-amd64-linux
VEX_PATH = "vex"
if not os.path.exists(VEX_PATH):
    VEX_URL = 'https://github.com/angr/vex/archive/master.tar.gz'
    with open('master.tar.gz', 'w') as v:
        v.write(urllib2.urlopen(VEX_URL).read())
    if subprocess.call(['tar', 'xzf', 'master.tar.gz']) != 0:
        raise LibError("Unable to retrieve libVEX.")
    VEX_PATH='./vex-master'

def _build_vex():
    if subprocess.call(['make'], cwd=VEX_PATH) != 0:
        raise LibError("Unable to build libVEX.")

def _build_pyvex():
    e = os.environ.copy()
    e['VEX_PATH'] = '../' + VEX_PATH
    if subprocess.call(['make'], cwd='pyvex_c', env=e) != 0:
        raise LibError("Unable to build pyvex-static.")

def _shuffle_files():
    shutil.rmtree('pyvex/lib', ignore_errors=True)
    shutil.rmtree('pyvex/include', ignore_errors=True)
    os.mkdir('pyvex/lib')
    os.mkdir('pyvex/include')

    shutil.copy(os.path.join('pyvex_c', library_file), 'pyvex/lib')
    shutil.copy('pyvex_c/pyvex.h', 'pyvex/include')
    for f in glob.glob(os.path.join(VEX_PATH, 'pub', '*')):
        shutil.copy(f, 'pyvex/include')

def _build_ffi():
    import make_ffi
    make_ffi.doit(os.path.join(VEX_PATH,'pub'))

class build(_build):
    def run(self):
        self.execute(_build_vex, (), msg="Building libVEX")
        self.execute(_build_pyvex, (), msg="Building pyvex-static")
        self.execute(_shuffle_files, (), msg="Copying libraries and headers")
        self.execute(_build_ffi, (), msg="Creating CFFI defs file")
        _build.run(self)
cmdclass = { 'build': build }

class bdist_egg(_bdist_egg):
    def run(self):
        self.run_command('build')
        _bdist_egg.run(self)
cmdclass['bdist_egg'] = bdist_egg

try:
    from setuptools.command.develop import develop as _develop
    class develop(_develop):
        def run(self):
            self.execute(_build_vex, (), msg="Building libVEX")
            self.execute(_build_pyvex, (), msg="Building pyvex-static")
            self.execute(_shuffle_files, (), msg="Copying libraries and headers")
            self.execute(_build_ffi, (), msg="Creating CFFI defs file")
            _develop.run(self)
    cmdclass['develop'] = develop
except ImportError:
    print "Proper 'develop' support unavailable."

setup(
    name="pyvex", version='5.6.10.5', description="A Python interface to libVEX and VEX IR.",
    packages=['pyvex'],
    cmdclass=cmdclass,
    install_requires=[ 'pycparser', 'cffi>=1.0.3', 'archinfo' ],
    setup_requires=[ 'pycparser', 'cffi>=1.0.3' ],
    include_package_data=True,
    package_data={
        'pyvex': ['lib/*', 'include/*']
    }
)
