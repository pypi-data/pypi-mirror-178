import io
import ipaddress
import zipfile

from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.http_client import http_cached_requests
from cdnmon.utils.misc import get_filename_no_ext


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        """
        [1] https://techdocs.akamai.com/property-mgr/docs/origin-ip-access-control
        """
        url = "https://techdocs.akamai.com/property-manager/pdfs/akamai_ipv4_ipv6_CIDRs-txt.zip"
        cache_folder = f"ip_ranges/{get_filename_no_ext(__file__)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/107.0.0.0 Safari/537.36 "
        }
        content = http_cached_requests(url, cache_folder=cache_folder, headers=headers)
        z = zipfile.ZipFile(io.BytesIO(content))
        ipv4_list = z.read("akamai_ipv4_CIDRs.txt").decode("utf-8")
        ipv6_list = z.read("akamai_ipv6_CIDRs.txt").decode("utf-8")

        ipv4_networks = []
        for ipv4_prefix in ipv4_list.split("\n"):
            ipv4_networks.append(ipaddress.IPv4Network(ipv4_prefix.strip(), strict=False))

        ipv6_networks = []
        for ipv6_prefix in ipv6_list.split("\n"):
            ipv6_networks.append(ipaddress.IPv6Network(ipv6_prefix.strip(), strict=False))

        return ipv4_networks, ipv6_networks


def main():
    print(IPRange.parse())


if __name__ == "__main__":
    main()
