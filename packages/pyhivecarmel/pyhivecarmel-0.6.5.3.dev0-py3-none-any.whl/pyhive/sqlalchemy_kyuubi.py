"""Integration between SQLAlchemy and Kyuubi.

Some code based on
https://github.com/zzzeek/sqlalchemy/blob/rel_0_5/lib/sqlalchemy/databases/sqlite.py
which is released under the MIT license.
"""

from pyhive.sqlalchemy_hive import HiveDialect
from pyhive import hive


class KyuubiDialect(HiveDialect):
    name = b'kyuubi'

    @classmethod
    def dbapi(cls):
        return hive

    def create_connect_args(self, url):
        # TODO  add params check
        kwargs = {
            'host': url.host,
            'port': url.port or 10000,
            'username': url.username,
            'password': url.password,
            'database': url.database or 'default',
            'configuration': {
                "set:hiveconf:kyuubi.engine.share.level": url.query["kyuubi.engine.share.level"],
                "set:hiveconf:kyuubi.session.cluster": url.query["kyuubi.session.cluster"],
                "set:hivevar:spark.yarn.queue": url.query["spark.yarn.queue"],
                "kyuubi.proxy.batchAccount": url.query["kyuubi.proxy.batchAccount"],
                "use:database": url.database
            }
        }

        # remove kyuubi params before merge back to Connection args, otherwise kyuubi sqlachemy cannot figure out to use hive driver
        url.query.pop("kyuubi.engine.share.level")
        url.query.pop("kyuubi.session.cluster")
        url.query.pop("spark.yarn.queue")
        url.query.pop("kyuubi.proxy.batchAccount")
        kwargs.update(url.query)
        return [], kwargs
