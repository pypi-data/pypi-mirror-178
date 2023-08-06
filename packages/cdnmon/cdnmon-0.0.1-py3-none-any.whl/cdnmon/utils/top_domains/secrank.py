import csv
import datetime
import gzip
import io
import requests
import os
import json


from cdnmon.models.abstract_top_domains import AbstractTopDomains
from cdnmon.utils.http_client import http_cached_requests


class TopDomains(AbstractTopDomains):
    @staticmethod
    def top(n, date):
        date_str = date.strftime("%Y-%m-%d")
        session = requests.Session()
        url = f"https://secrank.cn/api/topDomain/download/fqdn/{date_str}"
        cookies = {
            "SESSION": os.environ["SEC_RANK_SESSION"],
        }
        response = http_cached_requests(url, cache_folder="top_domains/secrank/api", cookies=cookies, session=session)
        oss_url = json.loads(response)["data"]
        oss_response = http_cached_requests(oss_url, cache_folder="top_domains/secrank/data", cookies=cookies)
        result = []
        reader = csv.DictReader(
            io.StringIO(gzip.decompress(oss_response).decode("utf-8")),
            fieldnames=["domain", "weight", "index"],
            delimiter="\t",
        )
        for row in reader:
            row["weight"], row["index"] = float(row["weight"]), int(row["index"])
            result.append(row)
            if len(result) >= n:
                break
        return result


def main():
    date = datetime.datetime(year=2022, month=11, day=10)
    domains = TopDomains.top(10, date)
    print(date, domains)


if __name__ == "__main__":
    main()
