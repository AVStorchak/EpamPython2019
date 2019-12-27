import argparse
import os
import sys
from urllib.parse import urlparse

parser = argparse.ArgumentParser(description='Data model trainig script',
                                 allow_abbrev=False)

parser.add_argument('model_name',
                    action='store',
                    type=str,
                    help='the model name',
                    choices=['DT', 'GB', 'PCA', 'RF'])

parser.add_argument("input_path",
                    action='store',
                    type=str,
                    help="the path to the model's input dataset")

parser.add_argument("output_path",
                    action='store',
                    type=str,
                    help="the path to the learned model storage")

parser.add_argument("-DT_mode",
                    action='store',
                    type=str,
                    help="Decision Tree algorithms",
                    choices=['ID3', 'C4.5', 'CART'])

parser.add_argument("-GB_depth",
                    action='store',
                    type=int,
                    help="tree depth for Gradient Boosting",
                    default=None)

parser.add_argument("-PCA_start_dim",
                    action='store',
                    type=int,
                    help="dimension of the start dataset \
                          for Principal Component Analysis",
                    default=None)

parser.add_argument("-PCA_end_dim",
                    action='store',
                    type=int,
                    help="dimension of the end dataset \
                          for Principal Component Analysis",
                    default=None)

parser.add_argument("-RF_tree_count",
                    action='store',
                    type=int,
                    help="count of trees for Random Forest",
                    default=None)

parser.add_argument('-c',
                    '--compression',
                    action='store',
                    type=str,
                    help='data compression algorithm',
                    choices=['zlib', 'gzip', 'bzip2', 'lzma'])

permissible_extensions = ('.csv', '.parquet', '.json',
                          '.tar.gz', '.tar.bz2', '.zip')

args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
model_name = args.model_name

if not os.path.isdir(input_path) and not input_path.endswith(permissible_extensions):
    print('Incorrect input path! Please specify a folder or a file with one of the following extensions:')
    print(*permissible_extensions)
    sys.exit()

if not os.path.isdir(output_path):
    result = urlparse(output_path)
    if result.scheme == '' or result.netloc == '':
        sys.exit('Incorrect input path! Please specify a folder or a vaild URL!')

if model_name == 'DT' and not args.DT_mode:
    sys.exit('Please provide a Decision Tree algorithm')

if model_name == 'GB' and args.GB_depth is None:
    sys.exit('Please provide a Gradient Boost depth')

if model_name == 'PCA' and (args.PCA_start_dim is None or args.PCA_end_dim is None):
    sys.exit('Please provide dimensions for Principal Component Analysis')

if model_name == 'RF' and args.RF_tree_count is None:
    sys.exit('Please provide a tree count for Random Forest')
