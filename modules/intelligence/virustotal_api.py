from config import api
from common.query import Query


class VirusTotalAPI(Query):
    def __init__(self, domain):
        Query.__init__(self)
        self.domain = domain
        self.module = 'Intelligence'
        self.source = 'VirusTotalAPIQuery'
        self.addr = 'https://www.virustotal.com/vtapi/v2/domain/report'
        self.key = api.virustotal_api_key

    def query(self):
        """
        向接口查询子域并做子域匹配
        """
        self.header = self.get_header()
        self.proxy = self.get_proxy(self.source)
        params = {'apikey': self.key, 'domain': self.domain}
        resp = self.get(self.addr, params)
        if not resp:
            return
        json = resp.json()
        data = json.get('subdomains')
        if data:
            subdomains = set(data)
            self.subdomains = self.subdomains.union(subdomains)

    def run(self):
        """
        类执行入口
        """
        if not self.check(self.key):
            return
        self.begin()
        self.query()
        self.finish()
        self.save_json()
        self.gen_result()
        self.save_db()


def run(domain):
    """
    类统一调用入口

    :param str domain: 域名
    """
    query = VirusTotalAPI(domain)
    query.run()


if __name__ == '__main__':
    run('example.com')
