from gv_ui import fileInput
import os
import os.path
import pytest

def test_find_source_path():
    result_exist = fileInput.find_source_path('rhopol.cube', 'tests/data/')
    result_dne = fileInput.find_source_path('not-real.cube', 'tests/data/')
    assert result_exist == 'tests/data/rhopol.cube'
    assert result_dne == None

def test_generate_unique_filename():
    name_1 = fileInput.generate_unique_filename('rhopol.cube', 'tests/data/')
    assert name_1 == 'rhopol_1.cube'

def test_copy_file():
    result = fileInput.copy_file('tests/data/rhopol.cube', 'tests/data/copy.cube')
    assert result == True
    assert os.path.isfile('tests/data/rhopol.cube') == True

    os.remove('tests/data/copy.cube')

    result = fileInput.copy_file('tests/data/not-real.cube', 'tests/data/copy.cube')
    assert result == False
    assert os.path.isfile('tests/data/copy.cube') == False
