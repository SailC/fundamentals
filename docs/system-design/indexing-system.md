# design a document repository

We have a lot of wikipedia document to index and
we will implement a search engine that answers queries on Wikipedia articles.

## create index
First creating the index by going through the documents

### what is our corpus
Our corpus (document collection) is Wikipedia articles.
To generate the corpus, we can write a [webcrawler](./web-crawler.md) to get the articles from Wikipedia.

### how to parse the corpus
The webpages are HTML like structure so we can identify different fields by looking at different HTML tags.
We will write our own routine to parse this structure by using regular expressions.

* case insensitive. we don’t want to index apple, Apple, and APPLE differently.
* gramma. we don’t want to index research, researches, and researching separately.
* stop words. we wouldn’t like to index words such as ‘the’, ‘a’, ‘an’ because they appear in almost every document and they don’t give us very much information about the document or the query

So, while parsing the Wikipedia articles we will perform the following operations on each page in this order:

1. Concatenate the title and the text of the page.
2. Lowercase all words.
3. Get all tokens, where a token is a string of alphanumeric characters terminated by a non-alphanumeric character. The alphanumeric characters are defined to be [a-z0-9]. So, the tokens for the word ‘apple+orange’ would be ‘apple’ and ‘orange’.
4. Filter out all the tokens that are in the stop words list, such as ‘a’, ‘an’, ‘the’.
5. Stem each token using Porter Stemmer to finally obtain the stream of terms. Porter Stemmer removes common endings from words. For example the stemmed version of the words fish, fishes, fishing, fisher, fished are all fish.

### build inverted index
an inverted index is a data structure that we build while parsing the documents that we are going to answer the search queries on.
Given a query, we use the index to return the list of documents relevant for this query.
The inverted index contains mappings from terms (words) to the documents that those terms appear in. Each vocabulary term is a key in the index whose value is its postings list
A term’s postings list is the list of documents that the term appears in.

#### single machine
We will use a Hashtable (python’s dictionary) to store the inverted index in memory.
First, we extract Document 1, Then we extract the second document, We continue like this and build our main inverted index for the whole collection.

#### map reduce

```javascript
class InvertedIndex {
    * mapper(_, value) {
      //key ? value : each line
        for (let word of value.content.split()) yield [word, value.id];
    }

    * reducer(key, values) {
      //key : term, values: doc id
      // kind1: values = [1, 2] // doc 1 doc2
      // kind2: values = [[1, [0, 2]], [2, [0, 3]]] // doc1 pos 0 & 2
        yield [key, [...new Set(values)].sort((a, b) => a - b)];
    }
}
```

