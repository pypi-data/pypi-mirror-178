import unittest
from Joking import *

class TestSum(unittest.TestCase):
    def test_skkjoke(self):
        """
        Test that it can sum a list of integers
        """
        data = 100
        result = skkjoke(data)
        self.assertEqual(result, """

Knock knock
Who's there
Woo!
Woo who?
Don't get too excited it's just a knock knock joke.
""")

    def test_sjoke(self):
        data = "SvPRCIeiNuc"
        result = sjoke(data)
        self.assertEqual(result, "How does a dyslexic poet write? Inverse.")

    def test_Submit_Joke(self):
        data = "test"
        result = Submit_joke(data, data, data)
        self.assertEqual(result, "{status:'Joke created'}")
        
    def test_random_dad_joke(self):
        result = random_dad_joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_programming_joke(self):
        result = programming_joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_random_joke(self):
        result = random_joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_Multiple_Jokes(self):
        data = 2
        result = Multiple_Jokes(data)
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_Random_knock_knock_joke(self):
        result = Random_knock_knock_joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_DarkJoke(self):
        result = DarkJoke()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_Pun(self):
        result = Pun()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_yo_mama_jokes_slash_insults(self):
        result = yo_mama_joke_slash_insults()
        self.assertNotEqual(result, "Traceback (most recent call last):")

    def test_search_for_joke(self):
        data = "Monkey"
        result = search_for_joke(data)
        self.assertEqual(result, "\nWhat do you call a monkey in a mine field? A babooooom!\n\n")


    def test_JOD(self):
        result = JOD()
        self.assertNotEqual(result, "Traceback (most recent call last):")
    
    def test_noris(self):
        result = chuck_norris_jokes()
        self.assertNotEqual(result, "Traceback (most recent call last):")
    
    def test_Animal_joke(self):
        result = animal_joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")
    
    def Irony(self):
        result = Irony_Joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")
    def Irony_By_ID(self):
        result = Irony_Joke_By_ID(2)
        self.assertEqual(result, "The irony of getting a job. You get a job so you won't be homeless. But when you get a job you're home a lot less.")
    
    def test_Law(self):
        result = Law_Joke()
        self.assertNotEqual(result, "Traceback (most recent call last):")
    
    def test_Law_By_ID(self):
        result = Law_Joke_By_ID(20)
        self.assertEqual(result, "Q: What’s the difference between a tick and a lawyer?\r\nA: The tick falls off when you are dead.")
if __name__ == '__main__':
    unittest.main()