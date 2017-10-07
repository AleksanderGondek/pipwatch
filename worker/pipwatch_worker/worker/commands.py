"""This module contains logic of running common commands within cloned project directory."""
import os
import subprocess


class Command:  # pylint: disable=too-few-public-methods
    """Encompasses logic of running any command within project cloned directory.

    Command will ensure that project directory exists.
    """

    DEFAULT_PROJECT_DIR_NAME = "projects"

    def __init__(self, project_id: int, projects_dir_name: str = None) -> None:
        """Create method instance."""
        self.project_id = project_id
        self.projects_dir_name = projects_dir_name if projects_dir_name \
            else self.DEFAULT_PROJECT_DIR_NAME

    def __call__(self, command: str, cwd: str = None) -> bytes:
        """Run given command within project directory and return standard output."""
        os.makedirs(self._project_dir_path, exist_ok=True)
        return self._execute(command=command, cwd=cwd)

    @property
    def _projects_dir_path(self) -> str:
        """Return full path to directory that should be root of all cloned projects."""
        return os.path.join(os.getcwd(), self.projects_dir_name)

    @property
    def _project_dir_path(self) -> str:
        """Return full path to directory that should contain cloned project."""
        return os.path.join(self._projects_dir_path, str(self.project_id))

    def _execute(self, command: str, cwd: str = None) -> bytes:
        """Execute given command in directory of selected project."""
        outcome = subprocess.run(args=command,
                                 cwd=self._project_dir_path if not cwd else cwd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 shell=False,
                                 check=True)

        return outcome.stdout


class Git(Command):  # pylint: disable=too-few-public-methods
    """Encompasses logic of running git command for given project.

    Command will ensure that the project is cloned.
    """

    def __init__(self, project_id: int, project_url: str, projects_dir_name: str = None) -> None:
        """Create method instance."""
        super().__init__(project_id=project_id, projects_dir_name=projects_dir_name)
        self.project_url = project_url

    def __call__(self, command: str, cwd: str = None) -> bytes:
        """Execute git command in given project repository."""
        os.makedirs(self._projects_dir_path, exist_ok=True)
        if not os.path.exists(self._project_dir_path):
            self._execute(
                command="git clone {} {}".format(self.project_url, str(self.project_id)),
                cwd=self._projects_dir_path if not cwd else cwd
            )

        return self._execute(
            command="git {}".format(command),
            cwd=self._project_dir_path if not cwd else cwd
        )


class FromVirtualenv(Command):  # pylint: disable=too-few-public-methods
    """Encompasses logic of running executables from virtualenv of given project.

    Command will ensure that the project virtualenv exists.
    """

    DEFAULT_VENV_COMMAND_NAME = "virtualenv"
    DEFAULT_VENV_DIR = "virtualenv"

    def __init__(self, project_id: int,
                 projects_dir_name: str = None,
                 venv_command_name: str = None,
                 venv_dir: str = None) -> None:
        """Create method instance."""
        super().__init__(project_id=project_id, projects_dir_name=projects_dir_name)
        self.venv_dir = venv_dir if venv_dir else self.DEFAULT_VENV_DIR
        self.venv_command_name = venv_command_name if venv_command_name \
            else self.DEFAULT_VENV_COMMAND_NAME

    @property
    def _venv_bin_directory_path(self) -> str:
        """Return relative path to virtualenv bin directory (or Scripts on Windows)."""
        bin_directory = "bin" if os.name != "nt" else "Scripts"
        return os.path.join(self.venv_dir, bin_directory)

    @property
    def _venv_creation_command(self) -> str:
        """Return shell command for creation of virtualenv."""
        command = "{virtualenv} {dir}".format(
            virtualenv=self.venv_command_name,
            dir=self.venv_dir
        )

        if os.name != "nt":
            command += " --python=python3"

        return command

    def __call__(self, command: str, cwd: str = None) -> bytes:
        """Run executable from virtualenv bin directory.

        Important: cwd parameter is ignored. Command is always run at the top of the project dir.
        """
        os.makedirs(self._project_dir_path, exist_ok=True)
        venv_full_path = os.path.join(self._project_dir_path, self.venv_dir)
        if not os.path.exists(venv_full_path):
            self._execute(
                command=self._venv_creation_command,
                cwd=self._project_dir_path
            )

        return self._execute(
            command="{cmd}".format(cmd=os.path.join(self._venv_bin_directory_path, command))
        )
