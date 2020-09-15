# Proximity Model

I want to have a class now that will do the full service. There's the building the model with TFIDF and then there's using the model to find the closest recipe in the list and returning maybe the recipe_id along with the ingredients.

# Spacy vs NLTK

I'm learning that I can do the tokenization step with either NLTK or Spacy and I can also do stuff like part of speech tagging with both. Below are some links that compare the two tools and overall it appears that spacy is the better tool to use. One it is faster (e.g., for word tokenization but not sentance and part of speech tagging) and two it takes an object oriented operation that makes it easier for getting production level code.

* https://www.activestate.com/blog/natural-language-processing-nltk-vs-spacy/
* https://medium.com/@akankshamalhotra24/introduction-to-libraries-of-nlp-in-python-nltk-vs-spacy-42d7b2f128f2#:~:text=NLTK%20is%20a%20string%20processing,spaCy%20uses%20object%2Doriented%20approach.&text=As%20we%20can%20see%20below,sentence%20tokenization%2C%20NLTK%20outperforms%20spaCy.
* https://medium.com/@makcedward/nlp-pipeline-word-tokenization-part-1-4b2b547e6a3

I want to now switch out my code to use spacy instead. 

* https://blog.ekbana.com/nlp-for-beninners-using-spacy-6161cf48a229
* https://stackabuse.com/python-for-nlp-tokenization-stemming-and-lemmatization-with-spacy-library/

## Whoops

So the spacy code was taking too long to run. It seems this may mostly have to do with the position tagging to get whether or not somethign is a verb. So I went back to my old code but maybe in the future I can implement some of the verb type stuff + do a better job with the timing.
