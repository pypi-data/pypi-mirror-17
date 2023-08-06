from __future__ import absolute_import

import click
from flask import current_app

from realms import search, cli_group
from realms.modules.wiki.models import Wiki


@cli_group(short_help="Search Module")
def cli():
    pass


@cli.command()
def rebuild_index():
    """ Rebuild search index
    """
    if current_app.config.get('SEARCH_TYPE') == 'simple':
        click.echo("Search type is simple, try using elasticsearch.")
        return

    # Wiki
    search.delete_index('wiki')
    wiki = Wiki(current_app.config['WIKI_PATH'])
    for entry in wiki.get_index():
        page = wiki.get_page(entry['name'])
        if not page:
            # Some non-markdown files may have issues
            continue
        # TODO add email?
        # TODO I have concens about indexing the commit info from latest revision, see #148
        info = next(page.history)
        body = dict(name=page.name,
                    content=page.data,
                    message=info['message'],
                    username=info['author'],
                    updated_on=entry['mtime'],
                    created_on=entry['ctime'])
        search.index_wiki(page.name, body)
