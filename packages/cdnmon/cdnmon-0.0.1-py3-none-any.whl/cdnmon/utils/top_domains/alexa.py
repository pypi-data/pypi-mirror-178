import datetime

from cdnmon.models.abstract_top_domains import AbstractTopDomains


class TopDomains(AbstractTopDomains):
    @staticmethod
    def top(n, date):
        """
        [1] https://www.alexa.com/topsites
        """
        return []


def main():
    date = datetime.datetime.today()
    domains = TopDomains.top(100, date)
    print(date, domains)


if __name__ == "__main__":
    main()
