

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_2():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'rdkit.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        load_order_filepath = os.path.join(libs_dir, '.load-order-rdkit-2022.9.2')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-rdkit-2022.9.2')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    WinDLL(lib_path)


_delvewheel_init_patch_1_1_2()
del _delvewheel_init_patch_1_1_2
# end delvewheel patch

import logging
import sys

# Need to import rdBase to properly wrap exceptions
# otherwise they will leak memory
from . import rdBase

try:
  from .rdBase import rdkitVersion as __version__
except ImportError:
  __version__ = 'Unknown'
  raise

logger = logging.getLogger("rdkit")

# if we are running in a jupyter notebook, enable the extensions
try:
  kernel_name = get_ipython().__class__.__name__

  if kernel_name == 'ZMQInteractiveShell':
    logger.info("Enabling RDKit %s jupyter extensions" % __version__)
    from rdkit.Chem.Draw import IPythonConsole
    rdBase.LogToPythonStderr()
except Exception:
  pass

# Do logging setup at the end, so users can suppress the
# "enabling jupyter" message at the root logger.
log_handler = logging.StreamHandler(sys.stderr)
logger.addHandler(log_handler)
logger.setLevel(logging.WARN)
logger.propagate = False

# Uncomment this to use Python logging by default:
# rdBase.LogToPythonLogger()
