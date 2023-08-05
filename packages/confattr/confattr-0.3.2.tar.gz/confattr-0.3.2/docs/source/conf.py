# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'confattr'
copyright = '2022, erzo'
author = 'erzo'
release = 'v0.3.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']

templates_path = ['_templates']
exclude_patterns = []
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'nature'
html_static_path = ['_static']

rst_prolog = '''
.. |WARNING| replace:: **Warning**
'''


# -- autodoc configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autoclass_content = 'both'  # 'class', 'both', 'init'
#autodoc_class_signature = 'separated'  # 'mixed', 'separated'
#autodoc_member_order = 'bysource'  # 'alphabetical', 'groupwise', 'bysource'
#autodoc_typehints = 'description'  # 'signature', 'description', 'none', 'both'
#autodoc_typehints_description_target = 'documented_params'  # 'all', 'documented', 'documented_params'
#autodoc_type_aliases = {}
#autodoc_typehints_format = 'fully-qualified'  # 'fully-qualified', 'short'
#autodoc_preserve_defaults = True  # True, False
#autodoc_warningiserror = True  # True, False
#autodoc_inherit_docstrings = True  # True, False
