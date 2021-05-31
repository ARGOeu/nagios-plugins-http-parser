import unittest
from unittest import mock

import requests.exceptions

from nagios_plugins_http_parser.parse import HttpParse


def mock_function(*args, **kwargs):
    pass


class MockResponse:
    def __init__(self, text):
        self.text = text


def mock_response_ok(*args, **kwargs):
    return MockResponse('OK')


def mock_response_warning(*args, **kwargs):
    return MockResponse('WARNING')


def mock_response_critical(*args, **kwargs):
    return MockResponse('CRITICAL')


def mock_response_strange(*args, **kwargs):
    return MockResponse('Some strange text.')


class HttpParseTests(unittest.TestCase):
    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_ok(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('OK - Everything is ok.')
        mock_sys.assert_called_with(0)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_ok_with_ssl(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_ok
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php', ssl=True
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'https://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('OK - Everything is ok.')
        mock_sys.assert_called_with(0)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_warning(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_warning
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('WARNING - Not everything is ok.')
        mock_sys.assert_called_with(1)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_critical(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_critical
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Nothing is ok.')
        mock_sys.assert_called_with(2)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_unknown(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = mock_response_strange
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with(
            'UNKNOWN - None of the sample texts found in response.'
        )
        mock_sys.assert_called_with(3)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_with_connection_error(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = requests.exceptions.ConnectionError('Error')
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('CRITICAL - Error')
        mock_sys.assert_called_with(2)

    @mock.patch('nagios_plugins_http_parser.parse.sys.exit')
    @mock.patch('nagios_plugins_http_parser.parse.print')
    @mock.patch('nagios_plugins_http_parser.parse.requests.get')
    def test_parse_with_unknown_error(self, mock_get, mock_print, mock_sys):
        mock_get.side_effect = Exception('Unknown exception')
        mock_print.side_effect = mock_function
        mock_sys.side_effect = mock_function
        parse = HttpParse(
            hostname='hostname.com', port=80, uri='/api/test.php'
        )
        parse.parse(
            ok_search='ok', warn_search='warning', crit_search='critical',
            ok_msg='Everything is ok.', warn_msg='Not everything is ok.',
            crit_msg='Nothing is ok.', timeout=20
        )
        mock_get.assert_called_with(
            'http://hostname.com:80/api/test.php', timeout=20
        )
        mock_print.assert_called_with('UNKNOWN - Unknown exception')
        mock_sys.assert_called_with(3)


if __name__ == '__main__':
    unittest.main()
