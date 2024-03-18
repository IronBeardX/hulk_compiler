import os
from hulk_definitions.token_def import LEXER
from hulk_definitions.grammar import G
from parser_gen.parser_lr1 import LR1Parser as My_Parser
from tools.evaluation import evaluate_reverse_parse
from cmp.tools.parsing import LR1Parser

import sys,logging

logger = logging.getLogger(__name__)

sys.setrecursionlimit(100000)

def main(debug = True, verbose = False):
    file_path = './hulk_compiler.log'

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"The file {file_path} has been deleted.")

    if debug:
        logging.basicConfig(filename='hulk_compiler.log', level=logging.DEBUG)
        files = os.listdir('./hulk_examples')
        logger.info('Program Started')
        for file in files:
            with open(f'./hulk_examples/{file}', 'r') as f:
                logger.info(f'=== Reading file: {file} ===')
                text = f.read()
                logger.info('=== Generating Parser ===')
                # parser = LR1Parser(G, True)
                my_parser = My_Parser(G)
                logger.info('=== Generating Lexer ===')
                tokens = LEXER(text)
                right_parse, operations = my_parser(tokens)
                print(right_parse)
                # ast = evaluate_reverse_parse(right_parse, operations, tokens)

if __name__ == "__main__":
    main()