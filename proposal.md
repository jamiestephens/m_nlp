### Question/Need

My proposal is to develop a book recommendation system based around keyword collection and analysis from Goodreads reviews. The initial scope is to limit this analysis to science fiction novels but fantasy may be included as well if the project is enhanced by its inclusion. 

### Data Description

I'm planning on building my own data set of 1,000+ books from Goodreads using Python's Selenium library. The dataset will feature a book title along with its author, publishing year, summary, and a set of randomly selected book reviews from which I'll draw the recommendations for future reading.

### Tools

Selenium: web-scraping Goodreads

Pandas/SQLAlchemy: data storage and manipulation

Sklearn CountVectorizer, TSNE: topic modeling

NLTK word_tokenize, LancasterStemmer: NLP preprocessing

Scipy svd: singular value decomposition for matrix factorization

### MVP Goal

A topic modeling visualization with a basic NLP pipeline, and enough of the final project finished to show a basic version of the recommendation system.
