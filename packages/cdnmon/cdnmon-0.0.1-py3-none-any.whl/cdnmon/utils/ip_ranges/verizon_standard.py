from cdnmon.models.abstract_ip_ranges import AbstractIPRanges


class IPRange(AbstractIPRanges):
    IS_PUBLIC = False


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
