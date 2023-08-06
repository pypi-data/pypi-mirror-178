"""Main module."""
import requests
import os
import zipfile
from fire import Fire
from typing import Dict
from os import environ as env
from loguru import logger

class GitLabArtifactsDownloader:
    def __init__(self, config_vars: Dict):
        self.header = {
            "PRIVATE-TOKEN": config_vars.get('GITLAB_ACCESS_TOKEN')
        }

    def get_pipelines(self, project_id: str, branch_name: str) -> str:
        """

        :param project_id:
        :param branch_name:
        :return:
        """
        param = {
            "ref": branch_name,
            "status": "success"
        }
        url = f'https://gitlab.com/api/v4/projects/{project_id}/pipelines'
        req = requests.get(url, headers=self.header, params=param)
        if req.status_code == 200:
            return req.json()
        else:
            logger.error(req.status_code)
            logger.error(req)


    def get_pipeline_jobs(self, project_id: str, pipeline_id: str) -> Dict:
        """

        :param project_id:
        :param pipeline_id:
        :return:
        """
        param = {
            "scope": "success"
        }
        url = f'https://gitlab.com/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs'
        req = requests.get(url, headers=self.header, params=param)
        if req.status_code == 200:
            return req.json()
        else:
            logger.error(req.status_code)
            logger.error(req)
    def download_file(self, url: str, header: Dict, local_file_name: str = 'artifacts.zip') -> str:
        """

        :param url:
        :param header:
        :param local_file_name:
        :return:
        """
        # NOTE the stream=True parameter below
        with requests.get(url, headers=header, stream=True) as r:
            r.raise_for_status()
            with open(local_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_file_name

    def unzip_file(self, path_to_zip_file: str):
        """

        :param path_to_zip_file:
        """
        logger.info(path_to_zip_file)
        folder_name = ".".join(os.path.basename(path_to_zip_file).rsplit('.')[:-1])
        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(folder_name)

    def download_pipeline_artifacts(self, project_id: str, branch_name: str, stage_name: str) -> None:
        """

        :param project_id:
        :param branch_name:
        :param stage_name:
        """
        logger.info("Getting pipeline info")
        pipeline_data = self.get_pipelines(project_id, branch_name)
        if len(pipeline_data) > 0:
            pipeline_data = sorted(pipeline_data, key=lambda d: d['updated_at'])
            pipeline_id = pipeline_data[-1].get('id')
        else:
            logger.error("Pipelines not found")
            return

        logger.info("Getting job info")
        job_data = self.get_pipeline_jobs(project_id, pipeline_id)
        downloaded_file = False

        for d in job_data:
            if d.get('name') == stage_name:
                job_id = d.get('id')
                url = f"https://gitlab.com/api/v4/projects/{project_id}/jobs/{job_id}/artifacts"
                logger.info("Downloading artifacts file")
                file_name = self.download_file(url, self.header)
                downloaded_file = True

        if downloaded_file:
            logger.info(f"Unzipping artifacts to {file_name}")
            self.unzip_file(file_name)


if __name__ == "__main__":
    dl = GitLabArtifactsDownloader(env.copy())
    Fire({"download_pipeline_artifacts": dl.download_pipeline_artifacts})
