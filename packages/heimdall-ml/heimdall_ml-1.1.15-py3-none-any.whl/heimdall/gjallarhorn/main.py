import json
import redis
import streamlit as st
from heimdall.utils.logging import get_logger
from heimdall.utils.yaml_helper import load_yaml_file
from heimdall.gjallarhorn.streamlit import (
    drift_monitor_page,
    performance_monitor_page,
    systems_monitor_page,
    home_page,
)
from streamlit_option_menu import option_menu

logger = get_logger(__name__)


class Gjallarhorn:
    def __init__(self, config_path: str = "heimdall_config.yml"):
        self.heimdall_config = load_yaml_file(config_path)

        self.config_name = self.heimdall_config.get("name")
        self.logs_dir = self.heimdall_config.get("logs-dir")

        self.schedule = self.heimdall_config.get("schedule")

        try:
            with open(self.logs_dir + "/heimdall-logs.json", "r") as json_data:
                heimdall_results = json.load(json_data)
        except:
            raise ValueError("Could not find results logs")

        self.models = list(heimdall_results.keys())
        self.load_data_logs = sum(
            [
                1
                if heimdall_results.get(model).get("meta").get("output_data_logs")
                else 0
                for model in heimdall_results
            ]
        )

        st.set_page_config(page_title=f"Heimdall", layout="wide", page_icon="👁")

        if self.load_data_logs:
            redis_password = self.heimdall_config.get("redis-password")
            self.redis_server = redis.StrictRedis(
                host="localhost", port=6379, db=0, password=redis_password
            )
        else:
            self.redis_server = None

        self.create_site(heimdall_results)

    def create_site(
        self,
        heimdall_results=None,
    ):
        selected_model = st.sidebar.selectbox("Select a model", self.models)

        run_drift_monitor = "drift" in heimdall_results.get(selected_model)
        run_performance_monitor = "performance" in heimdall_results.get(selected_model)
        run_systems_monitor = "systems" in heimdall_results.get(selected_model)

        page_names_to_funcs = {
            "Home": home_page,
            "Drift Monitor": drift_monitor_page,
            "Performance Monitor": performance_monitor_page,
            "Systems Monitor": systems_monitor_page,
        }

        page_name_icons = {
            "Home": "house-door-fill",
            "Drift Monitor": "exclamation-octagon-fill",
            "Performance Monitor": "easel2-fill",
            "Systems Monitor": "eyeglasses",
        }

        if not run_drift_monitor:
            page_names_to_funcs.pop("Drift Monitor")
            page_name_icons.pop("Drift Monitor")

        if not run_performance_monitor:
            page_names_to_funcs.pop("Performance Monitor")
            page_name_icons.pop("Performance Monitor")

        if not run_systems_monitor:
            page_names_to_funcs.pop("Systems Monitor")
            page_name_icons.pop("Systems Monitor")

        selected_page = option_menu(
            None,
            list(page_names_to_funcs.keys()),
            icons=list(page_name_icons.values()),
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )

        page_names_to_funcs[selected_page](
            selected_model, heimdall_results, self.redis_server
        )
