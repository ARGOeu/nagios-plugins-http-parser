import requests
import sys
from nagios_plugins_http_parser.nagios import NagiosResponse


class HttpParse:
    def __init__(self, hostname, port, uri, ssl=False):
        self.hostname = hostname
        self.port = port
        self.uri = uri
        self.ssl = ssl

        self.nagios = NagiosResponse()

    def _build_url(self):
        hostname = self.hostname
        if hostname.startswith('https://'):
            hostname = hostname[8:]

        if hostname.startswith('http://'):
            hostname = hostname[7:]

        if hostname.endswith('/'):
            hostname = hostname[0:-1]

        uri = self.uri
        if not uri.startswith('/'):
            uri = '/{}'.format(uri)

        if self.ssl:
            return 'https://{}:{}{}'.format(hostname, self.port, uri)

        else:
            return 'http://{}:{}{}'.format(hostname, self.port, uri)

    def parse(
            self, ok_search, warn_search, crit_search, ok_msg, warn_msg,
            crit_msg, unknown_msg, timeout
    ):
        url = self._build_url()

        try:
            response = requests.get(url, timeout=timeout)

            if crit_search.lower() in response.text.lower():
                if crit_msg:
                    msg = crit_msg
                else:
                    msg = response.text
                self.nagios.set_critical(msg)

            elif warn_search.lower() in response.text.lower():
                if warn_msg:
                    msg = warn_msg

                else:
                    msg = response.text

                self.nagios.set_warning(msg)

            elif ok_search.lower() in response.text.lower():
                self.nagios.set_ok(ok_msg)

            else:
                self.nagios.set_unknown(unknown_msg)

        except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                requests.exceptions.RequestException
        ) as e:
            self.nagios.set_critical(str(e))

        except Exception as e:
            self.nagios.set_unknown(str(e))

        print(self.nagios.get_message())
        sys.exit(self.nagios.get_code())
