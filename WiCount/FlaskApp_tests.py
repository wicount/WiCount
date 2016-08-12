import unittest


class FlaskAppTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_login(self):
        pass

    
    def test_login(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in'
        
         
if __name__ == '__main__':
    unittest.main()