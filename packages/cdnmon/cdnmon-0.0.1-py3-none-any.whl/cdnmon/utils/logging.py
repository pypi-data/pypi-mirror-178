import verboselogs
import coloredlogs
import logging

verboselogs.install()
logger = logging.getLogger(__name__)
coloredlogs.install(level="INFO", logger=logger)
