import cube_viskit as cv

def testCubeImport():
    new_cube = cv.Cube()
    new_cube.load_cube("GoVizzy/data/rhopol.cube")
    assert new_cube.fname == "GoVizzy/data/rhopol.cube" 
