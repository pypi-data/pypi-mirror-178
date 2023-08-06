print(40*'*')
print('testing location geocasual \n')
import sys
import unittest




sys.path.append('/media/henskyconsulting/easystore/Hensky/Projects/2022twitloccan/cannuckfind')
from geograpy import get_geoPlace_context

class Testgeocasual(unittest.TestCase):
    """
    Test location.geocasual
    """
    def test_GeoCasual(self):
        from cannuckfind import location
        testloc = location.GeoCasual()
        print("Start GeoCasual test in cannuckfind")
        print(dir(testloc))
        print(40*'=')

    def test_GeoCasual(self):
        print(40*'=')
        from cannuckfind import location
        
        print("Start GeoCasual test in cannuckfind")
        testcasual = location.GeoCasual()
        print(dir(testcasual))
        self.assertTrue(testcasual.isjoke('Nowhere'))
        self.assertTrue(testcasual.isjoke('Miles away'))
        self.assertTrue(testcasual.isCan("amiskwacîwâskahikan"))
        self.assertTrue(testcasual.isUS('NYC'))

        
    def test_Docs(self):
        # test examples used in documentation
        print(40*'=')
        from cannuckfind import location
        testcasual = location.GeoCasual()
        testC3 = location.C3(useGEOGRPY = True)
        
        isjoke = testcasual.isjoke("everywhere")
        print(isjoke)
        isCan = testC3.isCan('Toronto')
        print(isCan)
 
print('*** test geocasual complete')
print('*** only two tests should appear as there are not asserts in the first test')
print(40*'*')       

if __name__ == '__main__':
    unittest.main()




