class AbstractIPRanges:
    IS_PUBLIC = True

    @staticmethod
    def parse():
        """parse the IP range that the CDN provided.
        :return: a two elements tuple, the first element is a list of IPv4 networks, the second element is a list of
        IPv6 networks.

        >>> AbstractIPRanges.parse()
        (["173.245.48.0/20", "103.21.244.0/22"], ["2400:cb00::/32", "2606:4700::/32"])
        """
        raise NotImplementedError()


def main():
    print(AbstractIPRanges.parse())


if __name__ == "__main__":
    main()
