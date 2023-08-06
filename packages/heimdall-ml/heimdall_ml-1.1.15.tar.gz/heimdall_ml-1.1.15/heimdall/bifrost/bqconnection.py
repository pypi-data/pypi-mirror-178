import pandas as pd
from google.oauth2 import service_account
from heimdall.utils.logging import get_logger
from google.cloud.bigquery import Client

logger = get_logger(__name__)


class BQConnection:

    """Creates an authorised connection to BigQuery with which queries can be executed to fetch data into pandas"""

    def __init__(self, project_id: str, service_account_file_path: str):

        self.project = project_id
        self.credentials = service_account.Credentials.from_service_account_file(
            service_account_file_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = Client.from_service_account_json(service_account_file_path)

    def execute_query(self, query: str):
        response = pd.read_gbq(
            query=query,
            project_id=self.project,
            credentials=self.credentials,
            use_bqstorage_api=True,
        )
        return response

    def write_query(self, table_id, dataset, job_config):
        job = self.client.load_table_from_dataframe(
            dataset, table_id, job_config=job_config
        )
        job.result()
