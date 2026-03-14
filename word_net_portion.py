import json
#import nltk
#nltk.data.path.append('.')
#from nltk.corpus import wordnet as wn
#import enchant

british_ise_file_path = 'british_dictionaries/en_GB-ise.dic'
american_large_file_path = 'british_dictionaries/en_US-large.dic'
noun_file_path = 'corpora/wordnet/index.noun'
verb_file_path = 'corpora/wordnet/index.verb'
adj_file_path = 'corpora/wordnet/index.adj'

british_ise_set=set()
american_large_set = set()
adj_set = set()
noun_set = set()
verb_set = set()

""" do we need this? the sets are the exact same without it
def get_all_lemmas(file_path):
    Output all words in wordnet 
    
    words = set()


    with open (file_path, 'r') as file:
        for line in file:
            end_index = line.find("%")
            word = line[:end_index]
            #if file_contains(british_file_path, word) == False or (file_contains(british_file_path, word) == True and file_contains(american_file_path, word) == True):
                
            if word not in only_british_set:
                words.add(word)

    return words
"""

# reads through a file and generates a list of words from it
@staticmethod
def convert_to_set(file_path, set:set):
    with open (file_path, 'r') as file:
        for line in file:
            end_index = len(line)

            # for the US dictionary
            if line.find("/") != -1:
                end_index = line.find("/")

            # for the UK dictionary
            elif line.find("\t") != -1:
                end_index = line.find("\t")

            # for the wordnet dictionaries
            elif line.find(" ") != -1:
                end_index = line.find(" ") 


            word = line[:end_index]

            set.add(word)

    return set

""" do we need this? the sets are the exact samae without it
with open (british_ise_file_path, 'r') as file:
    for line in file: 
        end_index = len(line)
        if line.find("/") != -1:
            end_index = line.find("/")
        #elif line.find("\t") != -1:
            #end_index = line.find("\t")

        
        
        word1 = line[:end_index]

        word2 = word1.strip()
"""



# convert the US and UK files to sets, then lowercase every word in them
british_ise_set = {word.lower() for word in convert_to_set(british_ise_file_path, british_ise_set)}
american_large_set = {word.lower() for word in convert_to_set(american_large_file_path, american_large_set)}

# create a set with only british words
only_british_set = british_ise_set - american_large_set


# create sets fpr all of the adjectives, nouns, and verbs
adj_set = convert_to_set(adj_file_path, adj_set)
noun_set = convert_to_set(noun_file_path, noun_set)
verb_set = convert_to_set(verb_file_path, verb_set)

# combine them to create a final set
words = adj_set | noun_set | verb_set


# get rid of the british words from that final set
words = words - only_british_set





"""
def get_synonymous_terms():
    Create a dictionary of all synonymous terms
    
    # Iterate through all words
    for word in wn.all_lemma_names():
        
        # Get all sysnets for this lemma (i.e. the word, e.g. 'bank')
        synsets = wn.synsets(word)

        # Walk through all synsets
        for synset in synsets:
            
            terms = set()

            # Get the 'lemmas' (the actual word) from the synset
            lemmas = [lemma.name() for lemma in synset.lemmas()]

            # Ignore any lemma more than one word, i.e. 'zoom_out'
            for lemma in lemmas:

                # An underscore means multiple words
                if '_' in lemma:
                    continue

                terms.add(lemma)

            if len(terms) >= 4:
                print('\t' + synset.name(), end = ' ')
                print(terms)

        
        TODO:  
            Remove duplicates, .e.g.
            occidentalize.v.01 {'occidentalize', 'occidentalise', 'westernise', 'westernize'}
            occidentalize.v.01 {'occidentalize', 'occidentalise', 'westernise', 'westernize'}

            Remove british varients, e.g. 'westernise', 'westernize'
        

get_synonymous_terms()


#synset: synonym set
#hyponym: a more specific meaning of a word (spoon is a hyponum of cutlery)

def find_instances_of_noun_groups(type_of_noun, synsets):

    #Check if a noun synset is a category
    #which has more specific instances
    #dog => poodle, pitbull, ...


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


def get_ambiguous_nouns():
     Create the ambiguous_noun dictionary 
    ambiguous_nouns = {}

    # Create the type_of_noun dictionary
    type_of_noun = {}

    # Iterate through all nouns
    for word in wn.all_lemma_names(wn.NOUN):
        
        # Get all NOUN sysnets for this lemma (i.e. the word, e.g. 'bank')
        synsets = wn.synsets(word, wn.NOUN)

        # Is this ambiguous?
        find_ambiguous_nouns(ambiguous_nouns, synsets, 4)

        # How about a parent classification for a group of other words?
        find_instances_of_noun_groups(type_of_noun, synsets)

    return json.dumps(type_of_noun, indent = 4)
"""