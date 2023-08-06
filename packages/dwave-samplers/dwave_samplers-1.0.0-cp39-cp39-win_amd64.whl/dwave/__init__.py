

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_2():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'dwave_samplers.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        load_order_filepath = os.path.join(libs_dir, '.load-order-dwave_samplers-1.0.0')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-dwave_samplers-1.0.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    WinDLL(lib_path)


_delvewheel_init_patch_1_1_2()
del _delvewheel_init_patch_1_1_2
# end delvewheel patch

# Copyright 2022 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import pkgutil
__path__ = pkgutil.extend_path(__path__, __name__)
