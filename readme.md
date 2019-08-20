# Project Description

PySQLizer allows you to easily import data from standard comma-separated file (CSV) into a standard SQL table. The software tool parses the header fields of the CSV file. Then, it constructs a SQL table structure and adds the 'INSERT INTO' instructions allowing to add the parsed data into the SQL table. So, the resulting SQL file can be imported in few clicks in most relational databases' backends.

## Getting Started

PySQLizer can be used as either a command-line tool or a library that can be called from other Python code.

### Command-Line Interface

```
>> pysqlizer-cli.py -h
Usage: pysqlizer-cli.py [-h] -i infile [-o outfile] [-t tname] [-d dbname] [-s delimiter] [-v]

optional arguments:
  -h, --help                            show this help message and exit
  -i infile, --input infile             Input CSV filename (required)
  -o outfile, --output outfile          Output SQL filename
  -t tname, --table_name tname          SQL table name
  -d dbname, --db_name dbname           SQL database name
  -s delimiter, --delimiter delimiter   CSV file delimiter
  -v, --version                         Show the program version
```

### Library

PySQLizer provides two main classes that can be called from any other Python script:

* CSV Reader `CSVReader`: it reads the CSV file and parses its data and column fields.
* SQL Generator `SQLGenerator`: it generates the SQL table structure and data insertion instruction.

The following snippet summarizes the required steps to properly read and parse the CSV file:

~~~python
    csv_reader = CSVReader(input_file)
    csv_reader.read_file(delimiter=delimiter)
    csv_reader.extract_header_fields()
    csv_reader.check_data_sanity()
~~~

Once the CSV file is read and parsed, the SQL generator class is used as following to generate the SQL file:

~~~python
    sql_generator = SQLGenerator()
    table_query = sql_generator.create_sql_table(table_name=table_name, 
                                                 columns=csv_reader.keys, 
                                                 db_name=database_name)
    insert_query = sql_generator.insert_data(tablename=table_name, 
                                             columns=csv_reader.keys, 
                                             data=csv_reader.data)
    sql_generator.save_sql_file(filename=output_file, 
                                table_structure_query=table_query, 
                                insert_query=insert_query)
~~~

## Features

The main features of PySQLizer are the following:

* Supports five data types: integer, double, boolean, datetime and string.
* Supports whitespaces in columns' names.
* Creates automatically the SQL table structure where the data is inserted.
* Allows the selection of the database and the dropping of the SQL table if already exists.
* Generates standard SQL instructions. 
* Has no special dependencies.
* Logs useful information and all errors.

## Example

In this example, we use PySQLizer in order to convert a CSV file containing the geocoordinates of some cities located in North America into a SQL source file:

```
python pysqlizer-cli.py -i data/cities.csv -t nacities -d geocoordinates
```

## Dependencies

Besides few standard Python libraries, no special dependencies are required to run PySQLizer. 

## Limitations

PySQLizer fails if the first row of the CSV file does not contain the names of columns or / and one or many columns do not contain data.

## Authors

* **Sabeur Lafi** - *Initial work* - [slafi](https://github.com/slafi)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
