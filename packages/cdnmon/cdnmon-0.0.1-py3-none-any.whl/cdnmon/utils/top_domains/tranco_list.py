import datetime
import os

from tranco import Tranco
from cdnmon.models.abstract_top_domains import AbstractTopDomains
from cdnmon.utils.misc import get_project_root, yesterday
from cdnmon.utils.logging import logger
from cdnmon.utils.storage import save_to_minio


class TopDomains(AbstractTopDomains):
    @staticmethod
    def top(n, date):
        date_str = date.strftime("%Y-%m-%d")
        today_str = datetime.datetime.today().strftime("%Y-%m-%d")
        filepath = f"{today_str}/top_domains/tranco/{date_str}"
        cache_filepath = f"{get_project_root()}/.cache/{filepath}"
        try:
            os.makedirs(cache_filepath)
        except Exception as e:
            logger.warning(repr(e))
        minio_filepath = f"{filepath}"
        t = Tranco(cache=True, cache_dir=cache_filepath)
        save_to_minio(cache_filepath, minio_filepath)
        domains = []
        for index, item in enumerate(t.list(date_str).top(n)):
            domains.append(
                {
                    "domain": item,
                    "index": index + 1,
                }
            )
        return domains


def main():
    date = yesterday()
    domains = TopDomains.top(100, date)
    print(date, domains)


if __name__ == "__main__":
    main()