![](http://www.ardendertat.com/wp-content/uploads/2011/05/index.png)

the result postings list for the term ‘web’ is `[ [1, [0, 2]], [2, [2]], [3, [1]] ]` .

Meaning, the term ‘web’ appears in document 1 in positions 0 and 2 (we start counting positions from 0), document 2 position 2, and document 3 position 1.

Each of these lists contain the document ID as the first element, and the list of occurrences of the term in that document as the second element.



## what to query
second answering the search queries using the index we created

So, what types of queries our search engine will answer? We will answer the types of queries that we use while doing search every day. Namely:

1. One Word Queries: Queries that consist of a single word. Such as movie, or hotel.
2. Free Text Queries: Queries that contain sequence of words separated by space. Such as godfather movie, or hotels in San Francisco.
3. Phrase Queries: These are more advance queries that again consist of sequence of words separated by space, but they are typed inside double quotes and we want the matching documents to contain the terms in the query exactly in the specified order. Such as “godfather movie”.

Note: we would like to keep one additional information in the postings list, the positions of term occurrences within the document. The reason is to answer the phrase queries we need positional information, because we want to check whether the terms in the query appear in the specified order. Without knowing the positions of the terms in the document, we can only check whether the query terms simply appear in a document.

## how to query
We construct the index in memory by reading the index file line by line.

The transformations performed on words of the collection, such as stemming, lowercasing, removing stopwords, and eliminating non-alphanumeric characters will be performed on the query as well. So, querying for computer or Computer is basically the same.

1. One Word Queries: The input in OWQ is a single term, and the output is the list of documents containing that term.

2. Free Text Queries: The input in FTQ is a sequence of words, and the output is the list of documents that contain any of the query terms. So, we will get the list of documents for each query term, and take the union of them.

```javascript
let terms = getQueryFromUser();
let docs = [];
for (let term of terms) {
    for (let posting of index.get(term)) docs = [...docs, ...posting];
}
docs = [...new Set(docs)];
```


## how to optimize the query result
we will also add ranking

Tf-idf is a weighting scheme that assigns each term in a document a weight based on its term frequency (tf) and inverse document frequency (idf).  The terms with higher weight scores are considered to be more important. It’s one of the most popular weighting schemes in Information Retrieval.

### term frequency (TF)
Let’s first define how term frequency is calculated for a term t in document d. It is basically the number of occurrences of the term in the document.

We can see that as a term appears more in the document it becomes more important, which is logical.

However, there is a drawback, by using term frequencies we lose positional information. The ordering of terms doesn’t matter, instead the number of occurrences becomes important

However, it doesn’t turn to be a big loss. Of course we lose the semantic difference between “Bob likes Alice” and “Alice likes Bob”, but we still get the general idea.

We can use a vector to represent the document since the ordering is not important. consider the document “computer study computer science”. The vector representation of this document will be of size 3 with values [2, 1, 1] corresponding to computer, study, and science respectively.

We can indeed represent every document in the corpus as a k-dimensonal vector, where k is the number of unique terms in that document. Each dimension corresponds to a separate term in the document.

While using term frequencies if we use pure occurrence counts, longer documents will be favored more.
To remedy this effect, we length normalize term frequencies. So, the term frequency of a term t in document D now becomes:

![](http://s0.wp.com/latex.php?zoom=2&latex=tf_%7Bt%2Cd%7D+%3D+%5Cdfrac%7BN_%7Bt%2Cd%7D%7D%7B%7C%7CD%7C%7C%7D++&bg=ffffff&fg=000&s=2)

`||D||` is known as the Euclidean norm and is calculated by taking the square of each value in the document vector, summing them up, and taking the square root of the sum.

### inverted document frequency (IDF)
We can’t only use term frequencies to calculate the weight of a term in the document, because tf considers all terms equally important. However, some terms occur more rarely and they are more discriminative than others. Suppose we search for articles about computer vision. Here the term vision gives us more information about the intent of the query, instead of the term computer. To mitigate this effect, we use inverse document frequency. Let’s first see what document frequency is. The document frequency of a term t is the number of documents containing the term:

![](http://s0.wp.com/latex.php?zoom=2&latex=df_t+%3D+N_t++&bg=ffffff&fg=000&s=2)

We are only interested in whether the term is present in a document or not, without taking into consideration the counts. It’s like a binary 0/1 counting.

The idf of a term is the number of documents in the corpus divided by the document frequency of a term. Let’s say we have N documents in the corpus, then the inverse document frequency of term t is:

![](http://s0.wp.com/latex.php?zoom=2&latex=idf_t+%3D+%5Cdfrac%7BN%7D%7Bdf_t%7D+%3D+%5Cdfrac%7BN%7D%7BN_t%7D++&bg=ffffff&fg=000&s=2)

This is a very useful statistic, but it also requires a slight modification. It’s expected that the more frequent term to be considered less important, but the factor 10 seems too harsh. Therefore, we take the logarithm of the inverse document frequencies. Let’s say the base of log is 2, than term that appears 10 times less often is considered to be around 3 times more important. So, the idf of a term t becomes:

![](http://s0.wp.com/latex.php?zoom=2&latex=idf_t+%3D+log%5Cdfrac%7BN%7D%7Bdf_t%7D++&bg=ffffff&fg=000&s=2)

This is better, and since log is a monotonically increasing function we can safely use it.

Notice that idf never becomes negative because the denominator (df of a term) is always less than or equal to the size of the corpus (N). When a term appears in all documents, its df = N, then its idf becomes log(1) = 0. Which is ok because if a term appears in all documents, it doesn’t help us to distinguish between them. It’s basically a stopword, such as “the”, “a”, “an” etc.

The important result to note is, as more rare events occur, the information gain increases. Which means less frequent terms gives us more information.

### tf-idf scoring

Let’s say we have a corpus containing K unique terms, and a document containing k unique terms. Using the vector space model, our document becomes a k-dimensional vector in a K-dimensional vector space.

* [example tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf#Example_of_tf%E2%80%93idf)

Let’s say we have a corpus containing K unique terms, and a document containing k unique terms. Using the vector space model, our document becomes a k-dimensional vector in a K-dimensional vector space. Generally k will be much less than K, because all terms in the corpus won’t appear in a single document. The values in the vector corresponding to the k terms that appear in the document will be their respective tf-idf weights, computed by the formula above. To sum everything up, we represent documents as vectors in the vector space. A document vector has an entry for every term, with the value being its tf-idf score in the document.

We will also represent the query as a vector in the same K-dimensional vector space. It will have much fewer dimensions though, since queries are generally much shorter than the documents. Now let’s see how to find relevant documents to a query. Since both the query and the documents are represented as vectors in a common vector space, we can take advantage of this. We will compute the similarity score between the query vector and all the document vectors, and select the ones with top similarity values as relevant documents to the query.

## how to cache the query
