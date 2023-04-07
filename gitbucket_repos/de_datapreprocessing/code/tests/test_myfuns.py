from src.myfuns import AddTen

def setup_module(module):
    print('\n *****SETUP*****')

def teardown_module(module):
    print('\n ******TEARDOWN******')
    
def test_addten():
    assert AddTen(12) == 22
    