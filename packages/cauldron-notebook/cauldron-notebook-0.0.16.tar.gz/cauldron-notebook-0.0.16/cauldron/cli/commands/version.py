import json
from argparse import ArgumentParser

from cauldron import environ
from cauldron.environ import Response

NAME = 'version'
DESCRIPTION = 'Displays Cauldron\'s version information'


def get_package_data():
    with open(environ.paths.package('settings.json'), 'r') as f:
        return json.load(f)


def execute(
        parser: ArgumentParser,
        response: Response
) -> Response:
    """

    :return:
    """

    package_data = get_package_data()

    if package_data:
        return response.update(
            **package_data
        ).notify(
            kind='SUCCESS',
            code='VERSION',
            message='Version is: {}'.format(package_data['version'])
        ).console(
            'Version: {version}'.format(version=package_data['version']),
            whitespace=1
        ).response

    return response.notify(
        kind='ERROR',
        code='MISSING_PACKAGE_DATA',
        message='Unable to locate version information'
    ).console(
        whitespace=1
    ).response
