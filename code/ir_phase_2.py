# -*- coding: utf-8 -*-
"""IR-phase#2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TbbE_xTNqL7R6TvXzpPjLZtDeU1UtnO5
"""

import numpy as np
import nltk
import pandas as pd
import re
nltk.download('punkt')

from google.colab import drive
import glob

drive.mount('/content/drive')

file_path = '/content/drive/MyDrive/Novels/'
file_list = glob.glob(file_path + "*")

def read_document(file_name):
  with open(file_name) as file:
    lines = file.read()
  return lines

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def tokenize_english(text):
    tokens = nltk.word_tokenize(text)
    return tokens

def normalize_english_text(tokenized_text):
    tokenized_text = [token.lower() for token in tokenized_text]
    tokenized_text = [remove_punctuation(token) for token in tokenized_text]
    return tokenized_text


def stem_english(tokens):
    tokens = [stemmer.stem(token) for token in tokens]
    filtered_tokens = [token for token in tokens if len(stemmer.stem(token))>=3]
    return filtered_tokens

def remove_punctuation(tokenized_text):
    tokens = nltk.word_tokenize(tokenized_text)
    tokens = [token for token in tokens if token.isalpha()]
    return ' '.join(tokens)

import os
queries = ['mr. Henry Dashwood had one son', 'no money for gambling', 'all through the day Miss Abbott had seemed to Philip like a goddes', 'Are bears any good at discovering it?', 'I d like a shillin', 'On a January evening of the early seventies']
df = pd.DataFrame(columns=['name', 'content'])


for item in file_list:
    file_name_output_type = os.path.basename(item)
    output, _ = os.path.splitext(file_name_output_type)
    document_content = read_document(item)
    tokenized_document = tokenize_english(document_content)
    normalized_document = normalize_english_text(tokenized_document)
    stemmed_document = stem_english(normalized_document)
    number_of_tokens = len(stemmed_document)
    df = df.append({'name': output, 'content': stemmed_document, 'number of tokens': number_of_tokens}, ignore_index=True)

for query_num in range(0,6):
  tokenized_document = tokenize_english(queries[query_num])
  normalized_document = normalize_english_text(tokenized_document)
  stemmed_document = stem_english(normalized_document)
  query_name = f'query{query_num + 1}'
  number_of_tokens = len(stemmed_document)
  df = df.append({'name': query_name, 'content': stemmed_document, 'number of tokens': number_of_tokens}, ignore_index=True)

df

from collections import defaultdict
def create_english_inverted_index(df):


  inverted_index_english = defaultdict(list)
  term_dictionary_english = defaultdict(int)

  for index, row in df.iterrows():
      document_id = index + 1
      normalized_text = row['content']

      term_count = defaultdict(int)
      for token in normalized_text:
          term_count[token] += 1

      for term, count in term_count.items():
          if term not in term_dictionary_english:
              term_dictionary_english[term] = 0
          term_dictionary_english[term] += count

          inverted_index_english[term].append((document_id, count))

  for term, postings in inverted_index_english.items():
      inverted_index_english[term] = sorted(postings, key=lambda x: x[1], reverse=True)

  with open('inverted_index_english.txt', 'w') as file:
    for term, postings in inverted_index_english.items():
        term_freq = term_dictionary_english[term]
        posting_list = [(doc_id, count) for doc_id, count in postings]
        output_line = f"({term}) : frequency = {term_freq}, posting list: {posting_list}\n"
        # print(f"({term}) : frequency = {term_freq}, posting list: {posting_list}")
        file.write(output_line)
  return inverted_index_english

english_inverted_index = create_english_inverted_index(df)

tf_df = pd.DataFrame(index=english_inverted_index.keys(), columns=range(len(df)))

for key, values in english_inverted_index.items():
    for document_num in range(len(df)):
        tf_value = 0
        for value in values:
            if value[0] == document_num + 1:
                tf_value = value[1] / df['number of tokens'][document_num]
        tf_df.at[key, document_num] = tf_value

tf_df.head(10)

idf_df = pd.DataFrame(index=english_inverted_index.keys(), columns=[0])

total_documents = len(df)
for key, values in english_inverted_index.items():
    df_value = len(values)

    # Calculate IDF using the formula: IDF = log(total_documents / (1 + DF))

    idf_value = np.log10(total_documents / (df_value))
    idf_df.at[key, 0] = idf_value

idf_df.head(10)

tf_idf_df = pd.DataFrame(index=range(len(df)), columns=english_inverted_index.keys())

for key in english_inverted_index.keys():
    for document_num in range(len(df)):
        tf_value = tf_df.at[key, document_num]
        idf_value = idf_df.at[key, 0]

        tf_idf_value = tf_value * idf_value

        tf_idf_df.at[document_num, key] = tf_idf_value

tf_idf_df

from sklearn.metrics.pairwise import cosine_similarity
cos_sim_matrix = cosine_similarity(tf_idf_df)
cos_sim_df = pd.DataFrame(cos_sim_matrix, index=tf_idf_df.index, columns=tf_idf_df.index)
cos_sim_df

