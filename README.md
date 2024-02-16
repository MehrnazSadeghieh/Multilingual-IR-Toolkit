# Multilingual Information Retrieval Toolkit

This project focuses on implementing various information retrieval techniques on Persian and English datasets. We perform preprocessing, compute TF, IDF, and TF-IDF, and implement cosine similarity and Jaccard coefficient for document-query pairs.

## Datasets

- Persian Dataset: [Download here](https://github.com/mohamad-dehghani/persian-pdf-books-dataset/raw/master/final_books.xlsx)
- English Dataset: [Here](https://drive.google.com/drive/folders/1sypIfC03ZnnY9YmOffOYFIU3n5x95nuT)
  you have to create a shortcut in your google drive account and mount it in your google colab.

## Preprocessing

We utilized the Hazm library for Persian and NLTK for English to perform the following preprocessing steps on both datasets:

- Normalization
- Stemming
- Tokenization
- Removal of words with a length less than 3 after stemming

## TF, IDF, and TF-IDF Computation

TF (Term Frequency), IDF (Inverse Document Frequency), and TF-IDF (Term Frequency-Inverse Document Frequency) are computed based on the posting list generated in the [Boolean retrieval system assignment](https://github.com/negjafari/boolean-retrieval-system).

## Cosine Similarity

Cosine similarity scores for document-query pairs are calculated using the sum of TF-IDF values of common words in the query and the document. The documents are then ranked based on cosine similarity, and the top 10 documents are displayed.

## Jaccard Coefficient

Jaccard coefficient is calculated as the intersection of sets A and B divided by the union of A and B for document-query pairs.

## Queries

### English Queries:

𝑄1: "Mr. Henry Dashwood had one son" <br>
𝑄2: "no money for gambling" <br>
𝑄3: "All through the day Miss Abbott had seemed to Philip like a goddess" <br>
𝑄4: "Are bears any good at discovering it?" <br>
𝑄5: "I'd like a shilling" <br>
𝑄6: "On a January evening of the early seventies" <br>

### Persian Queries:

𝑄1: "ایران در عهد باستان" <br>
𝑄2: "موضوع این کتاب" <br>
𝑄3: "دریا گسترهای بس زیبا، فریبنده و شگفتانگیز است" <br>
𝑄4: "روانشناسی کودک" <br>
𝑄5: "فیزیکدان معاصر استیون هاوکینگ" <br>
𝑄6: "مهارتهای مطالعه برای دانشآموزان و دانشجویان" <br>
𝑄7: "اشکانیان از سویی دیرپاترین دودمان فرمانروای ایران و طولانیترین دوران تاریخ ما" <br>

## Contact Us

We're excited to hear from you! If you have any questions, suggestions, or need assistance, don't hesitate to reach out. Feel free to contact us via email at:

- neg.jaafari@gmail.com
- noorbakhsha1@gmail.com
- Mehrnaz271380@gmail.com

We're here to help and would love to hear about your experience using this project.
