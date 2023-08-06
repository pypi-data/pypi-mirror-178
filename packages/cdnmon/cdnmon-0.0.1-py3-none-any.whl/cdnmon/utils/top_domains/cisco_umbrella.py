import csv
import io
import zipfile

from cdnmon.models.abstract_top_domains import AbstractTopDomains
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import yesterday


class TopDomains(AbstractTopDomains):
    @staticmethod
    def top(n, date):
        """
        [1] https://umbrella-static.s3-us-west-1.amazonaws.com/index.html
        """
        date_str = date.strftime("%Y-%m-%d")
        url = f"http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-{date_str}.csv.zip"
        response = http_cached_requests(url, cache_folder=f"top_domains/cisco_umbrella/{date_str}")
        result = []
        z = zipfile.ZipFile(io.BytesIO(response))
        reader = csv.DictReader(
            io.StringIO(z.read("top-1m.csv").decode("utf-8")),
            fieldnames=["index", "domain"],
        )
        for row in reader:
            row["index"] = int(row["index"])
            result.append(row)
            if len(result) >= n:
                break
        return result


def main():
    date = yesterday()
    domains = TopDomains.top(10, date)
    print(date, domains)


if __name__ == "__main__":
    main()
