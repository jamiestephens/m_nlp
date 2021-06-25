## Book Recommender Engine
This project was to build a book recommender engine that took in a unique key that would identfy a book within the science fiction and speculative fiction genres, and deliver back recommendations based on shared keywords from reviews that rated the books highly. I gathered this data from Goodreads, primarily because it was easily to traverse through web scraping tools but partially because Goodreads uses a collaborative, rather than content-based, recommendation system. This meant that my engine would be able to make new recommendations based on information Goodreads wasn't previously using. I was also able to include book-specific keywords in my user information file to contextualize the cosine similarity score provided for each item.

### Design



### Data
The data was scraped from Goodreads, a literary social networking site. Up to 30 reviews of any sentiment were gathered for each book and stored, along with metadata about the book and star-based ratings for each review left. Later this data was cleaned to exclude reviews that were lower than 4 stars or impractically short. My data initially came to 76 MB but was eventually pared down to 23 MB.

### Algorithms
I used NLTK's Rapid Automatic Keyword Extraction (RAKE) library to extract the most relevant keywords. The main algorithm I used involved the cosine similarity 

### Tools
* Selenium: web scraping
* NumPy, pandas: data processing and cleaning
* Re: further data processing
* TfidVectorizer/Counter: eliminating overly common and uncommon words
* Levenshtein Distance: spellchecker
* NLTK: tokenization
* WordCloud: topic visualization
* LDA: 

### Communication

I built a wordcloud (seen below) to illustrate some of the topics that were gathered during the recommendation engine's construction. I also presented on the engine using a PowerPoint file. I also built a simple export function that provided book recommendation information for a user through an Excel file. 

![image](https://user-images.githubusercontent.com/71529189/123396703-a0281680-d56f-11eb-9449-145a53a0405a.png)

![image](https://user-images.githubusercontent.com/71529189/123410788-b210b600-d57d-11eb-9eba-5363d4366608.png)
