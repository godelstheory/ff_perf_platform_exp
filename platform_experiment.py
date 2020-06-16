from mozanalysis.experiment import Experiment

platform_metric_list = [

]

class PlatformExperiment():

    def __init__(self, experiment_slug, start_date, num_dates_enrollment, additional_metrics, bq_context):
        self.experiment = (experiment_slug, start_date, num_dates_enrollment)
        self.metric_list = platform_metric_list + additional_metrics
        self.bq_context = bq_context

    def analyze_full_obs(self):
        """"
        * single window
        * time-series windows
        """
        pass

    def generate_report(self):
        """Generate the final report.

        * RMD file with corresponding dataset(s)
          - Fire off a command to generate within R?



        """
        pass








