# Import all the essential modules.
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Variable for the file directory
books_dir = "./Books"

# Function for reading the files
def read_book(title_path):
    with open (title_path, "r", encoding="utf8") as current_file:
        text = current_file.read()
        text = text.replace("\n","").replace("\r","")
    return text

# Function for counting the number of unique words
def word_stats(word_counts):
    num_unique = len(word_counts)
    counts = word_counts.values()
    return (num_unique, counts)

# Function to count the number of words in the particular file
def count_words_fast(text):
    text = text.lower() # here we are converting every word to lower case so same word cannot be treated as different word
    skip = ['.',',',';',':','"']
    for ch in skip:  # here we are looping over the special characters to replace it with empty string so we can prevent them from counting
        text = text.replace(ch, "")
    word_counts = Counter(text.split(" "))
    return word_counts

# This is the basic structure of the table that will be formed by the values from that folder
stats = pd.DataFrame(columns = ("language","authoe","title","length","unique"))
title_num = 1

# This loop for looping through each folder and file in the given directory
for language in os.listdir(books_dir): # this loop is looping over languages
    for author in os.listdir(books_dir + "/" + language): # this loop is looping over different authors
        for title in os.listdir(books_dir + "/" + language + "/" + author): # this loop is looping over different title of the books
            inputFile = books_dir + "/" + language + "/" + author + "/" + title
            print(inputFile)
            text = read_book(inputFile)
            (num_unique, counts) = word_stats(count_words(text))
            # Here every detail get placed on the table
            stats.loc[title_num] = language, author.capitalize(), title.replace(".txt",""), sum(counts), num_unique
            title_num += 1
# Printing of the complete table
print(stats)

# Here we are ploting the data on the graph wich are obtained from above proccess
plt.figure(figsize = (10,10))
subset = stats[stats.language == "English"]
plt.loglog(subset.length, subset,unique, "o-", lable = "English", color = "crimson")
subset = stats[stats.language == "French"]
plt.loglog(subset.length, subset,unique, "o-", lable = "French", color = "forestgreen")
subset = stats[stats.language == "German"]
plt.loglog(subset.length, subset,unique, "o-", lable = "German", color = "orange")
subset = stats[stats.language == "Portuguese"]
plt.loglog(subset.length, subset,unique, "o-", lable = "Portuguese", color = "blueviolet")
plt.legend()
plt.xlable("Book length")               # Naming of the x-axis
plt.ylable("Number of unique words")    # Naming of the y-axis
plt.savefig("books.pdf")                # Saving the graph in pdf format with name of "books"
