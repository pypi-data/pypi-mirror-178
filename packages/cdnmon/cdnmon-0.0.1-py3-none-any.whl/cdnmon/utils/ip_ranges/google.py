import ipaddress
import json

from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        """
        [1] https://support.google.com/a/answer/10026322
        [2] https://www.gstatic.com/ipranges/goog.json
        [3] https://www.gstatic.com/ipranges/cloud.json
        :return:
        """
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        text = http_cached_requests("https://www.gstatic.com/ipranges/cloud.json", cache_folder=cache_folder).decode(
            "utf-8"
        )
        data = json.loads(text)

        ipv4_networks = []
        ipv6_networks = []
        prefixes = data["prefixes"]
        for prefix in prefixes:
            if "ipv4Prefix" in prefix:
                ipv4_networks.append(ipaddress.IPv4Network(prefix.get("ipv4Prefix"), strict=False))

            if "ipv6Prefix" in prefix:
                ipv6_networks.append(ipaddress.IPv6Network(prefix.get("ipv6Prefix"), strict=False))

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
