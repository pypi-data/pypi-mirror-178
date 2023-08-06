from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext
import ipaddress


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        ipv4_networks = []
        text = http_cached_requests("https://www.cloudflare.com/ips-v4", cache_folder=cache_folder).decode("utf-8")
        for line in text.split("\n"):
            ipv4_networks.append(ipaddress.IPv4Network(line, strict=False))

        ipv6_networks = []
        text = http_cached_requests("https://www.cloudflare.com/ips-v6", cache_folder=cache_folder).decode("utf-8")
        for line in text.split("\n"):
            ipv6_networks.append(ipaddress.IPv6Network(line, strict=False))

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange.parse())


if __name__ == "__main__":
    main()
