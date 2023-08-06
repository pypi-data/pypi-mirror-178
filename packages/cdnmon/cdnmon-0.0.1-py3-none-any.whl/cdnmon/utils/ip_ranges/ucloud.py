from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.bgp_view import query_asns, extract_networks


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        return extract_networks(query_asns("ucloud"))


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
