import logging
import os
import subprocess
import yaml
import dask.dataframe as dd
import datetime 
import gc
import re


################
# File Reading #
################

def read_config_file(filepath): #deserialization from yaml file
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)

def col_header_val(df,table_config):
    '''
    replace whitespaces in the column
    and standardized column names
    '''
    df.columns = df.columns.str.replace(' ', '')#removing the white spaces in the column names
    df.columns = df.columns.str.replace('[#,@,&,?]', '') #removing special characters
    expected_col = list(map(lambda x: x.lower(),  table_config['columns']))
    df.columns =list(map(lambda x: x.lower(), list(df.columns)))
    if len(df.columns) == len(expected_col) and list(expected_col)  == list(df.columns):
        print("column name and column length validation passed")
        return 1
    else:
        print("column name and column length validation failed")
        mismatched_columns_file = list(set(df.columns).difference(expected_col))
        print("Following File columns are not in the YAML file",mismatched_columns_file)
        missing_YAML_file = list(set(expected_col).difference(df.columns))
        print("Following YAML columns are not in the file uploaded",missing_YAML_file)
        logging.info(f'df columns: {df.columns}')
        logging.info(f'expected columns: {expected_col}')
        return 0
