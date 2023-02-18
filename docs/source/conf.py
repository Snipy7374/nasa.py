import sys
import os

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
sys.path.insert(0, os.path.abspath("../../"))
import nasa

project = nasa.__name__
copyright = nasa.__copyright__
author = nasa.__author__
version = f"{nasa.version_info.major}.{nasa.version_info.minor}.{nasa.version_info.micro}"
release = version
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
    "sphinxcontrib.towncrier.ext",
    "hoverxref.extension",
    "sphinxcontrib_trio",
]

github_repository = "https://github.com/Snipy7374/nasa.py"


extlinks = {
    "issue": (f"{github_repository}/issues/%s", "#%s"),
}
extlinks_detect_hardcoded_links = True


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
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
master_doc = "index"


# https://sphinx-hoverxref.readthedocs.io/en/latest/index.html
hoverxref_auto_ref = True
hoverxref_default_type = "tooltip"
hoverxref_role_types = {
    "class": "tooltip",
    "func": "tooltip",
    "meth": "tooltip",
    "attr": "tooltip",
    "ref": "modal",
    "mod": "modal",
    "hoverxref": "tooltip",
}
hoverxref_domains = ["py"]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "requests": ("https://requests.readthedocs.io/en/latest/", None),
    "aiohttp": ("https://docs.aiohttp.org/en/stable/", None),
}
hoverxref_intersphinx = [
    "python",
    "aiofiles",
    "requests",
    "aiohttp",
]
hoverxref_intersphinx_types = {
    "python": "tooltip",
}
hoverxref_tooltip_theme = ["tooltipster-shadow-custom"]


pygments_style = "sphinx"
pygments_dark_style = "monokai"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/Snipy7374/nasa.py/",
    "source_branch": "master",
    "source_directory": "docs/source/",
    "announcement": "<b><em>Important</em></b> this package isn't in its stable version yet! Breaking changes may occur at any time.",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/Snipy7374/nasa.py",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        }
    ]
}