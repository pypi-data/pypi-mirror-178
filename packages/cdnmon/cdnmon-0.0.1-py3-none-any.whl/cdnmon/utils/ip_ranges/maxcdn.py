from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext
import ipaddress


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        """
        [1] https://support.maxcdn.com/one/tutorial/ip-blocks/
        [2] https://support.maxcdn.com/one/assets/ips.txt
            ->
            https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt
        """
        url = "https://support.maxcdn.com/hc/en-us/article_attachments/360051920551/maxcdn_ips.txt"
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        text = http_cached_requests(url, cache_folder=cache_folder).decode("utf-8")

        ipv4_networks, ipv6_networks = [], []

        for prefix in text.strip().split("\n"):
            network = ipaddress.ip_network(prefix, strict=False)
            if network.version == 4:
                ipv4_networks.append(network)
            if network.version == 6:
                ipv6_networks.append(network)

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
