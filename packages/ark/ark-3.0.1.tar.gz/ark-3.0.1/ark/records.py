# --------------------------------------------------------------------------
# This module handles the creation and caching of Record objects.
# --------------------------------------------------------------------------

import os
import re
import datetime

from . import utils
from . import site
from . import hooks
from . import renderers
from . import loader


# An in-memory cache of Record objects indexed by source filepath.
cache = {}


# Return the Record object corresponding to the specified source file.
def record(filepath):
    if not filepath in cache:
        cache[filepath] = Record(filepath)
    return cache[filepath]


# A Record instance represents a parsed source file. Record objects should
# not be instantiated directly; instead use the `record()` function to take
# advantage of automatic caching.
class Record(dict):

    def __init__(self, filepath):

        # Parse the filepath.
        dirpath = os.path.dirname(filepath)
        fileinfo = utils.fileinfo(filepath)

        # Load the record file.
        text, meta = loader.load(filepath)
        self.update(meta)

        # Add the default set of record attributes.
        self['type'] = site.type_from_src(dirpath)
        self['slug'] = meta.get('slug') or utils.slugify(fileinfo.base)
        self['slugs'] = site.slugs_from_src(dirpath, self['slug'])
        self['src'] = filepath
        self['srcdir'] = dirpath
        self['ext'] = fileinfo.ext
        self['url'] = site.url(self['slugs'])

        # Add a default datetime stamp. We use the 'date' attribute if it's
        # present, otherwise we use the file creation time (OSX, BSD, Windows)
        # or the time of the file's last metadata change (Linux).
        date = self.get('date')
        if isinstance(date, datetime.datetime):
            self['date'] = date
        elif isinstance(date, datetime.date):
            self['date'] = datetime.datetime.fromordinal(date.toordinal())
        else:
            self['date'] = utils.get_creation_time(filepath)

        # Filter the record's text content. (Shortcodes are processed here.)
        self['text'] = hooks.filter('record_text', text, self)

        # Render the record's content into html.
        html = renderers.render(self['text'], fileinfo.ext)

        # Filter the record's html content.
        self['html'] = hooks.filter('record_html', html, self)

        # Fire the 'init_record' event. (Tags are processed here.)
        hooks.event('init_record', self)
