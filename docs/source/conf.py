from __future__ import unicode_literals

import os

extensions = []

templates_path = ['_templates']

source_suffix = '.rst'
master_doc = 'index'

project = u'django-anylink'
copyright = u'2014, Moccu'

version = '0.0.1'
release = '0.0.1'

exclude_patterns = ['build']

pygments_style = 'sphinx'

# on_rtd is whether we are on readthedocs.org,
# this line of code grabbed from docs.readthedocs.org
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# html_theme_options = {}
# html_static_path = ['_static']
htmlhelp_basename = 'django-anylinkdoc'

latex_elements = {
    'papersize': 'a4paper',
    # 'pointsize': '10pt',
}
latex_documents = [(
    'index', 'django-anylink.tex', u'django-anylink Documentation',
    'Moccu', 'manual'
)]

man_pages = [(
    'index', 'django-anylink', u'django-anylink Documentation',
    ['Moccu'], 1
)]

texinfo_documents = [(
    'index', 'django-anylink', u'django-anylink Documentation',
    'Moccu', 'django-anylink',
    'Generic linking in Django', 'Miscellaneous'
)]