query_number = int(input("Enter the query number (1 to 6): ")) - 1  # Adjusting for 0-based indexing

query_row_number = 28 + query_number
query_row = cos_sim_df[query_row_number]
top_similar_indices = query_row.nlargest(11)
top_similar_indices = top_similar_indices[1:11]

for index,cosine_value in top_similar_indices.iteritems():
  book_title = df.loc[index,'name']
  print(f"{book_title} : {cosine_value}")

def jaccard_similarity(doc1, doc2):
    intersection = sum((min(doc1[i], doc2[i]) for i in range(len(doc1))))
    union = sum((max(doc1[i], doc2[i]) for i in range(len(doc1))))
    return intersection / union

jaccard_df = pd.DataFrame(index=tf_idf_df.index, columns=tf_idf_df.index)

for doc1 in tf_idf_df.index:
    for doc2 in tf_idf_df.index:
        if doc1 != doc2:
            jaccard_df.loc[doc1, doc2] = jaccard_similarity(tf_idf_df.loc[doc1], tf_idf_df.loc[doc2])

jaccard_df = jaccard_df.fillna(1)
jaccard_df

query_number = int(input("Enter the query number (1 to 6): ")) - 1  # Adjusting for 0-based indexing

query_row_number = 28 + query_number
query_row = jaccard_df[query_row_number]
top_similar_indices = query_row.nlargest(11)
top_similar_indices = top_similar_indices[1:11]

for index,jaccard_value in top_similar_indices.iteritems():
  book_title = df.loc[index,'name']
  print(f"{book_title} : {jaccard_value}")

import pandas as pd

!wget https://github.com/mohamad-dehghani/persian-pdf-books-dataset/raw/master/final_books.xlsx

persian_df = pd.read_excel('/content/final_books.xlsx')
persian_df

persian_df = persian_df.iloc[:1000, :]
persian_df

queries = {
    'title': ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7'],
    'date': [None] * 7,
    'content': [
        'ایران در عهد باستان',
        'موضوع این کتاب',
        'دریا گسترهای بس زیبا، فریبنده و شگفت‌انگیز است',
        'روانشناسی کودک',
        'فیزیکدان معاصر استیون هاوکینگ',
        'مهارت های مطالعه برای دانش‌آموزان و دانشجویان',
        'اشکانیان از سویی دیرپاترین دودمان فرمانروای ایران و طوالنی ترین دوران تاریخ ما'
    ],
    'category': [None] * 7,
    'author': [None] * 7,
    'comments': [None] * 7
}


queries_df = pd.DataFrame(queries)

persian_df = pd.concat([persian_df, queries_df], ignore_index=True)

# Display the updated DataFrame
persian_df

persian_df.iloc[400:440]

persian_df['content'].fillna(persian_df['title'], inplace=True)

null_counts = persian_df.isnull().sum()
null_counts

persian_df['concat'] = persian_df['title'].fillna('')  + ' ' + persian_df['content'].fillna('') + ' ' + persian_df['category'].fillna('') + ' ' + persian_df['author'].fillna('')
persian_df

!pip install hazm --quiet

import hazm
from hazm import Normalizer, Stemmer, stopwords_list, WordTokenizer

normalizer = Normalizer()
stemmer = Stemmer()
persian_stopwords = set(stopwords_list())

def tokenize_persian(text):
    text = remove_punctuation_persian(text)
    tokenizer = hazm.WordTokenizer()
    tokens = tokenizer.tokenize(text)
    return tokens

def remove_punctuation_persian(text):
    text = re.sub(r'_', '\u200c', text)
    punctuation_pattern = r'[^\w\s]+'
    text = re.sub(punctuation_pattern, ' ', text)
    text = text.strip()

    return text

def normalize_persian(tokens):
    tokens = [normalizer.normalize(token) for token in tokens]
    return tokens

def stemming(tokens):
    tokens = [stemmer.stem(token) for token in tokens]
    return tokens

def remove_stopwords(tokens):
    tokens = [token for token in tokens if token not in persian_stopwords]
    return tokens

persian_df['tokenized_content'] = persian_df['concat'].apply(tokenize_persian)
persian_df['tokenized_content'] = persian_df['tokenized_content'].apply(remove_stopwords)
persian_df['normalized_content'] = persian_df['tokenized_content'].apply(normalize_persian)
persian_df['stemming_content'] = persian_df['normalized_content'].apply(stemming)

print(persian_df.loc[0,'tokenized_content'])

print(persian_df.loc[0,'normalized_content'])

print(persian_df.loc[0,'stemming_content'])

persian_df['final_content'] = persian_df['stemming_content'].apply(lambda tokens: [token for token in tokens if token and len(token) > 2])
persian_df.loc[0, 'final_content']

persian_df['number of tokens'] = persian_df['final_content'].apply(len)

persian_df

from collections import defaultdict

