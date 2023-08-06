from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext
import ipaddress
import json


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        text = http_cached_requests("https://api.gcorelabs.com/cdn/public-ip-list", cache_folder=cache_folder).decode(
            "utf-8"
        )
        data = json.loads(text)

        ipv4_networks = []
        ipv4_prefixes = data["addresses"]
        for ipv4_prefix in ipv4_prefixes:
            ipv4_networks.append(ipaddress.IPv4Network(ipv4_prefix, strict=False))

        ipv6_networks = []
        ipv6_prefixes = data["addresses_v6"]
        for ipv6_prefix in ipv6_prefixes:
            ipv6_networks.append(ipaddress.IPv6Network(ipv6_prefix, strict=False))

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange(cdn_name="gcore").parse())


if __name__ == "__main__":
    main()
