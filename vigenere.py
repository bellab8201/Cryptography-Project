#!/usr/bin/python3

import sys
from collections import Counter
import operator
import itertools

#taken from Wikipedia
letter_freqs = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.02361,
    'X': 0.00150,
    'Y': 0.01974,
    'Z': 0.00074
}

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def pop_var(s):
    """Calculate the population variance of letter frequencies in given string."""
    freqs = Counter(s)
    mean = sum(float(v)/len(s) for v in freqs.values())/len(freqs)  
    return sum((float(freqs[c])/len(s)-mean)**2 for c in freqs)/len(freqs)
def decrypt(s,key):
    cipher_decrypt =[]
    for x in range(len(s)):
        val = (ord(s[x]) - ord(key[x%len(key)])) % 26
        val += ord('A')
        cipher_decrypt.append(chr(val))
    return  "".join(cipher_decrypt)
def match_score(d_string):
    smallest = 100
    final_letter = ""
    possible_combos=[]
    c = Counter(d_string)
    c = c.most_common()[:3:1]
    for x in range(len(c)):
        possible_combos.append(c[x][0])
        num = c[x][1]
        if num !=0:
            l_freq = num/len(d_string)
            difference = abs(l_freq-letter_freqs[c[x][0]])
            if difference < smallest:
                smallest = difference
                final_letter = c[x][0]
    return smallest, final_letter, possible_combos









if __name__ == "__main__":
    # Read ciphertext from stdin
    # Ignore line breaks and spaces, convert to all upper case
    cipher = sys.stdin.read().replace("\n", "").replace(" ", "").upper()
    #cipher = sys.argv[1].replace("\n", "").replace(" ", "").upper()
    check = {}
    repeat = {}
    count = {}
    freq = {}
    test=[]
    possible={}
    final = ""
    n = 7
    #find each substring of suspected key length, also find the distance between repeats
    for i in range(0,len(cipher)):
        count[cipher[i:i+n]] = cipher.count(cipher[i:i+n])
        dist = cipher.rfind(cipher[i:i+n]) - cipher.find(cipher[i:i+n])
        if cipher[i:i+n] not in repeat.keys() and dist != 0:
            repeat[cipher[i:i+n]] = [dist]
        elif dist != 0:
            repeat[cipher[i:i + n]].append(dist)
    for k in range (0,n):
        check[k] = cipher[k::n]
    for word in check:
        for letter in alphabet:

            freq[letter] = check[word].count(letter)
        test.append(sorted(freq.items(),key=operator.itemgetter(1), reverse = True))
        freq = {}

    repeat = sorted(repeat.items(), key =operator.itemgetter(1),reverse=True)
    best_guess_lower=0
    best_key=""

    possible_combos = []
    for x in check:
        final += match_score(decrypt(check[x],"E"))[1]
        possible_combos.append(match_score(decrypt(check[x],"E"))[2])
    combos = list(itertools.product(*possible_combos))
    for combo in combos:
        best_guess = pop_var(decrypt(cipher,combo))
        if best_guess > best_guess_lower:
            best_guess_lower = best_guess
            best_key = combo
    checker = decrypt(cipher, "".join(best_key) )
    print("".join(best_key))