def create_persian_inverted_index(df):
  subset_dataset = df.head(1007)

  inverted_index = defaultdict(list)
  term_dictionary = defaultdict(int)

  for index, row in subset_dataset.iterrows():
      document_id = index + 1
      normalized_text = row['final_content']

      term_count = defaultdict(int)
      for token in normalized_text:
          term_count[token] += 1

      for term, count in term_count.items():
          if term not in term_dictionary:
              term_dictionary[term] = 0
          term_dictionary[term] += count

          inverted_index[term].append((document_id, count))

  for term, postings in inverted_index.items():
      inverted_index[term] = sorted(postings, key=lambda x: x[1], reverse=True)


  with open('inverted_index_persian.txt', 'w') as file:
    for term, postings in inverted_index.items():
        term_freq = term_dictionary[term]
        posting_list = [(doc_id, count) for doc_id, count in postings]
        output_line = f"({term}) : frequency = {term_freq}, posting list: {posting_list}\n"
        print(f"({term}) : frequency = {term_freq}, posting list: {posting_list}")
        file.write(output_line)

  return inverted_index

persian_inverted_index = create_persian_inverted_index(persian_df)

persian_inverted_index

persian_tf_df = pd.DataFrame(index=persian_inverted_index.keys(), columns=range(len(persian_df)))

for key, values in persian_inverted_index.items():
    for document_num in range(len(persian_df)):
        tf_value = 0
        for value in values:
            if value[0] == document_num + 1:
                tf_value = value[1] / persian_df['number of tokens'][document_num]
        persian_tf_df.at[key, document_num] = tf_value

persian_tf_df.head(10)

persian_idf_df = pd.DataFrame(index=persian_inverted_index.keys(), columns=[0])

total_documents = len(persian_df)
for key, values in persian_inverted_index.items():
    df_value = len(values)

    # Calculate IDF using the formula: IDF = log(total_documents / (1 + DF))

    idf_value = np.log10(total_documents / (df_value))
    persian_idf_df.at[key, 0] = idf_value

persian_idf_df

persian_tf_idf_df = pd.DataFrame(index=range(len(persian_df)), columns=persian_inverted_index.keys())

for key in persian_inverted_index.keys():
    for document_num in range(len(persian_df)):
        tf_value = persian_tf_df.at[key, document_num]
        idf_value = persian_idf_df.at[key, 0]

        tf_idf_value = tf_value * idf_value

        persian_tf_idf_df.at[document_num, key] = tf_idf_value

persian_tf_idf_df

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
cos_sim_matrix = cosine_similarity(persian_tf_idf_df)
persian_cos_sim_df = pd.DataFrame(cos_sim_matrix, index=persian_tf_idf_df.index, columns=persian_tf_idf_df.index)
persian_cos_sim_df

query_number = int(input("Enter the query number (1 to 7): "))-1   # Adjusting for 0-based indexing

query_row_number = 250 + query_number
query_row = persian_cos_sim_df[query_row_number]
query_row = query_row.iloc[:250]
top_similar_indices = query_row.nlargest(10)

for index,cosine_value in top_similar_indices.iteritems():
  book_title = persian_df.loc[index,'title']
  print(book_title , '\n, score: ', cosine_value)

def jaccard_similarity(doc1, doc2):
    intersection = np.sum(np.minimum(doc1, doc2))
    union = np.sum(np.maximum(doc1, doc2))
    return intersection / union if union != 0 else 0  # Avoid division by zero

# Assuming persian_tf_idf_df is a DataFrame with documents as rows and features as columns

# Calculate Jaccard similarity matrix
persian_jaccard_df = pd.DataFrame(index=persian_tf_idf_df.index, columns=persian_tf_idf_df.index)

# Iterate over unique pairs of documents
for i, doc1 in enumerate(persian_tf_idf_df.index):
    for j, doc2 in enumerate(persian_tf_idf_df.index):
        if i < j:
            similarity = jaccard_similarity(persian_tf_idf_df.loc[doc1], persian_tf_idf_df.loc[doc2])
            persian_jaccard_df.loc[doc1, doc2] = similarity
            persian_jaccard_df.loc[doc2, doc1] = similarity

# Fill diagonal with 1
np.fill_diagonal(persian_jaccard_df.values, 1)

persian_jaccard_df

def jaccard_similarity(doc1, doc2):
    intersection = sum((min(doc1[i], doc2[i]) for i in range(len(doc1))))
    union = sum((max(doc1[i], doc2[i]) for i in range(len(doc1))))
    return intersection / union

persian_jaccard_df = pd.DataFrame(index=persian_tf_idf_df.index, columns=persian_tf_idf_df.index)

for doc1 in persian_tf_idf_df.index:
    for doc2 in persian_tf_idf_df.index:
        if doc1 != doc2:
            persian_jaccard_df.loc[doc1, doc2] = jaccard_similarity(persian_tf_idf_df.loc[doc1], persian_tf_idf_df.loc[doc2])

persian_jaccard_df = persian_jaccard_df.fillna(1)
persian_jaccard_df

query_row_number = 1000 + query_number
query_row = persian_jaccard_df[query_row_number]
query_row = query_row.iloc[:1000]
query_row = pd.to_numeric(query_row, errors='coerce')
top_similar_indices = query_row.nlargest(10)

for index,jaccard_value in top_similar_indices.iteritems():
  book_title = persian_df.loc[index,'title']
  print(book_title , '\n, score: ', jaccard_value)

A