from config import Config
from get_format import get_format
from rdflib import Graph, Literal
from rdflib.namespace import RDF
from datetime import datetime
import log
from decimal import *
import math

class Hyperparameter: 

    def __init__(self, input_file=''):
        super().__init__()
        self.input_file = input_file
        self.limit = 75
    
    def build_graph(self, input_file=''):
        graph = Graph()
        graph.parse(input_file, format=get_format(value=input_file))
        return graph
    
    # def get_params(self, input_file=None):
    #     graph = self.build_graph(input_file=input_file)
    #     configuration = {
    #         "hobbit_spaten": {
    #             "alpha_predicate":1,
    #             "alpha": 0.3,
    #             "phi": 1,
    #             "measure_level": 0,
    #             "keywords_predicates": ""
    #         },
    #         "spimbench": {
    #             "alpha_predicate": 1,
    #             "alpha": 1,
    #             "phi": 1,
    #             "measure_level": 1,
    #             "keywords_predicates": "/title"
    #         }
    #     }
    #     params = None
    #     founded = False
    #     output = None
    #     for s, _, _ in graph : 
            
    #         if founded == False:
    #             if ('tomtom' in s) or ('spaten' in s) or ('hobbit' in s):
    #                 output = 'spatial'
    #                 founded = True
                
    #             if ('bbc.co.uk' in s) :
    #                 output = 'spimbench'
    #                 founded = True
    
    #         if 'bbc.co.uk' in s:
    #             params = configuration['spimbench']
    #             break
    #         if ('spaten' in s) or ('hobbit' in s) or ('tomtom' in s):
    #             params = configuration['hobbit_spaten']
    #             break
    #     return params['alpha_predicate'], params['alpha'], params['phi'], params['measure_level'], output 
        
    def get_params(self, input_file=None):
        graph = self.build_graph(input_file=input_file)
        stats = {
            'numeric': 1,
            'char': 1
        }
        i = 0
        alpha_predicate = 1
        alpha = 0
        phi = 0
        ml = 0
        output = ''
        founded = False
        for s, _, o in graph : 
            
            if founded == False:
                if ('tomtom' in s) or ('spaten' in s) or ('hobbit' in s):
                    output = 'spatial'
                    founded = True
                
                if ('bbc.co.uk' in s) :
                    output = 'spimbench'
                    founded = True
                
            if i <= self.limit :
                # 2007-01-18T12:17:00
                format_yyyymmdd = "%Y-%m-%dT%H:%M:%S"
                is_date = False
                try:
                    date = datetime.strptime(o, format_yyyymmdd)
                    is_date = True
                except ValueError:
                    pass
                if isinstance(o, Literal) and not is_date :
                    for c in o : 
                        if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                            stats['numeric'] = stats['numeric'] + 1
                        else:
                            stats['char'] = stats['char'] + 1
            else:
                break
            i = i + 1
        print(stats)
        alpha = stats['char']/stats['numeric']
        if alpha > 1 or alpha == 0 : 
            alpha = 1
        else:
            alpha, _ = math.modf(alpha)
             
        if alpha > 0 and alpha <=0.5:
            phi = 1
            ml = 0
        
        if alpha > 0.5 and alpha <=0.90 :
            phi = 2
            ml = 2
         
        if alpha > 0.90 and alpha <=1 :
            phi = 1
            ml = 1
        
        return alpha_predicate, alpha, phi, ml, output
    
    def run(self):
        return self.get_params(input_file=self.input_file) # self.get_params_hobbit(input_file=self.input_file)
        