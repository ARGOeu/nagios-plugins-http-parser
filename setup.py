from distutils.core import setup


NAME = 'nagios-plugins-http-parser'


def get_ver():
    try:
        for line in open(NAME + '.spec'):
            if "Version:" in line:
                return line.split()[1]

    except IOError:
        raise SystemExit(1)


setup(
    name=NAME,
    version=get_ver(),
    author='SRCE',
    author_email='kzailac@srce.hr',
    description='Nagios plugin that parses http response.',
    url='https://github.com/ARGOeu/nagios-plugins-http-parser',
    packages=['nagios_plugins_http_parser'],
    data_files=[('/usr/lib64/nagios/plugins', ['plugins/check_http_parser'])]
)
