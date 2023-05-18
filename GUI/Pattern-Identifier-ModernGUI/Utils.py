import re

def find_patterns_in_text(text, pattern, ignorecase=True):
    if ignorecase:
        pattern = pattern.lower()
        text = text.lower()

    pattern_index = text.find(pattern)
    pattern_indexes = []
    while pattern_index != -1:
        pattern_indexes.append(pattern_index)
        pattern_index = text.find(pattern, pattern_index + len(pattern))
    return pattern_indexes

def remove_unwanted_chars(text):
    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    return text

def generate_keywords(big_text, max_keywords):

    for text in big_text.split("\n"):
        text = remove_unwanted_chars(text)
        words = text.split()
        lwords = len(words)
        for i in range(0, lwords - 2):
            keyword = " ".join((words[i:i+max_keywords]))
