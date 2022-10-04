
from deep_similarity import DeepSimilarity
from get_format import get_format
from hyperparameter import Hyperparameter
from rdflib import Graph
from pyparsing import ParseException
import itertools
from decimal import *
from dump import dump
import validators
import base64
import time
import argparse
import os
import multiprocessing
from AlignmentFormat import serialize_mapping_to_tmp_file
from main import Main
import os
from six.moves import urllib

os.environ["PYTHONIOENCODING"] = "utf-8"
# scriptLocale=locale.setlocale(category=locale.LC_ALL, locale="en_GB.UTF-8")


def longest_substring_finder(string1='', string2=''):
        answer = ""
        len1, len2 = len(string1), len(string2)
        for i in range(len1):
            for j in range(len2):
                lcs_temp = 0
                match = ''
                while ((i+lcs_temp < len1) and (j+lcs_temp < len2) and string1[i+lcs_temp] == string2[j+lcs_temp]):
                    match += string2[j+lcs_temp]
                    lcs_temp += 1
                if (len(match) > len(answer)):
                    answer = match
        return answer

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False
    
def measure1_(value1='', value2='', alpha=0):
    decision = True
    mean_score = 0
    if len(value1) < 1 and len(value2) < 1:
        common_string = longest_substring_finder(string1=value1, string2=value2)
        _first_common_percent = len(common_string)/len(value1);
        _second_common_percent = len(common_string)/len(value2);
        mean_score = (_first_common_percent + _second_common_percent) / 2
        if (mean_score >= float(alpha)):
            decision = True
    return decision

def divide_chunks(l, n):
        outputs = [] 
        data = list(l)
        for i in range(0, len(data), n):
            outputs.append(data[i:i + n])
        return outputs

    
class CandidateEntityPairs:

    def __init__(self, source='', target='', similar_predicates=[], alpha=0, phi=0, level=1, output=''):
        # log.info("Candidates Entities Pairs started ")
        # self.read_similar_predicates(file_name=similar_predicates_path)
        self.predicates_pairs = similar_predicates
        self.source = source
        self.target = target
        self.output_path = './outputs/'
        self.recapitulating = {}
        self.limit = 10
        self.start_time = time.time()
        # self.local_time = datetime.now(tz.gettz())
        self.alpha = alpha
        self.phi = phi
        self.level = level
        self.output = output
        # print('----------- ', self.local_time, ' -----------')
        # log.info('###   Predicates similarities started    ###')

    def can_save_pair(self, key=''):
        _key = base64.b64encode((key).encode('utf-8')).decode('utf-8')
        if not _key in self.recapitulating:
            self.recapitulating[_key] = 0
        if _key in self.recapitulating:
            self.recapitulating[_key] += 1
            stat = self.recapitulating[_key]
            if stat >= int(self.phi):
                return True
        # self.recapitulating[_key] = 1
        return False

    def build_graph(self, input_file=''):
        graph = Graph()
        graph.parse(input_file, format=get_format(value=input_file))
        return graph

    def get_entities(self, graph=None, predicate=''):
        outputs = []
        query = """SELECT DISTINCT ?fsubject ?fobject
                    WHERE {?fsubject  :fpredicate  ?fobject .}
                """
        query = query.replace(':fpredicate', predicate)
        results = graph.query(query)
        for _predicate in results:
            if not validators.url(_predicate['fobject']):
                outputs.append((_predicate['fsubject'], _predicate['fobject']))
        return outputs

    def insert_to_graph(self, graph=None, fsubject='', ssubject=''):
        query = """INSERT DATA {  <?psubject>\t<?pobject>\t1.0  }"""
        query = query.replace('?psubject', fsubject).replace(
            '?pobject', ssubject)
        try:
            graph.update(query)
        except ParseException as _:
            pass
        return graph
    
    
    def sub_treatments(self, pairs=[], alpha=0):
        ds = DeepSimilarity(code='*')
        good_entities_pairs = []
        messages = []
        for first_so, second_so in pairs:
            fs, fo = first_so
            ss, so = second_so
            if ds.comparison_run(first=fo, second=so, alpha=alpha, level=self.level)  and self.can_save_pair(key=(fs + ss)):
                good_entities_pairs.append((fs, ss, fo, so, 1))
                message = '<' + fs + '>\t<' + ss + '>\t' + '1.0'
                print('>>>>', message)
                messages.append(message)
        return messages
    
    def treat_entities_pairs(self, entities_pairs=[], alpha=0.0):
        tmp_entities_pairs = entities_pairs
        good_entities_pairs = []
        bad_entities_pairs = []
        graph = Graph()
        print('start: treat_entities_pairs')
        if os.path.exists("./outputs/same_as_entities.nt"):
            os.remove("./outputs/same_as_entities.nt")
        messages = []
        pool = multiprocessing.Pool()
        cpu = multiprocessing.cpu_count()
        print("count of cpu : ", cpu)
        result_async = [pool.apply_async(self.sub_treatments, args =(pairs, alpha, )) for pairs in divide_chunks(tmp_entities_pairs, cpu)]
        for result_entities_pairs in result_async :
            # _res_graphs
            _results = result_entities_pairs.get()
            messages = messages + _results
            # dump().write_to_txt(file_path='./outputs/logs/links.txt', values=[message])
            # graph = self.insert_to_graph(graph=graph, fsubject=fs, ssubject=ss)
        dump().write_to_txt(file_path='./outputs/same_as_entities.nt', values=messages)
        print('end: treat_entities_pairs')
        return [graph, good_entities_pairs, bad_entities_pairs]

    def process_by_pairs_predicates(self, row=[], graphs=[]):
        entities = []
        graph = None
        good_entities_pairs = []
        bad_entities_pairs = []
        for i in range(len(graphs)):
            sub_entities = self.get_entities(graph=graphs[i], predicate=row['predicate_' + str(i+1)][0])
            entities.append(sub_entities)
        tmp_entities_pairs = itertools.product(entities[0], entities[1])
        print('process_by_pairs_predicates')
        graph, good_entities_pairs, bad_entities_pairs = self.treat_entities_pairs(entities_pairs=tmp_entities_pairs, alpha=self.alpha)
        return [graph, good_entities_pairs, bad_entities_pairs]

    def run(self):
        resulting_alignment = []
        gsource = self.build_graph(input_file=self.source)
        gtarget = self.build_graph(input_file=self.target)
        graphs = [gsource, gtarget]
        predicates = self.predicates_pairs
        # _graphs = Graph()
        # pool = multiprocessing.Pool()
        # to_delete = [self.output_path + 'good_to_validate.csv', self.output_path + 'bad_to_validate.csv']
        # for file in to_delete:
        #     if os.path.isfile(file) :
        #         os.remove(file)
        # parallel computing
        # print(predicates)
        # result_async = [pool.apply_async(self.process_by_pairs_predicates, args =(predicate, graphs, )) for predicate in predicates]
        
        for predicate in predicates:
            print(predicate)
            _, _good_entities_pairs, _ = self.process_by_pairs_predicates(predicate, graphs)
            for fs, ss, _, _, hm in _good_entities_pairs:
                resulting_alignment = resulting_alignment + [(str(fs), str(ss), '=', str(hm))]
        
        # for result_entities_pairs in result_async :
        #     # _res_graphs
        #     _, _good_entities_pairs, _bad_entities_pairs = result_entities_pairs.get()
        #     resulting_alignment = resulting_alignment + [(str(fs), str(ss), '=', str(hm)) for fs, ss, _, _, hm in _good_entities_pairs]
            # _graphs = _graphs + _res_graphs
            # dump().write_tuples_to_csv(file_name=self.output_path + 'good_to_validate', data=_good_entities_pairs, columns=['fsubject', 'ssubject', 'fobject', 'sobject', 'has_matched'])
            # dump().write_tuples_to_csv(file_name=self.output_path + 'bad_to_validate', data=_bad_entities_pairs, columns=['fsubject', 'ssubject', 'fobject', 'sobject', 'has_matched'])

        tmp_file = self.output_path + 'same_as_entities.nt'
        # _graphs.serialize(destination=tmp_file, format='nt')
        # self.local_time = datetime.now(tz.gettz())
        alignment_file_url = None
        if self.output == 'spatial':
            alignment_file_url = urllib.parse.urljoin(
                "file:", urllib.request.pathname2url(tmp_file))
            # tmp_file = self.output_path + 'refalign.rdf'
            # alignment_file_url = serialize_mapping_to_tmp_file(resulting_alignment, file=tmp_file)
        else:
            if self.output == 'spimbench':
                tmp_file = self.output_path + 'refalign.rdf'
                alignment_file_url = serialize_mapping_to_tmp_file(
                    resulting_alignment, file=tmp_file)
        return alignment_file_url


