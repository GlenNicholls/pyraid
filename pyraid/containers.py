"""Start/stop Docker containers based on config."""

import dataclasses
import logging

from .unraid import sys_call

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Docker:
    def start(self, container: str):
        """Start container."""
        logger.info(f"Starting container '{container}'")
        sys_call(f"docker start {container}")
        logger.debug(f"Container started: '{container}'")

    def stop(self, container: str):
        """Stop container."""
        logger.info(f"Stopping container '{container}'")
        sys_call(f"docker stop {container}")
        logger.debug(f"Container stopped: '{container}'")
