import unittest
import datetime
import io
import sys


class TestBowling(unittest.TestCase):
    '''
    After making a basic skeleton for Bowling with a calcScore that returned a score of zero, I made all the 
    tests from "testOneFrameBasic" to "testSampleInput5". They cover what I could think of after reading the 
    assignment instructions in addition to the sample inputs given.
    '''
    
    def testOneFrameBasic(self):
        b = Bowling()
        result = b.calcScore("[2 4]")
        self.assertEqual(result, 6, "cannot add one frame")
        
    def testTwoFrameBasic(self):
        b = Bowling()
        result = b.calcScore("[5 3] [4 7]")
        self.assertEqual(result, 19, "cannot add two basic frames")
        
    def testOneStrike(self):
        b = Bowling()
        result = b.calcScore("[X]")
        self.assertEqual(result, 13, "cannot handle one strike")
    
    def testOneSpare(self):
        b = Bowling()
        result = b.calcScore("[5 /]")
        self.assertEqual(result, 13, "cannot handle one spare")
        
    def testStrikePlusNext(self):
        b = Bowling()
        result = b.calcScore("[X] [5 6]")
        self.assertEqual(result, 35,"cannot handle strike and basic")
        
    def testSparePlusNext(self):
        b = Bowling()
        result = b.calcScore("[3 /] [7 2]")
        self.assertEqual(result, 29,"cannot handle spare and basic")  
        
    def testSpecialCaseOnly(self):
        b = Bowling()
        result = b.calcScore("[1 9] [8 /]")
        self.assertEqual(result, 104, "cannot handle special case")    
        
    def testSampleInput1(self):
        b = Bowling()
        result = b.calcScore("[1 3] [4 2] [1 /]")
        self.assertEqual(result, 23, "cannot handle sample 1")
        
    def testSampleInput2(self):
        b = Bowling()
        result = b.calcScore("[X] [2 4] [1 1]")
        self.assertEqual(result, 27, "cannot handle sample 2")
        
    def testSampleInput3(self):
        b = Bowling()
        result = b.calcScore("[2 /] [3 4] [5 3]")
        self.assertEqual(result, 31, "cannot handle sample 3")
        
    def testSampleInput4(self):
        b = Bowling()
        result = b.calcScore("[3 7] [1 9] [8 /]")
        self.assertEqual(result, 104, "cannot handle sample 4") 
        
    def testSampleInput5(self):
        b = Bowling()
        result = b.calcScore("[1 9] [1 1] [8 /]")
        self.assertEqual(result, 25, "cannot handle sample 5")  
        
    '''
    Next I realized that I didnt cover null/empty string or incorrect format so made the cases for these after all above tests were passing
    '''
    def testNullInput(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        b = Bowling()
        b.calcScore('')
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Null/empty string has been input, please check input\n") 
    
        
class Bowling():
    def __init__(self):
        self.special = 104
    
    def calcScore(self, rounds):
        score = 0
        
        
        #Here is where I added the exceptional cases such as null, these are handled by printing a message to standard output and returning a score of 0
        if(rounds == ''):
            print("Null/empty string has been input, please check input")
            return 0
        
        
        
        #The first tests I want to pass are the ones calculating just one frame. Once the "if(len(rounds) <= 5)" section was completed the 3 single frame tests passed
        if(len(rounds) <= 5):
            if(rounds[1] == 'X'):               
                score += 13
            elif(rounds[3] == '/'):                
                score += 13
            else:              
                score = int(rounds[1]) + int(rounds[3])
        
        else:
            frameScores = rounds
            frames = rounds.split(']')
            # Below adds a space to first frame to match the format of the rest of the values in the array
            frames[0] = ' ' + frames[0]
            x = 0
            frame = frames[x]
            for frame in frames:
                if(frame != ''):
                    
                    nextFrame = frames[x+1]
                    if(frame[2] == 'X'):
                        if(nextFrame == ''):
                            score += 13
                        else:
                            score += 13 + int(nextFrame[2]) + int(nextFrame[4])
                    elif(frame[4] == '/'):
                        if(nextFrame == ''):
                            score += 13  
                        else:
                            score += 13 + int(nextFrame[2])
                    else:
                        if(frame == " [1 9"):
                            if(nextFrame == " [8 /"):
                                score = 104
                                break
                            else:
                                score += int(frame[2]) + int(frame[4])
                        else:
                            score += int(frame[2]) + int(frame[4]) 
                        
                    x += 1
        return score
            

def main():
    unittest.main()


if __name__ == '__main__':
    main()
    
