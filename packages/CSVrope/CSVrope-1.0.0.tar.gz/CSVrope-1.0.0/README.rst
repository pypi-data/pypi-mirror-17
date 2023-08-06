################################
Comma-Separated-Values Row Operations (CSVROPE)
################################

This module provides a set of simple utilities for retrieving, manipulating and
updating data organized in rows and contained in a CSV file.

The source code for this module lives at: 

    https://github.com/thumbo/CSVrope

Please report any bugs or feature requests via the issue tracker there.


INSTALLATION DEPENDENCIES
====

The algorithms should work with Python 3.5 or later and require a few open
source Python modules.  Below are the dependencies required for the toolset with
the versions with which the algorithm was tested:
 * Python 3.5
 * Nose 1.3.7


INSTALLATION
====

This module is registered with the Python package index.

The easiest way to install the package is to use pip.
First make sure that your version of pip is up to date:

	https://pip.pypa.io/en/stable/installing/#upgrading-pip

... and then run the command:

	pip install csvrope

For additional information about how to use pip, please refer to the guide:

	https://packaging.python.org/installing/#use-pip-for-installing
	
In alternative you can also download the package from:

	http://pypi.python.org/pypi/csvrope
	
... and compile it in the usual way:

    $ python setup.py install


USAGE
====

The ``csvrope`` module contains a set of basic functions to be used in retrieving,
updating and manipulating data contained in a CSV file.

The ``csvrope`` module gives its best when the data contained in the CSV file
is organized in a "table" form, as in the following example:

	a01, Mark, 22,male, yes, 126
	
	a02, Jane, 31,female, yes, 152
	
	a03, Philip, 28,male, no, 88
	
	a04, John, 19,male, yes, 115
	
	...

+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
|             | Value 0   | Value 1   | Value 2   | Value 3   | Value 4   | Value 5   |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Row 0       | a01       | Mark      | 22        | male      | yes       | 126       |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Row 1       | a02       | Jane      | 31        | female    | yes       | 152       |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Row 2       | a03       | Philip    | 28        | male      | no        | 88        |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Row 3       | a04       | John      | 19        | male      | yes       | 115       |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+
| Row 4       | ...       | ...       | ...       | ...       | ...       | ...       |
+-------------+-----------+-----------+-----------+-----------+-----------+-----------+

In order to use the following functions, it is sufficient to import the module
within your script.

FUNCTIONS:

	append_row(filename, row)
		Append a row at the end of CSV file.

	clear(filename)
		Clear the CSV file.

	count_rows(filename)
		Return the number of rows present in the CSV file, 0 if none.

	get_row(filename, row_index)
		Return the row at row_index, from zero-index.

	get_row_value(filename, row_index, value_index)
		Return the value at value_index from the row at row_index, from zero-index.

	get_row_values(filename, row_index, values_indexes)
		Return the values at value_indexes from the row at row_index, from zero-index.

	get_rows(filename)
		Return a list containing all the rows of the CSV file.

	get_rows_value(filename, value_index)
		Return all the values at value_index from each row, from zero-index.

	get_rows_with_value(filename, value_index, value_target)
		Return a list containing all the rows that have value_target at value_index, from zero-index.

	get_rows_with_values(filename, targets)
		Return a list of lists, each containing the rows that match the targets, from zero-index.
		
		Targets: [ [value1_index, value1_target], [value2_index, value2_target], ... ]
		
		Output: [ [rows with value1 ], [rows with value2], ... ]

	overwrite_row(filename, row_index, new_row)
		Overwrite the row at row_index with the new_row, from zero-index.

	print_rows(filename)
		Print all the rows contained in the CSV file.

	write_row(filename, row)
		Clear the CSV file and write a single row.


For an account of the functionalities available from this module, 
see the tests.py module in the source code repository.


NOTES
====

The ``csvrope`` module is intended to be used in combination with 
the standard Python ``csv`` module.
