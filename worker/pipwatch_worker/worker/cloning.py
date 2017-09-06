"""This module contains operations related to cloning project operations."""
import subprocess


def clone(project_name: str, project_url: str) -> None:
    """Clone given git repository into given directory (project name)."""
    subprocess.run("git",
                   args=["clone", project_url, project_name],
                   cwd="",
                   shell=False,
                   check=True)
