"""Vox tests"""

import builtins
import stat
import os
from xontrib.voxapi import Vox

from tools import skip_if_on_conda


@skip_if_on_conda
def test_crud(xonsh_builtins, tmpdir):
    """
    Creates a virtual environment, gets it, enumerates it, and then deletes it.
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)

    last_event = None

    @xonsh_builtins.events.vox_on_create
    def create(name):
        nonlocal last_event
        last_event = 'create', name

    @xonsh_builtins.events.vox_on_delete
    def delete(name):
        nonlocal last_event
        last_event = 'delete', name

    vox = Vox()
    vox.create('spam')
    assert stat.S_ISDIR(tmpdir.join('spam').stat().mode)
    assert last_event == ('create', 'spam')

    env, bin = vox['spam']
    assert env == str(tmpdir.join('spam'))
    assert os.path.isdir(bin)

    assert 'spam' in vox

    del vox['spam']

    assert not tmpdir.join('spam').check()
    assert last_event == ('delete', 'spam')


@skip_if_on_conda
def test_activate(xonsh_builtins, tmpdir):
    """
    Creates a virtual environment, gets it, enumerates it, and then deletes it.
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)
    # I consider the case that the user doesn't have a PATH set to be unreasonable
    xonsh_builtins.__xonsh_env__.setdefault('PATH', [])

    last_event = None

    @xonsh_builtins.events.vox_on_activate
    def activate(name):
        nonlocal last_event
        last_event = 'activate', name

    @xonsh_builtins.events.vox_on_deactivate
    def deactivate(name):
        nonlocal last_event
        last_event = 'deactivate', name

    vox = Vox()
    vox.create('spam')
    vox.activate('spam')
    assert xonsh_builtins.__xonsh_env__['VIRTUAL_ENV'] == vox['spam'].env
    assert last_event == ('activate', 'spam')
    vox.deactivate()
    assert 'VIRTUAL_ENV' not in xonsh_builtins.__xonsh_env__
    assert last_event == ('deactivate', 'spam')


@skip_if_on_conda
def test_path(xonsh_builtins, tmpdir):
    """
    Test to make sure Vox properly activates and deactivates by examining $PATH
    """
    xonsh_builtins.__xonsh_env__['VIRTUALENV_HOME'] = str(tmpdir)
    # I consider the case that the user doesn't have a PATH set to be unreasonable
    xonsh_builtins.__xonsh_env__.setdefault('PATH', [])

    oldpath = list(xonsh_builtins.__xonsh_env__['PATH'])
    vox = Vox()
    vox.create('eggs')

    vox.activate('eggs')
    
    assert oldpath != xonsh_builtins.__xonsh_env__['PATH']
    
    vox.deactivate()
    
    assert oldpath == xonsh_builtins.__xonsh_env__['PATH']
