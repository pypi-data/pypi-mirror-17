# -*- coding: utf-8 -*-
"""
"""
import sys
from intelmq.lib.bot import Bot
from intelmq.lib.harmonization import IPAddress

try:
    import pyasn
except ImportError:
    pyasn = None


class ASNLookupExpertBot(Bot):

    def init(self):
        if pyasn is None:
            self.logger.error('Could not import pyasn. Please install it.')
            self.stop()

        try:
            self.database = pyasn.pyasn(self.parameters.database)
        except IOError:
            self.logger.error("pyasn data file does not exist or could not be "
                              "accessed in '%s'" % self.parameters.database)
            self.logger.error("Read 'bots/experts/asn_lookup/README' and "
                              "follow the procedure")
            self.stop()

    def process(self):
        event = self.receive_message()

        for key in ["source.", "destination."]:

            ip_key = key + "ip"
            asn_key = key + "asn"
            bgp_key = key + "network"

            if not event.contains(ip_key):
                continue

            ip = event.get(ip_key)

            if IPAddress.version(ip) == 6:
                # Currently not supported by pyasn, fix will come soon
                continue

            info = self.database.lookup(ip)

            if info:
                if info[0]:
                    event.add(asn_key, str(info[0]), force=True)
                if info[1]:
                    event.add(bgp_key, str(info[1]), force=True)

        self.send_message(event)
        self.acknowledge_message()


if __name__ == "__main__":
    bot = ASNLookupExpertBot(sys.argv[1])
    bot.start()
