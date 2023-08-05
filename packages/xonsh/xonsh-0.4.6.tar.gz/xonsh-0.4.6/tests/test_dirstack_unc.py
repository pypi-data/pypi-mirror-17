# -*- coding: utf-8 -*-
"""Testing dirstack"""
#from __future__ import unicode_literals, print_function

from contextlib import contextmanager
from functools import wraps
import os
import os.path
import subprocess

import builtins
import pytest

from xonsh import dirstack
from xonsh.environ import Env
from xonsh.built_ins import load_builtins
from xonsh.dirstack import DIRSTACK

from xonsh.platform import ON_WINDOWS

from xonsh.dirstack import _unc_tempDrives

HERE = os.path.abspath(os.path.dirname(__file__))
PARENT = os.path.dirname(HERE)

def drive_in_use(letter):
    return ON_WINDOWS and os.system('vol {}: 2>nul>nul'.format(letter)) == 0

pytestmark = pytest.mark.skipif(any(drive_in_use(l) for l in 'ywzx'),
                                reason='Drive letters used by tests are '
                                       'are already used by Windows.')


@pytest.yield_fixture(scope="module")
def shares_setup(tmpdir_factory):
    """create some shares to play with on current machine.

    Yield (to test case) array of structs: [uncPath, driveLetter, equivLocalPath]

    Side effect: `os.chdir(TEST_WORK_DIR)`
    """

    if not ON_WINDOWS:
        return []

    shares = [[r'uncpushd_test_HERE', 'y:', HERE]
              , [r'uncpushd_test_PARENT', 'w:', PARENT]]

    for s, d, l in shares:  # set up some shares on local machine.  dirs already exist test case must invoke wd_setup.
        subprocess.call(['NET', 'SHARE', s, '/delete'], universal_newlines=True)  # clean up from previous run after good, long wait.
        subprocess.call(['NET', 'SHARE', s + '=' + l], universal_newlines=True)
        subprocess.call(['NET', 'USE', d, r"\\localhost" + '\\' + s], universal_newlines=True)

    yield [[r"\\localhost" + '\\' + s[0], s[1], s[2]] for s in shares]

    # we want to delete the test shares we've created, but can't do that if unc shares in DIRSTACK
    # (left over from assert fail aborted test)
    os.chdir(HERE)
    for dl in _unc_tempDrives:
        subprocess.call(['net', 'use', dl, '/delete'], universal_newlines=True)
    for s, d, l in shares:
        subprocess.call(['net', 'use', d, '/delete'], universal_newlines=True)
        # subprocess.call(['net', 'share', s, '/delete'], universal_newlines=True) # fails with access denied,
        # unless I wait > 10 sec. see http://stackoverflow.com/questions/38448413/access-denied-in-net-share-delete


def test_pushdpopd(xonsh_builtins):
    """Simple non-UNC push/pop to verify we didn't break nonUNC case.
    """
    xonsh_builtins.__xonsh_env__ = Env(CDPATH=PARENT, PWD=HERE)

    dirstack.cd([PARENT])
    owd = os.getcwd()
    assert owd.casefold() == xonsh_builtins.__xonsh_env__['PWD'].casefold()
    dirstack.pushd([HERE])
    wd = os.getcwd()
    assert wd.casefold() == HERE.casefold()
    dirstack.popd([])
    assert owd.casefold() == os.getcwd().casefold(), "popd returned cwd to expected dir"


