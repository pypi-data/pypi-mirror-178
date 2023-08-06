import json
import os

from assertpy import assert_that
from typing import Dict
from pathlib import Path
from deepdriver.sdk.data_types.dataFrame import DataFrame
from deepdriver.sdk.data_types.run import Run
from deepdriver import logger
from deepdriver.sdk.interface import interface

import hashlib
TYPE_HISTOGRAM = "histogram"
TYPE_LINE = "line"
TYPE_SCATTER = "scatter"

class Chart:

    def __init__(self, data: DataFrame, chart_type: str, data_fields: Dict, label_fields: Dict=None) -> None:
        assert_that(data).is_not_none()
        assert_that(chart_type).is_not_none()
        assert_that(data_fields).is_not_none()

        self.data = data
        self.log_type = "chart"
        self.chart_type = chart_type
        self.data_fields = data_fields
        self.label_fields = label_fields if label_fields else {}

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()

        value_type = __class__.__name__
        return json.dumps({
            "log_type" : self.log_type,
            "chart_type" : self.chart_type,
            "data_fields" : self.data_fields,
            "label_fields" : self.label_fields,
            "path" : self.get_path(key_name, value_type),
        })



    def upload_file(self, run: Run, key_name: str) -> None:
        Path(self.get_local_dir_path(str(run.run_id))).mkdir(parents=True, exist_ok=True)
        value_type = __class__.__name__
        local_path = self.get_local_path(run.run_id, key_name, value_type)
        with open(local_path, "w") as f:
            json.dump(self.data.data, f)
        with open(local_path, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()

        # 저장한 파일을 Interface.py의 upoad_file을 호출하여 전송
        value_type = __class__.__name__
        root_path = self.get_root_path(run.run_id)
        path = self.get_path(key_name, value_type)
        logger.debug(f"file upload[chart] : local_path=[{local_path}], root_path=[{root_path}], path=[{path}]")

        interface.upload_file(upload_type="RUN", local_path=local_path, root_path=root_path, path=path,
                              run_id=run.run_id, artifact_id=0, last_file_yn="Y", teamName=run.team_name,
                              expName=run.exp_name, run_name=run.run_name,
                              artifact_name="", artifact_type="", artifact_digest="", entry_digest=digest,
                              entry_list=[], file_index=0)
    def get_path(self, key_name: str, value_type: str) -> str:
        return f"{key_name}.{value_type}.json"

    def get_local_dir_path(self, run_id: int) -> str:
        return os.path.join(".", "deepdriver", "run", self.get_root_path(run_id))

    def get_root_path(self, run_id: int) -> str:
        return os.path.join(str(run_id), "chart")

    def get_local_path(self, run_id: int, key_name: str, value_type: str) -> str:
        return os.path.join(self.get_local_dir_path(str(run_id)), self.get_path(key_name, value_type))