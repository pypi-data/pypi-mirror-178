from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.bgp_view import query_asns, extract_networks
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext
import ipaddress


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        """
        [1] https://support.stackpath.com/hc/en-us/articles/360001091666-Review-and-Allowlist-CDN-WAF-IP-Blocks
        """
        ipv4_networks, ipv6_networks = extract_networks(query_asns("stackpath"))

        url = "https://k3t9x2h3.map2.ssl.hwcdn.net/ipblocks.txt"
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        text = http_cached_requests(url, cache_folder=cache_folder).decode("utf-8")

        for prefix in text.strip().split("\n"):
            network = ipaddress.ip_network(prefix, strict=False)
            if network.version == 4:
                ipv4_networks.append(network)
            if network.version == 6:
                ipv6_networks.append(network)

        ipv6_networks = []
        return ipv4_networks, ipv6_networks


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
