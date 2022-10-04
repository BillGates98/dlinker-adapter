from get_format import get_format
from rdflib import Graph, Literal
from datetime import datetime
from decimal import *
import math


class Hyperparameter:

    def __init__(self, input_file=''):
        super().__init__()
        self.input_file = input_file

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

    def get_objects(self, graph=None):
        query = """SELECT DISTINCT ?s ?o WHERE { ?s ?p ?o .} LIMIT 25"""
        return graph.query(query)

    def get_params(self, input_file=None):
        graph = self.build_graph(input_file=input_file)
        stats = {
            'numeric': 1,
            'char': 1
        }
        alpha_predicate = 1
        alpha = 0
        phi = 0
        ml = 0
        output = ''
        founded = False
        for _objects in self.get_objects(graph=graph):
            _tmp_subject = _objects['s']
            _tmp_object = _objects['o']
            if founded == False:
                if ('tomtom' in _tmp_subject) or ('spaten' in _tmp_subject) or ('hobbit' in _tmp_subject):
                    output = 'spatial'
                    founded = True

                if ('bbc.co.uk' in _tmp_subject):
                    output = 'spimbench'
                    founded = True

            format_yyyymmdd = "%Y-%m-%dT%H:%M:%S"
            is_date = False
            try:
                _ = datetime.strptime(_tmp_object, format_yyyymmdd)
                is_date = True
            except ValueError:
                pass
            if isinstance(_tmp_object, Literal) and not is_date:
                for c in _tmp_object:
                    if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        stats['numeric'] = stats['numeric'] + 1
                    else:
                        stats['char'] = stats['char'] + 1
        print(stats)
        alpha = stats['char']/stats['numeric']
        if alpha > 1 or alpha == 0:
            alpha = 1
        else:
            alpha, _ = math.modf(alpha)

        if alpha > 0 and alpha <= 0.5:
            phi = 1
            ml = 0

        if alpha > 0.5 and alpha <= 0.90:
            phi = 2
            ml = 2

        if alpha > 0.90 and alpha <= 1:
            phi = 1
            ml = 1

        return alpha_predicate, alpha, phi, ml, output

    def run(self):
        # self.get_params_hobbit(input_file=self.input_file)
        return self.get_params(input_file=self.input_file)
