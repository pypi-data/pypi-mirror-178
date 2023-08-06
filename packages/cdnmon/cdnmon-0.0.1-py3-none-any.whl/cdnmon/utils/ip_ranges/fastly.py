from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext
import ipaddress
import json


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        text = http_cached_requests("https://api.fastly.com/public-ip-list", cache_folder=cache_folder).decode("utf-8")
        data = json.loads(text)

        ipv4_networks = []
        for ipv4_prefix in data["addresses"]:
            ipv4_networks.append(ipaddress.IPv4Network(ipv4_prefix, strict=False))

        ipv6_networks = []
        for ipv6_prefix in data["ipv6_addresses"]:
            ipv6_networks.append(ipaddress.IPv6Network(ipv6_prefix, strict=False))

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange(cdn_name="fastly").parse())


if __name__ == "__main__":
    main()