if __name__ == '__main__':
    def arg_manager():
        parser = argparse.ArgumentParser()
        # parser.add_argument("--source", type=str, default='/system/oaei-resources/inputs/spaten_hobbit/source.nt')
        # parser.add_argument("--target", type=str, default='/system/oaei-resources/inputs/spaten_hobbit/target.nt')
        parser.add_argument("--source", type=str,
                            default='./inputs/spaten_hobbit/source.nt')
        parser.add_argument("--target", type=str,
                            default='./inputs/spaten_hobbit/target.nt')
        parser.add_argument("--alpha_predicate", type=float, default=1)
        parser.add_argument("--alpha", type=float, default=0.88)
        parser.add_argument("--phi", type=int, default=1)
        parser.add_argument("--measure_level", type=int, default=2)
        return parser.parse_args()
    args = arg_manager()
    # configuration = {
    #     "hobbit_spaten": {
    #         "alpha_predicate": 1,
    #         "alpha": 0.3,
    #         "phi": 1,
    #         "measure_level": 0,
    #         "keywords_predicates": ""
    #     },
    #     "spimbench": {
    #         "alpha_predicate": 1,
    #         "alpha": 1,
    #         "phi": 1,
    #         "measure_level": 1,
    #         "keywords_predicates": "/title"
    #     }
    # }
    # params = configuration['hobbit_spaten']
    args.alpha_predicate, args.alpha, args.phi, args.measure_level, output = Hyperparameter(input_file=args.source).run()
    # params['alpha_predicate'], params['alpha'], params['phi'], params['measure_level'], 'spatial'
    dirs = ['./outputs/', './outputs/logs/', './logs/']
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)
    print(args.alpha_predicate, args.alpha, args.phi, args.measure_level, output)
    main = Main(source=args.source, target=args.target, alpha_predicate=args.alpha_predicate, keywords_predicates='/title').run()
    if len(main) > 0:
        print(main)
        print("Predicates generated ...")
        resulting_alignment = CandidateEntityPairs(source=args.source, target=args.target, similar_predicates=main, alpha=args.alpha, phi=args.phi, level=args.measure_level, output=output).run()
        print(resulting_alignment)
    else:
        print("Error happens")
    # print('file:///system/oaei-resources/inputs/spaten_hobbit/source.nt')
