import sys
import os

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "nasa.py"
copyright = "2023, Snipy7374"
author = "Snipy7374"
version = "0.0.1"
release = version

sys.path.insert(0, os.path.abspath("../../"))
# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
]

autodoc_member_order = "bysource"
autodoc_typehints = "signature"
autodoc_class_signature = "separated"
autodoc_preserve_defaults = True
autoclass_content = "class"

autodoc_type_aliases = {
    "AstronomyPicture": "AstronomyPicture",
    "_RawSpatialCoordinates": "nasa._RawSpatialCoordinates",
    "EpicImage": "EpicImage"
}
autodoc_default_options = {
    "exclude-members": "__init__, __new__",
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build"]
source_suffix = ".rst"
master_doc = "index"


# used to cross-reference stuff
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "aio": ("https://docs.aiohttp.org/en/stable/", None),
    "req": ("https://requests.readthedocs.io/en/latest/", None),
}

pygments_style = "sphinx"
pygments_dark_style = "monokai"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
#html_static_path = ["_static"]
html_theme_otpions = {
    "soruce_repository": "https://github.com/Snipy7374/nasa.py",
    "source_branch": "master",
    "prefers_color_scheme": "dark"
}