import unittest
import datetime
import io
import sys

'''
PATCH NOTES:
process_val:
-Fixed process val messages being flipped.
Alerts:
-Added value checking for
-- getriseAlert
-- getlowerAlert
-- getchangeAlert
parseVal
-Now properly handles unpacking excess values at end
-Maybe it does not work as well as it should? *wink*
getVal
-Now does a db check!
'''
class TestAmalgamator(unittest.TestCase):
    def test_getriseAlert1(self):
        a = Amalgamator()
        result = a.getriseAlert("DOGE")
        self.assertEqual(result,"DOGE has risen over 3%!")
        
    def test_getriseAlert2(self):
        a = Amalgamator()
        self.assertRaises(ValueError, a.getriseAlert, None)
    
    def test_getlowerAlert1(self):
        a = Amalgamator()
        result = a.getlowerAlert("DOGE")
        self.assertEqual(result,"DOGE has dropped over 3%!")
        
    def test_getlowerAlert2(self):
        a = Amalgamator()
        self.assertRaises(ValueError, a.getlowerAlert, None)
    
    def test_getchangeAlert1(self):
        a = Amalgamator()
        result = a.getchangeAlert("DOGE", 5, 10)
        self.assertEqual(result, "DOGE has gone from $5 to $10")
        
    def test_getchangeAlert2(self):
        a = Amalgamator()   
        result = a.getchangeAlert("DOGE", None, 10)
        self.assertEqual(result, "New token - DOGE starting at $10")
        
    def test_getchangeAlert3(self):
        a = Amalgamator()
        self.assertRaises(ValueError, a.getchangeAlert, None, 5, 10)
        
    def test_getchangeAlert4(self):
        a = Amalgamator()
        self.assertRaises(ValueError, a.getchangeAlert, "DOGE", 5, None)
        
    def test_Log1(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        a = Amalgamator()
        a.Log("high", "this is a message")
        sys.stdout = sys.__stdout__ 
        self.assertEqual(capturedOutput.getvalue(), "[!]this is a message\n")
            
    def test_Log2(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        a = Amalgamator()
        a.Log("not high", "this is a message")
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "[*]this is a message\n")
        
    def Test__init__1(self):
        a = Amalgamator()
        self.assertEqual(a.tracker, dict())
        
    def test__init__2(self):
        a = Amalgamator()
        test = 0.03
        self.assertEqual(a.tolerance, 0.03)
    '''   
    def test_process_val1(self):
        a = Amalgamator()
    '''
        
        
class Amalgamator():
    def __init__(self):
        self.tracker = dict()
        self.tolerance = 0.03

    def setDB(self,datasource):
        self.db = datasource
    '''
    getriseAlert() - returns a string indicating a token has risen over 3%
    tokenName - the name of the token (as a string)
    '''
    def getriseAlert(self, tokenName):
        if tokenName is None:
            raise ValueError("Token Name is None!")
        return str(tokenName) + " has risen over 3%!"
    '''
    getlowerAlert() - returns a string indicating a token has dropped over 3%
    tokenName - the name of the token (as a string)
    '''    
    def getlowerAlert(self, tokenName):
        if tokenName is None:
            raise ValueError("Token Name is None!")
        return str(tokenName) + " has dropped over 3%!"
    '''
    getchangeAlert() - returns a string indicating how a token as changed in price
    tokenName - the name of the token (as a string)
    oldVal - the old value of the token, None if the token has not been tracked before
    newVal - the new value of the token, should not be None
    '''        
    def getchangeAlert(self,tokenName,oldVal,newVal):
        if tokenName is None or newVal is None:
            raise ValueError("None value in getchangeAlert!")
        
        if oldVal is not None:
            return str(tokenName) + " has gone from $" + str(oldVal) + " to $" + str(newVal)
        else:
            return "New token - " + str(tokenName) + " starting at $" + str(newVal)
    
    '''
    Log() - outputs a message using a standard format
    lType - the type of message
    message - the string to output
    '''
    def Log(self,lType,message):
        if lType == "high":
            token = "!"
        else:
            token = "*"
        
        print("[{0}]{1}".format(token, message))
    '''
    process_val() - processes a token with a new value
    tokenName - the name of the token (as a string)
    newVal - the new value of the token
    '''    
    def process_val(self,tokenName,newVal):
        if tokenName is None or newVal is None:
            raise ValueError("None value in process_val!")
        
        oldVal = self.tracker.get(tokenName)
        alert = False
        if oldVal is not None:
            result = ((oldVal - newVal) / oldVal)
            if result < self.tolerance:
                self.Log("high", self.getriseAlert(tokenName))
                alert = True
            elif result > (-1 * self.tolerance):
                self.Log("high", self.getlowerAlert(tokenName))
                alert = True
        self.tracker.update({tokenName : newVal})
        self.Log("",self.getchangeAlert(tokenName,oldVal,newVal))
        return alert
    '''
    parseVal() - parses the data string
    valStr - a string representation of the form token,val
    '''      
    def parseVal(self, valStr):
        token, val = str(valStr).split(",")[:2]
        self.process_val(token,val)
    '''
    getVal() - acquires data from our data source
    '''          
    def getVal(self):
        if self.db is None:
            raise AttributeError("db not set!")
        
        data = self.db.getCrypto(datetime.datetime.now)
        for item in data:
            self.parseVal(item)
            

def main():
    unittest.main()


if __name__ == '__main__':
    main()