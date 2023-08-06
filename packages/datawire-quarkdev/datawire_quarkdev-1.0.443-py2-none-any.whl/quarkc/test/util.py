# Copyright 2016 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, pytest
import subprocess

from quarkc import _metadata

def is_excluded_file(name):
    if "quarkc/lib/" in name or name == "reflector":
        return True
    else:
        return False

def is_runtime(path):
    return "quark_" in path and "_runtime" in path

def filter_builtin(content):
    """Filter out lines that shouldn't be compared in tests."""
    if content is None:
        return None
    lines = content.split("\n")
    result = []
    skipping = False
    for line in lines:
        # Checked-in test comparison packaging hardcodes version 0.0.1 since we
        # have different versions of Quark stdlib on each release:
        quark_dependency = (('"quark": "0.0.1"' in line) or
                            ('"quark": "{}"'.format(_metadata.__version__) in line) or
                            ("spec.add_runtime_dependency 'quark'" in line) or
                            ("<version>0.0.1</version>" in line) or
                            ("<version>{}</version>".format(_metadata.__version__) in line) or
                            ("install_requires" in line and "quark==" in line))
        if "BEGIN_BUILTIN" in line:
            skipping = True
        if not skipping and not quark_dependency:
            result.append(line)
        if "END_BUILTIN" in line:
            skipping = False
    return "\n".join(result)

def is_valid_change(path, content, expected):
    if is_runtime(path): return True
    return filter_builtin(content) == filter_builtin(expected)

def check_file(path, content):
    try:
        with open(path) as fd:
            expected = fd.read()
    except IOError:
        expected = None
    if expected != content:
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        if is_valid_change(path, content, expected):
            with open(path, "wb") as fd: fd.write(content)
            return content
        else:
            with open(path + ".cmp", "wb") as fd: fd.write(content)
    return expected

def assert_file(path, content):
    expected = check_file(path, content)
    assert content == expected

def maybe_xfail(code, ext=None):
    if "xfail" in code and "xfail:" not in code:
        pytest.xfail()
    if ext and ("xfail:%s"%ext) in code:
        pytest.xfail()


def get_git_top(start="."):
    try:
        git_top = subprocess.check_output("git rev-parse --show-toplevel".split(), cwd=start).strip()
    except (OSError, subprocess.CalledProcessError):
        raise ValueError("Not a git repository: %r" % start)
    return git_top
