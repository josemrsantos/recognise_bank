# Insert lib imports here

class DMSException(Exception):
    pass

class DataExtractor:
    """
    Main class to handle the data loading from MongoDB into S3
    """
    def __init__(self):
        self.mongodb_server = ''  # This should be filled from the configuration
        self.mongodb_collection = '' # This should be filled from the configuration
        self.s3_url = ''  # This should be filled from the configuration. Inferred from the collection and server names?
        self.task_config = None
        # Other object variables needed in the code should be added here.

    def run(self):
        """
        This is more of a rough plan on how the execution should happen. We can have either this method or run this
        logic on the __init__ method.
        To create and execute the code, it will be either:
        # If this code goes to the __init__ method
        DataExtractor(parameters)
        # If we keep this method
        data_extractor = DataExtractor(parameters)
        data_extractor.run()
        PLEASE NOTE THAT THE FOLLOWING CODE IS JUST TO GIVE A ROUGH IDEA OF THE LOGIC TO BE IMPLEMENTED
        """
        # Prepare a DMS task config
        self.prepare_dms_task_config()
        # Execute a DMS task to extract a MongoDB collection into
        try:
            output_from_dms = self.execute_dms_task()
        except DMSException as e:
            self.report_event('data-extract-failed')
        else:
            self.report_metrics(output_from_dms)
        self.report_event('data-extract-success')

    def report_metrics(self, value):
        """
        Method that will send metrics into CloudWatch
        e.g. lines copied into Redshift
        :param value:
        """
        pass

    def report_event(self, event):
        """
        Method that will send an event into CloudWatch
        :param event:
        """
        pass

    def prepare_dms_task_config(self):
        """
        Prepares the DMS task config for exporting from a given collection into S3
        """
        pass

    def execute_dms_task(self):
        """
        Executes the DMS task to export from a given collection into S3
        :return: the output from the DMS task execution
        """