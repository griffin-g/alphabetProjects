# wordlist downloaded from https://websites.umich.edu/~jlawler/wordlist.html -> https://websites.umich.edu/~jlawler/wordlist

import os 
import random
import string
from collections import Counter


# import "words_alpha.txt" dictionary into set dictionary
def importDictionary(filepath):
    dictionary = set()
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}")
        return
    with open(filepath, 'r') as f:
        for word in f:
            dictionary.add(word.rstrip())
    return dictionary

# generate random letters
# first letter in list is "must use" letter
def randomLetters(length):
    word = ''.join(random.sample(string.ascii_lowercase, length))
    vowels = {"a", "e", "i", "o", "u"}
    while not any(char in vowels for char in word):
        word = ''.join(random.sample(string.ascii_lowercase, length))
    letters = list(word)
    print(letters)
    return letters

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

def main():
    letters = randomLetters(7)
    wordlist = findWordList(letters, "wordlist.txt")
    print(wordlist)
    return 0

if __name__ == "__main__":
    main()