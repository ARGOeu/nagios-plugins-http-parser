# nagios-plugins-http-parser

This is a Nagios plugin that parses http response for given three versions of texts which, if found, will return OK, WARNING or CRITICAL status.

`check_http_parser` plugin synopsis

```commandline
# /usr/lib64/nagios/plugins/check_http_parser --help
usage: check_http_parser -H HOSTNAME -t TIMEOUT [-h] [-p PORT] [-u URI]
                         [--ok-search OK_SEARCH]
                         [--warning-search WARNING_SEARCH]
                         [--critical-search CRITICAL_SEARCH]
                         [--ok-message OK_MSG] [--warning-message WARNING_MSG]
                         [--critical-message CRITICAL_MSG] [--ssl]

Nagios plugin that parses http response for given three versions of text that,
if found, will return OK, WARNING or CRITICAL status.

required arguments:
  -H HOSTNAME, --hostname HOSTNAME
                        Name of the host
  -t TIMEOUT, --timeout TIMEOUT
                        Seconds before connection times out (default 10)

optional arguments:
  -h, --help            Show this help message and exit
  -p PORT, --port PORT  Port number (default: 80)
  -u URI, --uri URI     URI to GET (default /)
  --ok-search OK_SEARCH
                        Text to be searched in the http response which, if
                        found, will return status OK (default: ok)
  --warning-search WARNING_SEARCH
                        Text to be searched in the http response which, if
                        found, will return status WARNING (default: warning)
  --critical-search CRITICAL_SEARCH
                        Text to be searched in the http response which, if
                        found, will return status CRITICAL (default: critical)
  --ok-message OK_MSG   Status message to return in case of status OK
                        (default: "")
  --warning-message WARNING_MSG
                        Status message to return in case of status WARNING
                        (default: "")
  --critical-message CRITICAL_MSG
                        Status message to return in case of status CRITICAL
                        (default: "")
  --ssl                 Connect using SSL.
```

Sample execution of `check_http_parser`

```commandline
# /usr/lib64/nagios/plugins/check_http_parser -H <HOSTNAME> -t 20 -p 8000 -u "/api/v1/all&format=status"
OK
```

Check response text with custom return messages
```commandline
# /usr/lib64/nagios/plugins/check_http_parser -H <HOSTNAME> -t 20 -p 8000 -u "/api/v2/all&format=status" 
--ok-search <ok_response_text> --warning-search <warn_response_text> --critical-search <crit_response_text> 
    --ok-message "Everything is OK." --warning-message "Not everything is OK." --critical-message "Nothing is OK."
OK - Everything is OK.
```