@pytest.mark.skipif( not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_simple_push_pop(xonsh_builtins, shares_setup):
    xonsh_builtins.__xonsh_env__ = Env(CDPATH=PARENT, PWD=HERE)

    dirstack.cd([PARENT])
    owd = os.getcwd()
    assert owd.casefold() == xonsh_builtins.__xonsh_env__['PWD'].casefold()
    dirstack.pushd([r'\\localhost\uncpushd_test_HERE'])
    wd = os.getcwd()
    assert os.path.splitdrive(wd)[0].casefold() == 'z:'
    assert os.path.splitdrive(wd)[1].casefold() == '\\'
    dirstack.popd([])
    assert owd.casefold() == os.getcwd().casefold(), "popd returned cwd to expected dir"
    assert len(_unc_tempDrives) == 0


@pytest.mark.skipif( not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_push_to_same_share(xonsh_builtins):
    xonsh_builtins.__xonsh_env__ = Env(CDPATH=PARENT, PWD=HERE)

    dirstack.cd([PARENT])
    owd = os.getcwd()
    assert owd.casefold() == xonsh_builtins.__xonsh_env__['PWD'].casefold()
    dirstack.pushd([r'\\localhost\uncpushd_test_HERE'])
    wd = os.getcwd()
    assert os.path.splitdrive(wd)[0].casefold() == 'z:'
    assert os.path.splitdrive(wd)[1].casefold() == '\\'
    assert len(_unc_tempDrives) == 1
    assert len(DIRSTACK) == 1

    dirstack.pushd([r'\\localhost\uncpushd_test_HERE'])
    wd = os.getcwd()
    assert os.path.splitdrive(wd)[0].casefold() == 'z:'
    assert os.path.splitdrive(wd)[1].casefold() == '\\'
    assert len(_unc_tempDrives) == 1
    assert len(DIRSTACK) == 2

    dirstack.popd([])
    assert os.path.isdir('z:\\'), "Temp drived not unmapped till last reference removed"
    dirstack.popd([])
    assert owd.casefold() == os.getcwd().casefold(), "popd returned cwd to expected dir"
    assert len(_unc_tempDrives) == 0


@pytest.mark.skipif( not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_push_other_push_same(xonsh_builtins):
    """push to a, then to b. verify is w:, skipping already used y:
       Then push to a again. Pop (check b unmapped and a still mapped), pop, pop (check a is unmapped)"""
    xonsh_builtins.__xonsh_env__ = Env(CDPATH=PARENT, PWD=HERE)

    dirstack.cd([PARENT])
    owd = os.getcwd()
    assert owd.casefold() == xonsh_builtins.__xonsh_env__['PWD'].casefold()
    dirstack.pushd([r'\\localhost\uncpushd_test_HERE'])
    assert os.getcwd().casefold() == 'z:\\'
    assert len(_unc_tempDrives) == 1
    assert len(DIRSTACK) == 1

    dirstack.pushd([r'\\localhost\uncpushd_test_PARENT'])
    wd = os.getcwd()
    assert os.getcwd().casefold() == 'x:\\'
    assert len(_unc_tempDrives) == 2
    assert len(DIRSTACK) == 2

    dirstack.pushd([r'\\localhost\uncpushd_test_HERE'])
    assert os.getcwd().casefold() == 'z:\\'
    assert len(_unc_tempDrives) == 2
    assert len(DIRSTACK) == 3

    dirstack.popd([])
    assert os.getcwd().casefold() == 'x:\\'
    assert len(_unc_tempDrives) == 2
    assert len(DIRSTACK) == 2
    assert os.path.isdir('x:\\')
    assert os.path.isdir('z:\\')

    dirstack.popd([])
    assert os.getcwd().casefold() == 'z:\\'
    assert len(_unc_tempDrives) == 1
    assert len(DIRSTACK) == 1
    assert not os.path.isdir('x:\\')
    assert os.path.isdir('z:\\')

    dirstack.popd([])
    assert os.getcwd().casefold() == owd.casefold()
    assert len(_unc_tempDrives) == 0
    assert len(DIRSTACK) == 0
    assert not os.path.isdir('x:\\')
    assert not os.path.isdir('z:\\')


@pytest.mark.skipif( not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_push_base_push_rempath(xonsh_builtins):
    """push to subdir under share, verify  mapped path includes subdir"""
    pass


#really?  Need to cut-and-paste 2 flavors of this? yield_fixture requires yield in defined function body, not callee
@pytest.yield_fixture()
def with_unc_check_enabled():
    if not ON_WINDOWS:
        return

    import winreg

    old_wval = 0
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'software\microsoft\command processor', access=winreg.KEY_WRITE)
    try:
        wval, wtype = winreg.QueryValueEx(key, 'DisableUNCCheck')
        old_wval = wval # if values was defined at all
    except OSError as e:
        pass
    winreg.SetValueEx(key, 'DisableUNCCheck', None, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

    yield old_wval

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'software\microsoft\command processor', access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'DisableUNCCheck', None, winreg.REG_DWORD, old_wval)
    winreg.CloseKey(key)


@pytest.yield_fixture()
def with_unc_check_disabled():  # just like the above, but value is 1 to *disable* unc check
    if not ON_WINDOWS:
        return

    import winreg

    old_wval = 0
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'software\microsoft\command processor', access=winreg.KEY_WRITE)
    try:
        wval, wtype = winreg.QueryValueEx(key, 'DisableUNCCheck')
        old_wval = wval # if values was defined at all
    except OSError as e:
        pass
    winreg.SetValueEx(key, 'DisableUNCCheck', None, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)

    yield old_wval

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'software\microsoft\command processor', access=winreg.KEY_WRITE)
    winreg.SetValueEx(key, 'DisableUNCCheck', None, winreg.REG_DWORD, old_wval)
    winreg.CloseKey(key)


@pytest.fixture()
def xonsh_builtins_cd(xonsh_builtins):
    xonsh_builtins.__xonsh_env__['PWD'] = os.getcwd()
    xonsh_builtins.__xonsh_env__['DIRSTACK_SIZE'] = 20
    return xonsh_builtins


@pytest.mark.skipif(not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_cd_unc_auto_pushd(xonsh_builtins_cd, with_unc_check_enabled):
    xonsh_builtins_cd.__xonsh_env__['AUTO_PUSHD'] = True
    so, se, rc = dirstack.cd([r'\\localhost\uncpushd_test_PARENT'])
    assert rc == 0
    assert os.getcwd().casefold() == 'z:\\'
    assert len(DIRSTACK) == 1
    assert os.path.isdir('z:\\')


@pytest.mark.skipif(not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_cd_unc_nocheck(xonsh_builtins_cd, with_unc_check_disabled):
    dirstack.cd([r'\\localhost\uncpushd_test_HERE'])
    assert os.getcwd().casefold() == r'\\localhost\uncpushd_test_here'


@pytest.mark.skipif(not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_cd_unc_no_auto_pushd(xonsh_builtins_cd, with_unc_check_enabled):
    so, se, rc = dirstack.cd([r'\\localhost\uncpushd_test_PARENT'])
    assert rc != 0
    assert so is None or len(so) == 0
    assert 'disableunccheck' in se.casefold() and 'auto_pushd' in se.casefold()


@pytest.mark.skipif(not ON_WINDOWS, reason="Windows-only UNC functionality")
def test_uncpushd_unc_check():
    # emminently suited to mocking, but I don't know how
    # need to verify unc_check_enabled correct whether values set in HKCU or HKLM
    pass

