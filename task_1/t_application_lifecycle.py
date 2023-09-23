import csv
from datetime import datetime
import argparse


class TransformApplicationLifecycle:

    def __init__(self,
                 in_file_name='input.csv',
                 out_file_name='output.csv',
                 id_column='UniqueID',
                 string_column='string_agg',
                 forced_headers=None):
        """
        Constructor method. This will set some object variables that we will need in the transformation
        :param in_file_name: Input file name/path
        :param out_file_name: Output file name/path
        :param id_column: Header of the column that contains the id
        :param string_column: Header of the column that contains the string that we will need to process
        :param forced_headers: If we know beforehand the headers that will be created, and we need them in that order
        """
        self.in_file_name = in_file_name
        self.out_file_name = out_file_name
        self.id_column = id_column
        self.string_column = string_column
        self.forced_headers = forced_headers
        self.headers = [self.id_column]  # This will hold all possible column names. We know that id_column will be one.
        self.data = []  # each element of the list will be a dictionary with the column name as the key
        # We create the result list (this will hold the "final" result) with the headers
        self.result = [self.headers]


    @staticmethod
    def unique_column_name(columns, name):
        """
        This method is related with the Transformation class itself, so it should stay inside it as a static method.
        Finds repeated names and returns a unique name (by adding a counter at the end of the name)
        Note: This would be a good candidate to create a different class/object to hold and manage unique names
        :param columns: Current rows dictionary (to find repeated column names)
        :param name: The name that we need to find a unique name for
        :return: a string with a unique name
        """
        # If name not in row_columns yet, set it to 0
        # otherwise, increase by 1
        columns[name] = columns.get(name, -1) + 1
        return f'{name}_{columns[name]}'

    def fetch_data(self):
        with open(self.in_file_name, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter=',')
            for row in csvreader:
                # This will hold the existing headers in this row, to handle the cases where the same name appears more than once
                row_columns = {}
                id_value = row[self.id_column]
                data_row = {self.id_column: id_value}
                string_value = row[self.string_column]
                # Next, we use a list comprehension to get the headers and respective values in a list of tuples
                # Given an input like: 'column1]value1|column2]value2|column1]value3'
                # We get as a result: [(column1,value1),(column2,value2),(column1,value3)]
                row_raw_values = [(i.split(']')[0], i.split(']')[1]) for i in string_value.split('|')]
                # We than need to convert [(column1,value1),(column2,value2),(column1,value3)]
                # To the final: [{column1_0: value1},{column2_0: value2},{column1_1: value3}]
                for i in row_raw_values:
                    column_name = self.unique_column_name(row_columns, i[0])
                    value = i[1] + ':00'  # Adding ':00' so that we can read the timestamp more easily
                    # Process the timestamp string to the required output format
                    value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f%z').strftime('%b %d %Y, %H:%M:%S')
                    # Add this column_name / value to the current row
                    data_row[column_name] = value
                    # Add column_name to headers
                    if column_name not in self.headers:  # This is ok as long as the dataset is fairly small
                        self.headers.append(column_name)
                self.data.append(data_row)

    def transform(self):
        # Are we forcing the header list?
        if self.forced_headers is not None:
            # Make sure that in the forced_headers we have the same headers that we found in the data
            if sorted(self.forced_headers) != sorted(self.headers):
                raise Exception('Forced headers are not the same as the headers found on the data.')
            self.headers = self.forced_headers
        self.result = [self.headers]
        # Add all rows to self.result
        for row in self.data:
            new_row = {i: row.get(i, '') for i in self.headers}
            new_row_iter = [new_row[i] for i in new_row]
            self.result.append(new_row_iter)

    def output_result(self):
        with open(self.out_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerows(self.result)


def eval_forced_headers(forced_headers_str):
    """
    Expects either a Null or a valid Python expression of a list of strings. Throws a SyntaxError Exception otherwise.
    :param forced_headers_str: A string that should contain a valid Python expression of a list of strings
    :return: A valid python object, that should be a list of strings
    """
    if not forced_headers_str:
        return None
    forced_headers = eval(forced_headers_str)
    return forced_headers


def main():
    # Fetch (optional) arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file_name',
                        required=False,
                        help='Input file name (or full path)',
                        default='CC Application Lifecycle.csv',
                        type=str)
    parser.add_argument('--out_file_name',
                        required=False,
                        help='Output file name (or full path)',
                        default='result.csv',
                        type=str)
    parser.add_argument('--header',
                        required=False,
                        help='A string representing a valid Python of a list of strings. This will force a given list '
                             'of headers and therefore is only useful if we already know the columns and want to set a '
                             'given order. See Readme.md for an example of how to use this argument.',
                        default='',
                        type=str)
    args = parser.parse_args()
    # Process the header argument
    forced_headers_str = args.header
    forced_headers_str = ("['UniqueID','REGISTERED_0','ACKNOWLEDGED_0','APPROVED_0','REACKNOWLEDGED_0','CLOSED_0', "
                      "'APPOINTMENT_SCHEDULED_0','REJECTED_0','ON_HOLD_0','BLOCKED_0','TERMINATE_0','INITIATED_0', "
                      "'APPROVED_1','ON_HOLD_1','INITIATED_1','REGISTERED_1','BLOCKED_1','CLOSED_1','APPROVED_2']")
    forced_headers = eval_forced_headers(forced_headers_str)
    transformation = TransformApplicationLifecycle(in_file_name=args.in_file_name,
                                                   out_file_name=args.out_file_name,
                                                   forced_headers=forced_headers)
    # Read the data
    transformation.fetch_data()
    # Process it
    transformation.transform()
    # Output the result
    transformation.output_result()
    # I have opted to have these methods being called outside the class constructor method as that makes testing just a
    # bit easier to write and understand.


if __name__ == '__main__':
    main()


