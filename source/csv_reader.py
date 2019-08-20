import csv
import os.path
from utils import infer_type


class CSVReader():

    '''
    This class reads the CSV file, extracts its headers and data in seperate
    variables
    :param filename: The CSV filename
    :param data: A structure containing the CSV file data
    :param keys: The CSV file headers
    :param Cols: The number of data columns
    :param Rows: The number of data rows / lines
    '''

    def __init__(self, filename):
        if(os.path.exists(filename)):
            self.filename = filename
            self.data = None
            self.keys = None
            self.values = None
            self.Cols = 0
            self.Rows = 0
        else:
            raise Exception('FILE_NOT_FOUND', 'The file does not exist in the specified path.')


    def read_file(self, delimiter=',', quotechar='"', strict=True):

        '''This function reads the CSV file

        :param delimeter: The delimiter character to use for the parsing of the CSV file
        :param quotechar: The quote char to consider while parsing the CSV file
        :param strict: A flag which indicates if the CSV file should be parsed in strict mode 
        :raises: :Exception:`EMPTY_FILE`: The CSV file has no contents
        :raises: :Exception:`INCONSISTENT_DATA`: The data is corrupted
        '''

        csv.register_dialect('parsing_dialect', delimiter=delimiter, quotechar=quotechar, strict=strict, skipinitialspace=True)
        self.data = []
        with open(self.filename, 'r') as csvfile:
            self.reader = csv.DictReader(csvfile, dialect='parsing_dialect')
            if(self.reader == None):
                raise Exception('EMPTY_FILE', 'The CSV file has no contents.')
            else:
                for row in self.reader:
                    d = []
                    idx = 0
                    for k, v in row.items():
                        if(k == '' or v == ''):
                            raise Exception('INCONSISTENT_DATA', 'The data is corrupted (row: {}, column: {}).'.format(self.Rows + 1, idx + 1))
                            
                        d.append(k)
                        d.append(v)
                        idx += 1
                    self.data.append(d)
                    self.Rows += 1

        csvfile.close()


    def extract_header_fields(self):

        '''This function extracts the header fields of the CSV file

        :raises: :Exception:`EMPTY_FILE`: The CSV file has no contents
        :raises: :Exception:`INCONSISTENT_DATA`: The number of header fields does not match the number of first line of data
        :raises: :Exception:`UNKNOWN_DATA_TYPE`: We could not infer a data type
        '''

        if(len(self.data) == 0):
            raise Exception('EMPTY_FILE', 'The CSV file has no contents.')
        else:            
            self.keys = [y for x,y in enumerate(self.data[0]) if x%2 == 0]
            self.values = [y for x,y in enumerate(self.data[0]) if x%2 != 0]
            self.Cols = len(self.keys)

            if(len(self.keys) != len(self.values)):
                raise Exception('INCONSISTENT_DATA', 'The number of header fields does not match the number of first line of data.')
            else:
                idx = 0
                for key in self.keys:
                    dtype = infer_type(self.values[idx])
                    if(dtype == None):
                        raise Exception('UNKNOWN_DATA_TYPE', 'We could not infer a data type.')

                    self.keys[idx] = (self.sanitize_column_name(key),dtype)
                    idx += 1


    def check_data_sanity(self):

        '''This function checks the number of data columns at each row the CSV file and the type of the corresponding data

        :raises: :Exception:`EMPTY_FILE`: The CSV file has no contents
        :raises: :Exception:`UNKNOWN_DATA_TYPE`: We could not infer a data type
        :raises: :Exception:`DATA_TYPE_MISMATCH`: Data type mismatch
        '''

        if(len(self.data) == 0):
            raise Exception('EMPTY_FILE', 'The CSV file has no contents.')
        else:

            for item in self.data:
                j = 0
                i = 0
                while j < self.Cols:
                    dtype = infer_type(item[j+1])
                    if(dtype == None):
                        raise Exception('UNKNOWN_DATA_TYPE', 'We could not infer a data type.')
                    elif(dtype != self.keys[i][1]):
                        raise Exception('DATA_TYPE_MISMATCH', 'Data type mismatch.')
                    else:
                        j += 2
                        i += 1

        return True


    def sanitize_column_name(self, column_name):
        
        '''This function replaces whitespaces in column name with underscores to comply with SQL requirements

        :param delimeter: The column name
        :returns: The column name with no whitespaces
        :rtype: String
        '''

        tmp = column_name.strip()
        
        idx = 0
        N = len(tmp)
        tmp_array = list(tmp)
        
        while idx < N:
            c = tmp_array[idx]
            
            if(c == ' ' or c == '\t' or c=='\n' or c== '\r'):
                tmp_array[idx] = '_'
            idx += 1    
        
        return "".join(tmp_array)
    

    

