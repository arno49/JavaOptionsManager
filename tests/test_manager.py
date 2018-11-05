from mock import patch
import os
from shaper import manager


def test_create_folder():
    """Check that manager.create_folders call create dir"""
    dir_name = 'test_folder'
    manager.create_folders(dir_name)
    assert os.path.isdir(dir_name)


def test_read_properties():
    pass