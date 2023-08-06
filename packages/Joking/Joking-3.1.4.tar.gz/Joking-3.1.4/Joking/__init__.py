"""
Joking is a python library to get jokes
"""
import webbrowser
import requests, urllib, random
from bs4 import BeautifulSoup

def random_dad_joke():
    url = "https://icanhazdadjoke.com/"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("p").text)

def programming_joke():
    url = "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    return(response.json)


def Give_FeedBack(name, message):
    webbrowser.open(f"mailto:hahacoolguystaco@gmail.com?subject=FEEDBACK&body={message}%0D%0A%0D%0AFrom%20{name}")
def Help():
    webbrowser.open("https://readthedocs.org/projects/joking/")

def chuck_norris_jokes():
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    return(response.json().get("value"))

def random_joke():
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    return(response.json)

def JOD():
    url = "https://jokes.one/joke-of-the-day/jod"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("p").text)

def Multiple_Jokes(n):
    for i in range(n):
        url = "https://icanhazdadjoke.com/"
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")
        return(soup.find("p").text)

def sjoke(Joke_id):
    url = f"https://icanhazdadjoke.com/j/{Joke_id}"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("p").text)

def search_for_joke(Search_term):
    url = f"https://icanhazdadjoke.com/search?term={Search_term}"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("td").text)

def Random_knock_knock_joke():
    import random
    ran_int = random.randint(1, 148)
    url = f"http://www.jokes4us.com/knockknockjokes/random/knockknock{ran_int}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("font").text)

def skkjoke(Joke_id):
    url = f"http://www.jokes4us.com/knockknockjokes/random/knockknock{Joke_id}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("font").text)

def DarkJoke():
    url = "https://v2.jokeapi.dev/joke/Dark?format=txt"
    response = requests.request("GET", url)
    return(response.text)

def Pun():
    url = "https://v2.jokeapi.dev/joke/Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt"
    response = requests.request("GET", url)
    return(response.text)

def Submit_joke(Q, Punchline, Your_name="Anonymous", twitter="@Null"):
    url = "https://backend-omega-seven.vercel.app/api/addjoke"
    payload = {
        "name": Your_name,
        "twitter": twitter,
        "question": Q,
        "punchline": Punchline
    }
    response = requests.request("POST", url, json=payload)
    return(response.text)

def yo_mama_joke_slash_insults():
    import random
    Joke_id = random.randint(1, 1000)
    url = f"http://www.jokes4us.com/yomamajokes/random/yomama{Joke_id}.html"
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, "html.parser")
    return(soup.find("font").text)

def animal_joke():
    import random
    idtouse = random.randint(1, 29)
    idtouse = f"https://retoolapi.dev/NyRMHE/anijokes/{idtouse}"
    response = requests.get(idtouse)
    return(response.json().get(" Jokes"))

def Meme(Subreddit=""):
    url = f"https://meme-api.herokuapp.com/gimme/{Subreddit}"
    response = requests.request("GET", url)
    Meme_url = response.json().get("url")
    return Meme_url

def make_meme(Meme_Name, Top_Text, Bottom_text):
    try:
        url = f"http://apimeme.com/meme?meme={Meme_Name}&top={Top_Text}&bottom={Bottom_text}"
        meme = urllib.parse.quote(url, safe=".:/-&?=")
        return meme
    except:
        return "Whoops, you can report errors using this form https://qjsezwc2ejy.typeform.com/to/CiSSoxpr"
    

def Irony_Joke():
    nu = random.randint(1, 16)
    url = f"https://retoolapi.dev/whbbdL/irony/{nu}"
    response = requests.get(url)
    return response.json()["Joke"]

def Irony_Joke_By_ID(id):
    url = f"https://retoolapi.dev/whbbdL/irony/{id}"
    response = requests.get(url)
    return response.json()["Joke"]

def Law_Joke():
    nu = random.randint(1, 16)
    url = f"https://retoolapi.dev/S5yUMi/lawjokes/{nu}"
    response = requests.get(url)
    return response.json()["Joke"]

def Law_Joke_By_ID(id):
    url = f"https://retoolapi.dev/S5yUMi/lawjokes/{id}"
    response = requests.get(url)
    return response.json()["Joke"]

__version__ = "3.1.4"
__copyright__ = """MIT License

Copyright (c) 2022 IEATCODE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""