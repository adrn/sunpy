# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# SunPy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else.
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for sunpy or sunpy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_docs" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

import os
import datetime
import sys
from distutils.version import LooseVersion


import ruamel.yaml as yaml

from sphinx import __version__
SPHINX_LT_17 = LooseVersion(__version__) < LooseVersion('1.7')

# -- Convert Sphinx Warnings to output to stdout not stderr---------------------
if not SPHINX_LT_17:
    import logging
    from sphinx.util.logging import NAMESPACE, WarningStreamHandler, SafeEncodingWriter

    sphinxlogger = logging.getLogger(NAMESPACE)
    handlers = sphinxlogger.handlers
    warninghandler = list(filter(lambda x: isinstance(x, WarningStreamHandler), handlers))[0]
    warninghandler.stream = SafeEncodingWriter(stream=sys.stdout)

# -- Import Base config from sphinx-astropy ------------------------------------

try:
    from sphinx_astropy.conf.v1 import *
except ImportError:
    print('ERROR: the documentation requires the sphinx-astropy package to be installed')
    sys.exit(1)

try:
    import sphinx_gallery
    has_sphinx_gallery = True
except ImportError:
    has_sphinx_gallery = False

if on_rtd:
    os.environ['SUNPY_CONFIGDIR'] = '/home/docs/'
    os.environ['HOME'] = '/home/docs/'
    os.environ['LANG'] = 'C'
    os.environ['LC_ALL'] = 'C'

try:
    import suds
except ImportError:
    print('ERROR: suds could not be imported and the documentation requires the suds-jerko package to be installed')
    sys.exit(1)

from sunpy import version as versionmod

# -- Shut up numpy warnings from WCSAxes
import numpy as np
np.seterr(invalid='ignore')

# -- Download Sample Data -----------------------------------------------------

import sunpy.data.sample

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.5'

# To perform a Sphinx version check that needs to be more specific than
# major.minor, call `check_sphinx_version("x.y.z")` here.
check_sphinx_version(needs_sphinx)

# add any custom intersphinx for sunpy
intersphinx_mapping.pop('h5py', None)
intersphinx_mapping['sqlalchemy'] = ('http://docs.sqlalchemy.org/en/latest/', None)
intersphinx_mapping['pandas'] = ('http://pandas.pydata.org/pandas-docs/stable/', None)
intersphinx_mapping['skimage'] = ('http://scikit-image.org/docs/stable/', None)

# Load data about stability

with open('./dev_guide/sunpy_stability.yaml', 'r') as estability:
    sunpy_modules = yaml.load(estability.read(), Loader=yaml.Loader)

html_context = {
    'sunpy_modules': sunpy_modules
}


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# Add any paths that contain templates here, relative to this directory.
if 'templates_path' not in locals():  # in case parent conf.py defines it
    templates_path = []
templates_path.append('_templates')

# For the linkcheck
linkcheck_ignore = [r" https://doi.org/\d+",
                    r"https://riot.im/\d+",
                    r"https://github.com/\d+",
                    r"http://docs.sunpy.org/\d+"]
linkcheck_anchors = False

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog += """
.. SunPy
.. _SunPy: http://sunpy.org
.. _`SunPy mailing list`: http://groups.google.com/group/sunpy
.. _`SunPy dev mailing list`: http://groups.google.com/group/sunpy-dev
""".format(sunpy)

# -- Project information ------------------------------------------------------

project = u'SunPy'
author = u'The SunPy Community'
copyright = u'{}, {}'.format(datetime.datetime.now().year, author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The short X.Y version.
version = versionmod.version.split('-', 1)[0]
# The full version, including alpha/beta/rc tags.
release = versionmod.version

try:
    from sunpy_sphinx_theme.conf import *
    html_sidebars = {'**': ['docsidebar.html']}

except ImportError:
    html_theme = 'default'

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "./logo/favicon.ico"

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = ''

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)


# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# -- Options for LaTeX output --------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation', author, 'manual')]

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation', [author], 1)]

# -- Swap to Napoleon ---------------------------------------------------------
# Remove numpydoc
extensions.remove('numpydoc')
extensions.append('sphinx.ext.napoleon')

# Disable having a separate return type row
napoleon_use_rtype = False
# Disable google style docstrings
napoleon_google_docstring = False

extensions += ['sphinx_astropy.ext.edit_on_github', 'sphinx.ext.doctest', 'sphinx.ext.githubpages']

# -- Options for the edit_on_github extension
# Don't import the module as "version" or it will override the
# "version" configuration parameter
edit_on_github_project = "sunpy/sunpy"
if versionmod.release:
    edit_on_github_branch = "v{0}.{1}.x".format(versionmod.major, versionmod.minor)
else:
    edit_on_github_branch = "master"
edit_on_github_source_root = ""
edit_on_github_doc_root = "docs"

edit_on_github_skip_regex = '_.*|generated/.*'

github_issues_url = 'https://github.com/sunpy/sunpy/issues/'

# -- Options for the Sphinx gallery -------------------------------------------
if has_sphinx_gallery:
    extensions += ["sphinx_gallery.gen_gallery"]

    sphinx_gallery_conf = {
        'backreferences_dir':
        'generated{}modules'.format(os.sep),  # path to store the module using example template
        'filename_pattern':
        '^((?!skip_).)*$',  # execute all examples except those that start with "skip_"
        'examples_dirs': os.path.join('..', 'examples'),  # path to the examples scripts
        'gallery_dirs': os.path.join('generated',
                                    'gallery'),  # path to save gallery generated examples
        'default_thumb_file': os.path.join('.', 'logo', 'sunpy_icon_128x128.png'),
        'reference_url': {
            'sunpy': None,
            'astropy': 'http://docs.astropy.org/en/stable/',
            'matplotlib': 'https://matplotlib.org/',
            'numpy': 'http://docs.scipy.org/doc/numpy/',
        },
        'abort_on_example_error': True,
        'plot_gallery': True
    }

def rstjinja(app, docname, source):
    """
    Render our pages as a jinja template for fancy templating goodness.
    """
    # Make sure we're outputting HTML
    if app.builder.format != 'html':
        return
    src = source[0]
    if "Current status" in src[:20]:
        rendered = app.builder.templates.render_string(
            src, app.config.html_context
        )
        source[0] = rendered


def setup(app):
    if has_sphinx_gallery == False:
        app.warn('The sphinx_gallery extension is not installed, so the '
                 'gallery will not be built. You will probably see '
                 'additional warnings about undefined references due '
                 'to this.')
    try:
        app.connect("source-read", rstjinja)
    except:
        pass
