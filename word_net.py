import json
import os
import argparse
import random
from pathlib import Path
import subprocess
import pip

import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn

DATASET_DIR = '/Users/bd569421/Downloads/dict'

wn.synsets('dog')
