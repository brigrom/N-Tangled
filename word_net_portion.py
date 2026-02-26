
#import os
#import argparse
#import random
#from pathlib import Path
#import subprocess
#import pip

import json
import nltk
nltk.data.path.append('/Users/bd569421/Downloads/dict')
#nltk.download('wordnet')
from nltk.corpus import wordnet as wn

#DATASET_DIR = '/Users/bd569421/Downloads/dict'

#print(wn.synsets('dog'))

def find_instances_of_noun_groups(type_of_noun, synsets):
    """
    Check if a noun synset is a category
    which has more specific instances
    dog => poodle, pitbull, ...
    """

    # Get all the individual synsets
    for synset in synsets:
  
        # Do we have, say, types of dogs?
        types_of_stuff = synset.hyponyms()

        # group_name is the actual word, ignore noun phrases (words with an _)
        group_name = synset.name().split('.')[0]

        # Each synset here is a specific instance
        for specific_synset in types_of_stuff:
      
            # Get the 'lemma' (the actual word) from the synset
            names = [lemma.name() for lemma in specific_synset.lemmas()]

	    # There needs to be at least four of these to get a set
            if len(names) >= 4:

                # Add to the dictionary
                type_of_noun[synset.name()] = {}
                type_of_noun[synset.name()]['group_name'] = group_name
                type_of_noun[synset.name()]['definition'] = specific_synset.definition()
                type_of_noun[synset.name()]['names'] = names


def find_ambiguous_nouns(ambiguous_noun, synsets, threshold):
    """
    Store nouns that have multiple senses
    """

    # How many synsets are there?
    if len(synsets) > threshold:

        # Do something here about these
        pass



# Create the ambiguous_noun dictionary
ambiguous_noun = {}

# Create the type_of_noun dictionary
type_of_noun = {}

# Iterate through all nouns
for word in wn.all_lemma_names(wn.NOUN):
        
    # Get all NOUN sysnets for this lemma (i.e. the word, e.g. 'bank')
    synsets = wn.synsets(word, wn.NOUN)

    # Is this ambiguous?
    find_ambiguous_nouns(ambiguous_noun, synsets, 2)

    # How about a parent classification for a group of other words?
    find_instances_of_noun_groups(type_of_noun, synsets)

print(json.dumps(type_of_noun, indent = 4))
