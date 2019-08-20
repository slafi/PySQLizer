import argparse
import time

from pathlib import Path
from logger import get_logger
from csv_reader import CSVReader
from utils import infer_type, clear_console
from sql_generator import SQLGenerator


if __name__ == "__main__":

    ## Clear console
    clear_console()

    ## get logger
    logger = get_logger('pysqlizer')

    # Parse command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', type=str, default='', help='Input CSV filename', metavar='infile', required=True)
    parser.add_argument('-o', '--output', type=str, default='', help='Output SQL filename', metavar='outfile')
    parser.add_argument('-t', '--table_name', type=str, default='', help='SQL table name', metavar='tname')
    parser.add_argument('-d', '--db_name', type=str, default='', help='SQL database name', metavar='dbname')
    parser.add_argument('-s', '--delimiter', type=str, default='', help='CSV file delimiter', metavar='delimiter')
    parser.add_argument('-v', '--version', help='Show the program version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    #print(args)
    logger.info('Starting PySQLizer...')

    # Get arguments
    input_file = args.input
    output_file = args.output
    table_name = args.table_name
    database_name = args.db_name
    delimiter = args.delimiter if args.delimiter else ','
   
    ## Check input file (type, existence and extension)
    infile = Path(input_file)
    if infile.is_dir():
        logger.error('The file {} is a directory!'.format(input_file))
        quit()

    if not infile.exists():
        logger.debug('The file {} does not exist!'.format(input_file))
        quit()

    if not infile.suffix.lower() == '.csv':
        logger.error('The extension of the file {} is not CSV!'.format(input_file))
        quit()  

    if output_file == '':
        output_file = infile.stem

    if table_name == '':
        table_name = 'tname'

    try:
        
        logger.info('Reading CSV file: {}'.format(input_file))
        start_time = time.perf_counter()

        ## Create CSV reader instance
        csv_reader = CSVReader(input_file)        
        csv_reader.read_file(delimiter=delimiter)
        csv_reader.extract_header_fields()
        csv_reader.check_data_sanity()

        end_time = time.perf_counter()
        logger.info('Elapsed time: {}s'.format(end_time-start_time))

        logger.info('Generating SQL instructions...')
        start_time = time.perf_counter()

        ## Create SQL generator instance
        sql_generator = SQLGenerator()        
        table_query = sql_generator.create_sql_table(table_name=table_name, columns=csv_reader.keys, db_name=database_name)
        insert_query = sql_generator.insert_data(tablename=table_name, columns=csv_reader.keys, data=csv_reader.data)
        
        end_time = time.perf_counter()
        logger.info('Elapsed time: {}s'.format(end_time-start_time))

        logger.info('Saving SQL file: {}'.format(output_file + '.sql'))
        start_time = time.perf_counter()

        sql_generator.save_sql_file(filename=output_file, table_structure_query=table_query, insert_query=insert_query)

        end_time = time.perf_counter()
        logger.info('Elapsed time: {}s'.format(end_time-start_time))

    except Exception as e:
        logger.error('{}'.format(e.args))
