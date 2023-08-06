import csv
import datetime
import os.path
import queue
import time
import uuid

import dns

from dns.resolver import Resolver
from cdnmon.utils.logging import logger
from cdnmon.utils.misc import get_project_root


class DNSClient:
    def __init__(self, resolver_ip, log_folder_name):
        self.resolver_ip = resolver_ip
        self.resolver = Resolver()
        self.resolver.nameservers = [self.resolver_ip]
        today = datetime.datetime.today().strftime("%Y-%m-%d")
        self._log_filepath = f"{get_project_root()}/output/{today}/dns/{log_folder_name}/query_log.csv"
        self._log_fieldnames = [
            "log_uuid",
            "start_time",
            "end_time",
            "qname",
            "qtype",
            "rname",
            "rtype",
            "ttl",
        ]
        self.writer = self._open_log_file_writer()
        self.cache = self.load_cache()

    def load_cache(self):
        return {}

    def _create_log_file(self):
        if not os.path.exists(self._log_filepath):
            os.makedirs(os.path.dirname(self._log_filepath), exist_ok=True)
            log_fd = open(self._log_filepath, "a+", encoding="utf-8", newline="\n")
            writer = csv.DictWriter(log_fd, fieldnames=self._log_fieldnames)
            writer.writeheader()
            log_fd.close()

    def _open_log_file_writer(self):
        self._create_log_file()
        log_fd = open(self._log_filepath, "a+", encoding="utf-8", newline="\n")
        return csv.DictWriter(log_fd, fieldnames=self._log_fieldnames)

    def query(self, qname, qtype, log_uuid):
        logger.debug(f"resolving {qname} {qtype} from {self.resolver_ip}")
        answers = []

        cache_key = (qname, qtype)
        if cache_key in self.cache.keys():
            return self.cache[cache_key]

        try:
            start_time = time.time()
            response = self.resolver.resolve(qname, qtype)
            end_time = time.time()
            answers = list(response)
            assert len(answers) > 0
            self.save(
                log_uuid,
                start_time,
                end_time,
                qname,
                qtype,
                "|".join([answer.target.to_text() for answer in answers]),
                dns.rdatatype.to_text(response.rdtype),
                response.ttl,
            )
        except dns.resolver.NoAnswer as e:
            end_time = time.time()
            logger.debug(repr(e))
            self.save(log_uuid, start_time, end_time, qname, qtype, "EMPTY", "", -1)
        except dns.resolver.NXDOMAIN as e:
            end_time = time.time()
            logger.debug(repr(e))
            self.save(log_uuid, start_time, end_time, qname, qtype, "NXDOMAIN", "", -1)
        except Exception as e:
            logger.debug(repr(e))

        return answers

    def save(self, log_uuid, start_time, end_time, qname, qtype, rname, rtype, ttl):
        self.writer.writerow(
            {
                "log_uuid": log_uuid,
                "start_time": start_time,
                "end_time": end_time,
                "qname": qname,
                "qtype": qtype,
                "rname": rname,
                "rtype": rtype,
                "ttl": ttl,
            }
        )

    def query_cname(self, qname):
        return self.query(qname, qtype="CNAME")

    def query_cname_recursively(self, qname):
        log_uuid = uuid.uuid4()
        q = queue.Queue()
        q.put(qname)
        results = []
        while not q.empty():
            current_qname = q.get()
            results.append(current_qname)
            for answer in self.query(current_qname, qtype="CNAME", log_uuid=log_uuid):
                q.put(answer.target.to_text())
        return results
