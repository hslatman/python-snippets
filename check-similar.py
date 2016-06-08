from __future__ import print_function

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import codecs
import fnmatch
import os

DIRECTORY = "<path/to/directory/>"
LIST_FILE = "list.txt"
LIST_FILE_PATH = os.getcwd() + os.sep + LIST_FILE


class Fitter(object):

    def __init__(self):
        self.docs = []
        self.tv = None
        self.tfidf = None

    def train(self, docs=[]):
        """Trains the fitter using uni-, bi- and trigrams.

        :docs: a list containing strings to train 
        """
        self.docs = docs

        # create a TFIDF matrix based on words using unigram, bigram and trigrams
        # english stopwords are removed from the documents
        # terms occurring having a document frequency lower than min_df are ignored
        self.tv = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')

        # learn the terms and inverse document frequency of terms
        self.tfidf = self.tv.fit_transform(self.docs)

    def similar(self, doc):
        """Calculate linear kernel of doc and existing training set.
        
        :doc: a string to calculate similarities for
        """
        doc_tfidf = self.tv.transform([doc])
        cos_sim = linear_kernel(doc_tfidf, self.tfidf)

        # return only the first element: the similarity scores to this doc
        return cos_sim[0]




def setup():
    """Creates a list of documents to use for training.
    
    Change this to get a different type/list of documents
    """

    # check if we have a training file already
    if not os.path.exists(LIST_FILE_PATH):

        with open(LIST_FILE_PATH, 'w') as handle:

            # perform recursive lookup in seed folder:
            for root, dirnames, filenames in os.walk(DIRECTORY):
                # looking only for .pdf files
                for filename in fnmatch.filter(filenames, '*.pdf'):
                    # splitting off the pdf extension
                    fn_write = ".".join(filename.split('.')[:-1]).lower()
                    try:
                        fn_write.decode('utf-8')
                        handle.write(fn_write + '\n')
                    except:
                        pass
                    
    
    # get a list with all of the docs including numeric identifier
    docs = {}
    with codecs.open(LIST_FILE_PATH, encoding='utf-8') as handle:
        for id, doc in enumerate(handle.readlines()):
            docs[id] = doc

    # return the titles
    return docs


def similar_enough(similarities=[]):
    """Naive similarity threshold calculator.
    
    Similar enough when at least 3 rows in similarities 
    have a cosine similarity of 0.15 or higher.

    :similarities: list containing similarity scores
    """

    return len([s for s in similarities if s >= 0.15]) >= 3
    

def main():

    # perform setup
    titles = setup()

    # create and train an estimator
    f = Fitter()
    f.train(titles.values())

    # current doc 
    doc = "python programming"

    # retrieve the cosine similarities for each document vs the doc to lookup
    similarities = f.similar(doc)

    # check if the new doc is similar enough to the other docs
    if similar_enough(similarities):
        print("the doc '{}' looks interesting".format(doc))


if __name__ == "__main__":
    main()