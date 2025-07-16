# wordlist downloaded from https://websites.umich.edu/~jlawler/wordlist.html -> https://websites.umich.edu/~jlawler/wordlist

import os 
import random
import string
from collections import Counter

# Flask for hosting
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dictionary_path = os.path.join(os.path.dirname(__file__), "wordlist.txt")

# import "wordlist.txt" dictionary into set dictionary
def importDictionary(filepath):
    dictionary = set()
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        for word in f:
            dictionary.add(word.rstrip())
    return dictionary

DICTIONARY = importDictionary(dictionary_path)

# find list of words
# first letter in list must be in the word

def canSpell(word, letters):
    wordCount = Counter(word)
    letterCount = Counter(letters)
    return all(wordCount[c] <= letterCount.get(c, 0) for c in wordCount)

def findWordList(letters, dictionary_path="wordlist.txt"):
    words = importDictionary(dictionary_path)
    first = letters[0]
    return [word for word in words if canSpell(word, letters) and first in word]

# generate random letters
# first letter in list is "must use" letter
def randomLetters(length):
    vowels = {"a", "e", "i", "o", "u"}
    while True:
        word = ''.join(random.sample(string.ascii_lowercase, length))
        if any(char in vowels for char in word):
            return list(word)

# Get a list of words based on random letters
@app.route('/api/getWordList', methods=['GET'])
def getWordList():
    length = int(request.args.get('length', 7))
    letters = randomLetters(length)
    wordlist = findWordList(letters)
    return jsonify({
        'letters': letters,
        'words': wordlist
    })

if __name__ == "__main__":
    from os import environ
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
