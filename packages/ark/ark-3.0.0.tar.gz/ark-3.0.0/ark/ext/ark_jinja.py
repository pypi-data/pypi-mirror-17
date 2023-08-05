# --------------------------------------------------------------------------
# This extension adds support for Jinja templates.
# --------------------------------------------------------------------------

import sys
from ark import hooks, templates, site

try:
    import jinja2
except ImportError:
    jinja2 = None


# Stores an initialized Jinja environment instance.
env = None


# The jinja2 package is an optional dependency.
if jinja2:

    # Initialize our Jinja environment on the 'init' event hook.
    @hooks.register('init')
    def init():

        # Initialize a template loader.
        settings = {
            'loader': jinja2.FileSystemLoader(site.theme('templates'))
        }

        # Check the site's config file for any custom settings.
        settings.update(site.config.get('jinja', {}))

        # Initialize an Environment instance.
        global env
        env = jinja2.Environment(**settings)

    # Register our template engine callback for files with a .jinja extension.
    @templates.register('jinja')
    def callback(page, filename):
        try:
            template = env.get_template(filename)
            return template.render(page)
        except jinja2.TemplateError as e:
            msg =  "------------------------\n"
            msg += "  Jinja Template Error  \n"
            msg += "------------------------\n\n"
            msg += "  Template: %s\n" % filename
            msg += "  Page:     %s\n\n" % page['path']
            msg += "  %s: %s" % (e.__class__.__name__, e)
            if e.__context__:
                msg += "\n\nThe following exception was reported:\n\n"
                msg += "%s: %s" % (
                    e.__context__.__class__.__name__, e.__context__
                )
            sys.exit(msg)
