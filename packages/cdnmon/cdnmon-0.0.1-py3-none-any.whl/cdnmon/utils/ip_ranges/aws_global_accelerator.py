from cdnmon.models.abstract_ip_ranges import AbstractIPRanges
from cdnmon.utils.ip_ranges import _aws


class IPRange(AbstractIPRanges):
    @staticmethod
    def parse():
        """
        [1] https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html
        """
        return _aws.get_ip_range_of_aws("CLOUDFRONT")


def main():
    print(IPRange().parse())


if __name__ == "__main__":
    main()
