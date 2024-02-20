import cube_viskit as cv
import pytest

def testCubeImport():
    new_cube = cv.Cube()
    new_cube.load_cube("tests/data/rhopol.cube")
    assert new_cube.fname == "tests/data/rhopol.cube"

def testNoFileErr():
    new_cube = cv.Cube()
    with pytest.raises(SystemExit) as exc_info:
        new_cube.load_cube("")
    
    assert exc_info.value.code == -1
    
def testHeaderErr():
    new_cube = cv.Cube()
    with pytest.raises(SystemExit) as exc_info:
        new_cube.load_cube("tests/data/rhopol_err_header.cube")
    
    assert exc_info.value.code == -2


def testAtomsErr():
    new_cube = cv.Cube()
    with pytest.raises(SystemExit) as exc_info:
        new_cube.load_cube("tests/data/rhopol_err_atoms.cube")
    
    assert exc_info.value.code == -3
    
def testDimensionsErr():
    new_cube = cv.Cube()
    with pytest.raises(SystemExit) as exc_info:
        new_cube.load_cube("tests/data/rhopol_err_dimensions.cube")
    
    assert exc_info.value.code == -4
    
def testFieldDataErr():
    new_cube = cv.Cube()
    with pytest.raises(SystemExit) as exc_info:
        new_cube.load_cube("tests/data/rhopol_err_data.cube")
    
    assert exc_info.value.code == -4
    

