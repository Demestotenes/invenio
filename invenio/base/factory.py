# -*- coding: utf-8 -*-
## This file is part of Invenio.
## Copyright (C) 2011, 2012, 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Invenio -> Flask adapter
"""

## Import the remote debugger as a first thing, if allowed
try:
    from invenio import remote_debugger
except:
    remote_debugger = None

import os
from flask import current_app

from invenio import config
from invenio.errorlib import register_exception
from invenio.config import \
    CFG_WEBDIR, \
    CFG_FLASK_DISABLED_BLUEPRINTS, \
    CFG_SITE_SECRET_KEY, CFG_BINDIR

from werkzeug.utils import import_string

from .helpers import with_app_context
from .wrappers import Flask

def import_extension(directories, extension_name):
    """
        Searches EXTENSION_DIRECTORIES for the desired extension;

        returns (setup_app, config)
    """

    for directory in directories:
        ext_path = '{directory}{dot}{name}'.format(
            directory=directory,
            dot=('.' if directory else ''),
            name=extension_name)

        try:
            ext_module = import_string(ext_path)
            ext_setup = getattr(ext_module, 'setup_app', None)
            ext_config = getattr(ext_module, 'config', None)
            if not ext_config:
                try:
                    ext_config = import_string(ext_path + '.config')
                except:
                    pass
            return (ext_setup, ext_config)

        except:
            # Extension not found here, keep looking
            pass

    try:
        # Maybe it is a callable extensions
        ext_module = import_string(extension_name)
        return (ext_module, None)
    except:
        # TODO Write to 'missing-extensions.log'
        return (None, None)


def register_extensions(app):
    for ext_name in app.config.get('EXTENSIONS', []):
        (ext_setup, ext_config) = import_extension(
            app.config.get('EXTENSION_DIRECTORIES', ['']),
            ext_name)
        if ext_config:
            app.config.from_object(ext_config)

        if ext_setup:
            try:
                new_app = ext_setup(app)
                if new_app is not None:
                    app = new_app
            except Exception as e:
                print ext_name, e
                # TODO Write to 'broken-extensions.log'
                pass

    return app

from flask import has_app_context, current_app
from werkzeug.utils import import_string, find_modules
from functools import partial
from itertools import chain


def import_module_from_packages(name, app=None, packages=None):
    if packages is None:
        if app is None and has_app_context():
            app = current_app
        if app is None:
            raise Exception('Working outside application context or provide app')
        packages = app.config.get('PACKAGES', [])

    for package in packages:
        if package.endswith('.*'):
            for module in find_modules(package[:-2], include_packages=True):
                try:
                    yield import_string(module + '.' + name)
                except ImportError:
                    pass
                except Exception as e:
                    app.logger.error('Could not import: "%s.%s: %s',
                                     module, name, str(e))
                    pass
            continue
        try:
            yield import_string(package + '.' + name)
        except ImportError:
            pass
        except Exception as e:
            app.logger.error('Could not import: "%s.%s: %s',
                             package, name, str(e))
            pass


collect_blueprints = lambda app: chain(
    partial(import_module_from_packages, 'blueprint')(app),
    partial(import_module_from_packages, 'admin_blueprint')(app)
    )
collect_models = partial(import_module_from_packages, 'model')
collect_user_settings = partial(import_module_from_packages, 'user_settings')


def create_app(**kwargs_config):
    """
    Prepare WSGI Invenio application based on Flask.

    Invenio consists of a new Flask application with legacy support for
    the old WSGI legacy application and the old Python legacy
    scripts (URLs to *.py files).

    An incoming request is processed in the following manner:

     * The Flask application first routes request via its URL routing
       system (see LegacyAppMiddleware.__call__()).

     * One route in the Flask system, will match Python legacy
       scripts (see static_handler_with_legacy_publisher()).

     * If the Flask application aborts the request with a 404 error, the request
       is passed on to the WSGI legacy application (see page_not_found()). E.g.
       either the Flask application did not find a route, or a view aborted the
       request with a 404 error.
    """

    ## The Flask application instance
    _app = Flask(__name__, #FIXME .split('.')[0],
        ## Static files are usually handled directly by the webserver (e.g. Apache)
        ## However in case WSGI is required to handle static files too (such
        ## as when running simple server), then this flag can be
        ## turned on (it is done automatically by wsgi_handler_test).
        ## We assume anything under '/' which is static to be server directly
        ## by the webserver from CFG_WEBDIR. In order to generate independent
        ## url for static files use func:`url_for('static', filename='test')`.
        static_url_path='',
        static_folder=CFG_WEBDIR)

    # Handle both url with and without trailing slashe by Flask.
    # @blueprint.route('/test')
    # @blueprint.route('/test/') -> not necessary when strict_slashes == False
    _app.url_map.strict_slashes = False

    # Load invenio.conf
    _app.config.from_object(config)

    # Load invenio.cfg
    _app.config.from_pyfile('invenio.cfg')

    ## Update application config from parameters.
    _app.config.update(kwargs_config)

    # Register extendsions listed in invenio.cfg
    register_extensions(_app)

    ## Database was here.

    ## First check that you have all rights to logs
    #from invenio.bibtask import check_running_process_user
    #check_running_process_user()

    from invenio.messages import language_list_long
    from invenio.webinterface_handler_flask_utils import unicodifier

    # Jinja2 hacks were here.
    # See note on Jinja2 string decoding using ASCII codec instead of UTF8 in
    # function documentation

    # SECRET_KEY is needed by Flask Debug Toolbar
    SECRET_KEY = _app.config.get('SECRET_KEY') or CFG_SITE_SECRET_KEY
    if not SECRET_KEY or SECRET_KEY == '':
        fill_secret_key = """
    Set variable CFG_SITE_SECRET_KEY with random string in invenio-local.conf.

    You can use following commands:
    $ %s
    $ %s
        """ % (CFG_BINDIR + os.sep + 'inveniocfg --create-secret-key',
               CFG_BINDIR + os.sep + 'inveniocfg --update-config-py')
        try:
            raise Exception(fill_secret_key)
        except Exception:
            register_exception(alert_admin=True,
                               subject="Missing CFG_SITE_SECRET_KEY")
            raise Exception(fill_secret_key)

    _app.config["SECRET_KEY"] = SECRET_KEY

    # Debug toolbar was here

    # Set email backend for Flask-Email plugin

    # Mailutils were here

    # SSLify was here

    # Legacy was here

    # Jinja2 Memcache Bytecode Cache was here.

    # Jinja2 custom loader was here.

    # SessionInterface was here.

    ## Set custom request class was here.

    ## ... and map certain common parameters
    _app.config['CFG_LANGUAGE_LIST_LONG'] = [(lang, longname.decode('utf-8'))
        for (lang, longname) in language_list_long()]

    ## Invenio is all using str objects. Let's change them to unicode
    _app.config.update(unicodifier(dict(_app.config)))

    from invenio.base import before_request_functions
    before_request_functions.setup_app(_app)

    # Cache was here

    # Logging was here.

    # Login manager was here.

    # Main menu was here.

    # Jinja2 extensions loading was here.

    # Custom template filters were here.

    # Gravatar bridge was here.

    # Set the user language was here.

    # Custom templete filters loading was here.

    def _invenio_blueprint_plugin_builder(plugin):
        """
        Handy function to bridge pluginutils with (Invenio) blueprints.
        """
        from invenio.webinterface_handler_flask_utils import InvenioBlueprint
        if 'blueprint' in dir(plugin):
            candidate = getattr(plugin, 'blueprint')
            if isinstance(candidate, InvenioBlueprint):
                if candidate.name in CFG_FLASK_DISABLED_BLUEPRINTS:
                    _app.logger.info('%s is excluded by CFG_FLASK_DISABLED_BLUEPRINTS' % candidate.name)
                    return
                return candidate
        _app.logger.error('%s is not a valid blueprint plugin' % plugin.__name__)


    ## Let's load all the blueprints that are composing this Invenio instance
    _BLUEPRINTS = [m for m in map(_invenio_blueprint_plugin_builder,
                                  collect_blueprints(app=_app))
                   if m is not None]

    _app.config['breadcrumbs_map'] = {}

    ## Let's attach all the blueprints
    for plugin in _BLUEPRINTS:
        _app.register_blueprint(plugin,
                                url_prefix=_app.config.get(
                                    'BLUEPRINTS_URL_PREFIXES',
                                    {}).get(plugin.name))
        if plugin.config:
            ## Let's include the configuration parameters of the config file.
            ## E.g. if the blueprint specify the config string
            ## 'invenio.webmessage_config' any uppercase variable defined in
            ## the module invenio.webmessage_config is loaded into the system.
            _app.config.from_object(plugin.config)

    # Flask-Admin was here.

    return _app