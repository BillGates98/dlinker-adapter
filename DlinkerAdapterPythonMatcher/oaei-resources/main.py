import os
import logging as log
from get_format import get_format
from handle_predicates import HandlePredicates
from compute_similars_pairs_predicates import ComputeSimilarPredicate
from compute_files import ComputeFile
import time
import argparse
import sys
import logging

from rdflib import Graph


class Main: 

    def __init__(self, source='', target='', alpha_predicate=0, keywords_predicates=''):
        self.source = source
        self.target = target
        self.output_path = './outputs/'
        self.input_files = []
        self.start_time = time.time()
        self.alpha_predicate = alpha_predicate
        self.keywords_predicates = keywords_predicates
        # log.info('###   Predicates similarities started    ###')
        
    def build_graph(self, input_file=''):
        graph = Graph()
        graph.parse(input_file, format=get_format(value=input_file))
        return graph
    
    def run(self):
        inputs = [self.source, self.target]
        graphs = [self.build_graph(input_file=self.source), self.build_graph(input_file=self.target)]
        # log.warning("Start similarity predicates protocol between datasets ...")
        dataset_predicates = []
        try :
            dataset_predicates = HandlePredicates(input_files=inputs, graphs=graphs).run()
            couples = ComputeSimilarPredicate(keywords_predicates=self.keywords_predicates, predicates=dataset_predicates, graphs=graphs, alpha_predicate=self.alpha_predicate, output_path=self.output_path).run()
        except RuntimeError:
            exit()
            # log.error("Increasing on each dataset -> Failed")
        # print("--- %s seconds ---" % (time.time() - self.start_time))
        return 0
