#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import click
import requests
from operator import itemgetter


base_url = "https://packages.gandi.net/api/packinfo"


@click.group()
def cli():
    pass


@cli.command()
@click.option('--login', prompt=True)
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False)
def auth(login, password):
    """Retrieve packinfo apikey using LDAP auth."""
    url = '%s/token' % base_url
    headers = {'login': login, 'password': password}
    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    apikey = resp.json()['apikey']
    click.echo('export PACKINFO_TOKEN=%s' % apikey)


@cli.command()
@click.argument('package')
@click.argument('distrib', default='*')
@click.argument('source', default='*')
@click.argument('version', required=False)
def search(package, distrib, source, version):
    """Search for a debian package."""
    url = '%s/debian/%s/%s/%s' % (base_url, distrib, source, package)
    if version:
        url = '%s/%s' % (url, version)
    resp = requests.get(url)
    if resp.status_code != 200:
        try:
            json = resp.json()
            error = json['error']
        except:
            error = resp.text
        click.echo(error)
        sys.exit(1)
    for item in resp.json():
        item['release'] = item['release'].replace('debian-', '')
        line = '%(release)s %(component)s: %(name)s = %(version)s (source: %(source)s)' % item # noqa
        click.echo(line)


@cli.command()
@click.argument('package')
@click.argument('distrib')
@click.argument('source')
@click.argument('destination')
@click.argument('token', envvar='PACKINFO_TOKEN', required=False)
def move(package, distrib, source, destination, token):
    """Move a debian package between sources."""
    if not token:
        click.echo('missing API token, please provide token using command '
                   'line argument or PACKINFO_TOKEN envvar.')
        sys.exit(1)

    url = '%s/packages/%s/%s/%s/%s' % (base_url, distrib, package,
                                       source, destination)
    resp = requests.post(url, headers={'apikey': token})
    if resp.status_code != 204:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    click.echo('Command successful')


@cli.command()
@click.argument('package')
@click.argument('distrib')
@click.argument('source')
@click.argument('token', envvar='PACKINFO_TOKEN', required=False)
def delete(package, distrib, source, token):
    """Delete a debian package from source."""
    if not token:
        click.echo('missing API token, please provide token using command '
                   'line argument or PACKINFO_TOKEN envvar.')
        sys.exit(1)

    url = '%s/packages/%s/%s/%s' % (base_url, distrib, package, source)
    resp = requests.delete(url, headers={'apikey': token})
    if resp.status_code != 204:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    click.echo('Command successful')


@cli.group()
def morgue():
    """Commands related to morgue debian packages"""
    pass


@morgue.command(name='search')
@click.argument('package')
@click.argument('distrib', default='*')
@click.argument('version', required=False)
def morgue_search(package, distrib, version):
    """Search for a debian package in the morgue."""
    url = '%s/morgue/%s/%s' % (base_url, distrib, package)
    if version:
        url = '%s/%s' % (url, version)
    resp = requests.get(url)
    if resp.status_code != 200:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    # sort by version
    entries = sorted(resp.json(), key=itemgetter('version'))
    for item in entries:
        item['release'] = item['release'].replace('debian-', '')
        line = '%(release)s: %(name)s = %(version)s' % item
        click.echo(line)


@morgue.command(name='resurrect')
@click.argument('package')
@click.argument('distrib')
@click.argument('component')
@click.argument('version')
@click.argument('token', envvar='PACKINFO_TOKEN', required=False)
def resurrect(package, distrib, component, version, token):
    """Bring back to life a morgue debian package."""
    if not token:
        click.echo('missing API token, please provide token using command '
                   'line argument or PACKINFO_TOKEN envvar.')
        sys.exit(1)

    url = '%s/debian/%s/%s/%s' % (base_url, '*', '*', package)
    resp = requests.get(url)
    if resp.status_code != 200:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    source = None
    release = None
    source_component = None
    for item in resp.json():
        source = item['source']
        release = item['release'].replace('debian-', '')
        source_component = item['component']
        break
    if not source:
        click.echo('Cannot find source for package %s' % package)
        sys.exit(1)

    url = '%s/source/debian/%s/%s/%s' % (base_url, release, source_component,
                                         source)
    resp = requests.get(url)
    if resp.status_code != 200:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    # sort by version
    package_list = sorted([item['name'] for item in resp.json()
                           if item['name'] != package])
    proceed = False
    if not package_list:
        proceed = click.confirm('You want to resurrect %s, continue ?' %
                                package)
    else:
        package_info = '- ' + '\n- '.join(package_list)
        proceed = click.confirm('You want to resurrect %s, it will also '
                                'resurrect these packages: \n%s\n'
                                'Continue ?' % (package, package_info))
    if not proceed:
        return

    url = '%s/morgue/resurrect/%s/%s/%s/%s' % (base_url, distrib, component,
                                               package, version)
    resp = requests.post(url, headers={'apikey': token})
    if resp.status_code != 204:
        json = resp.json()
        click.echo(json['error'])
        sys.exit(1)
    click.echo('Command successful')


def main():
    cli.main()


if __name__ == '__main__':
    main()
