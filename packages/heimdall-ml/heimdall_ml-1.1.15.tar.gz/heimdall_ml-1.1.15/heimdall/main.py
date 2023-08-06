from webbrowser import get
from heimdall.utils.yaml_helper import load_yaml_file
from heimdall.gulltoppr import Gulltoppr
from heimdall.bifrost.bqconnection import BQConnection
from heimdall.bifrost.utils.data_structures import (
    METRIC_CONFIG,
    get_metric_table,
    TEST_CONFIG,
    get_test_table,
)
from heimdall.utils.logging import get_logger
from pathlib import Path
import schedule
import time
import redis
import os
import json
import numpy as np

logger = get_logger(__name__)


class Heimdall:
    def __init__(self, config_path: str = "heimdall_config.yml"):
        self.heimdall_config = load_yaml_file(config_path)

        self.config_name = self.heimdall_config.get("name")

        self.models_dir = self.heimdall_config.get("models-dir")
        self.logs_dir = self.heimdall_config.get("logs-dir")

        self.slack_channel = self.heimdall_config.get("slack-channel")
        self.slack_token = self.heimdall_config.get("slack-token")

        self.schedule = self.heimdall_config.get("schedule")

        if "bigquery-project" in self.heimdall_config:
            logger.info("BigQuery account found - connecting...")
            self.project = self.heimdall_config.get("bigquery-project")
            self.service_account = self.heimdall_config.get("service-account")

            self.metric_store = self.heimdall_config.get("metric-store")
            self.test_store = self.heimdall_config.get("test-store")

            self.bigquery_connector = BQConnection(self.project, self.service_account)
            logger.info("BigQuery account connected")

        if "redis-password" in self.heimdall_config:
            logger.info("Redis password found - connecting...")
            redis_password = self.heimdall_config.get("redis-password")

            self.redis_server = redis.StrictRedis(
                host="localhost", port=6379, db=0, password=redis_password
            )
            logger.info("Redis account connected")
        else:
            self.redis_server = None

    def get_files(self):
        rootdir = Path(self.models_dir)
        file_list = [f for f in rootdir.glob("**/*.yml") if f.is_file()]
        return file_list

    def single_run(self):
        self.redis_server.execute_command("FLUSHDB")

        total_results = {}
        files = self.get_files()

        for file in files:
            gulltoppr = Gulltoppr(
                file,
                self.bigquery_connector,
                self.metric_store,
                self.test_store,
                self.redis_server,
                self.slack_channel,
                self.slack_token,
            )

            gulltoppr.run()

            run_results = gulltoppr.heimdall_results
            total_results.update(
                {run_results.get("meta").get("model_name"): run_results}
            )

            del gulltoppr

        logger.info("Saving Heimdall logs.")
        self.check_create_file(self.logs_dir, "heimdall-logs", total_results)

        metric_table_exists = self.metric_store is not None
        contains_metrics = (
            sum(
                [
                    1 if total_results.get(model).get("performance") else 0
                    for model in total_results
                ]
            )
            > 0
        )
        if metric_table_exists & contains_metrics:
            logger.info("Uploading performance metrics to BigQuery.")
            metric_table = get_metric_table(total_results)
            self.bigquery_connector.write_query(
                self.metric_store, metric_table, METRIC_CONFIG
            )

        test_table_exists = self.test_store is not None
        contains_tests = (
            sum(
                [
                    1 if total_results.get(model).get("drift") else 0
                    for model in total_results
                ]
            )
            > 0
        )
        if test_table_exists & contains_tests:
            logger.info("Uploading drift results to BigQuery.")
            test_table = get_test_table(total_results)
            self.bigquery_connector.write_query(
                self.test_store, test_table, TEST_CONFIG
            )

    def run(self):
        if self.schedule:
            self.set_schedule(self.single_run)

            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            self.single_run()

    @staticmethod
    def _fix_time(time):
        if len(time) == 4:
            time = "0" + time
        return time

    @staticmethod
    def _schedule_day_of_week(day_of_week, time):
        eval(f"schedule.every().{day_of_week}.at('{time}').do(job)")

    def set_schedule(self, job):
        if type(self.schedule) is str:
            time = self._fix_time(self.schedule)
            schedule.every().day.at(time).do(job)

        elif type(self.schedule) is list:
            for date_config in self.schedule:
                day_of_week = list(date_config.keys())[0]
                time = self._fix_time(date_config.get(day_of_week))
                self._schedule_day_of_week(day_of_week, time)

        else:
            raise ValueError("Model schedule not configured correctly.")

    @staticmethod
    def check_create_file(folder, filename, log):
        clean_name = filename.replace(" ", "_")
        logs = f"{folder}/{clean_name}.json"

        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.isfile(logs):
            os.remove(logs)

        with open(logs, "w") as f:
            f.write(json.dumps(log, cls=NpEncoder))


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
