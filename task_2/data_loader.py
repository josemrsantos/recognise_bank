# Insert lib imports here

class DataLoader:
    """
    Main class to handle the data loading from S3 into Redshift
    """
    def __init__(self):
        self.redshift_table_name = '' # This should be filled from the configuration
        self.redshift_table_schema = None  # To be set by check_table_redshift or create_table_schema
        self.s3_data_schema = None  # To be set by create_table_schema
        self.s3_url = ''  # This should be filled, from the configuration
        # As several commands should be run on Redshift, might as well keep a connection open
        # Note: Its important that this connection is closed, so consider transforming this into a context manager
        self.redshift_connection = None
        # Other object variables needed in the code should be added here.

    def run(self):
        """
        This is more of a rough plan on how the execution should happen. We can have either this method or run this
        logic on the __init__ method.
        To create and execute the code, it will be either:
        # If this code goes to the __init__ method
        DataLoader(parameters)
        # If we keep this method
        data_loader = DataLoader(parameters)
        data_loader.run()
        PLEASE NOTE THAT THE FOLLOWING CODE IS JUST TO GIVE A ROUGH IDEA OF THE LOGIC TO BE IMPLEMENTED
        """
        # Check if the table already exist on Redshift and if it does, get the existing schema
        table_exists = self.check_table_redshift()
        # Infers schema from S3 data
        self.create_table_schema()
        # If schemas differ, raise exception
        if table_exists and not self.invalid_schema():
            self.report_event('invalid-schema')
            raise Exception('New schema is different from existing schema')
        # else if table does not exist, create table in Redshift
        elif not table_exists:
            self.create_table()
        # Load data from the files on S3 into Redshift
        self.copy_data()
        # Report event and metrics after data is loaded
        self.report_event('data-copy-ok')
        self.report_metrics()

    def copy_data(self):
        """
        Creates the SQL for the copy command and executes it on Redshift
        :return:
        """
    def create_table(self):
        """
        Creates a new table in Redshift according to self.redshift_table_schema
        :return:
        """
        pass

    def report_metrics(self):
        """
        Method that will send metrics into CloudWatch
        e.g. lines copied into Redshift
        """
        pass

    def report_event(self, event):
        """
        Method that will send an event into CloudWatch
        :param event:
        """
        pass

    def create_table_schema(self):
        """
        Infers the schema from the data on S3 and sets that schema into the variable self.s3_data_schema
        :return:
        """
        pass

    def check_table_redshift(self):
        """
        This method should check if a table for this collection already exists on Redshift.
        :return: True if table exists, False otherwise
        """
        pass

    def invalid_schema(self):
        """
        Checks if the schema from S3 and the schema from Redshift are equal
        :return: True if they are different, False otherwise
        """
