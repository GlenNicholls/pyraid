"""Script utilities."""

import dataclasses
import logging
import json
import shlex
import subprocess

from pathlib import Path

logger = logging.getLogger(__name__)


ROOT = Path(__file__).parent.resolve()


@dataclasses.dataclass
class SysCallMetadata:
    command: str
    """Command that was run."""

    successful: bool
    """True if the command was successful."""

    error_msg: str
    """Error message for the call."""


def parse_json(file: Path) -> dict:
    """Parses JSON file and returns config object."""

    logger.debug(f"Parsing config from file '{file}'")
    with open(file) as f:
        data = json.load(f)

    return data


def _sys_call_wrap(command: str) -> SysCallMetadata:
    """Run a system call and return metadata with info about the call."""
    logger.debug(f"Running the following system call: {command}")
    proc = subprocess.run(shlex.split(command), capture_output=True, text=True)

    def fmt(arg: str) -> str:
        return "\n\t " + arg.lstrip().rstrip().replace("\n", "\n\t ")

    # Re-format stdout/stderr for logging.
    stdout = fmt(proc.stdout)
    stderr = fmt(proc.stderr)
    logger.debug(stdout)

    # Log error when call fails.
    err_msg = ""
    if proc.returncode !=0:
        err_msg = (
            f"System call '{command}' failed with non-zero exit code"
            f" ({proc.returncode}). \n stdout: {stdout} \n stderr: {stderr}"
        )
        logger.error(err_msg)

    return SysCallMetadata(
        command=command,
        successful=proc.returncode == 0,
        error_msg=err_msg,
    )
