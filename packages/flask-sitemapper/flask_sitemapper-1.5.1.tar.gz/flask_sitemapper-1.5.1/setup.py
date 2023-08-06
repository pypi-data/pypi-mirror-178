# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_sitemapper']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.2.2,<3.0.0', 'jinja2>=3.1.2,<4.0.0']

setup_kwargs = {
    'name': 'flask-sitemapper',
    'version': '1.5.1',
    'description': 'Flask extension for generating XML sitemaps',
    'long_description': '# Flask Sitemapper\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/h-janes/flask-sitemapper/Run%20Tests)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/flask-sitemapper?color=%23529AC3)\n\nFlask Sitemapper is a Python 3 package that generates XML sitemaps for Flask applications. This allows you to create fully functional sitemaps and sitemap indexes for your Flask projects with minimal code.\n\nYou can install the [latest version](https://pypi.org/project/flask-sitemapper/) of Flask Sitemapper with pip:\n```terminal\npip install flask-sitemapper\n```\n\nFor documentation (including for contributors), see [the wiki](https://github.com/h-janes/flask-sitemapper/wiki).\n\n# Features\n* Easily generate and serve XML sitemaps and sitemap indexes for your Flask apps\n* Include URLs in your sitemaps by adding a decorator to their route/view functions\n* Serve your sitemap on any URL you choose\n* Include lastmod, changefreq, and priority information in your sitemaps\n* Specify whether to use HTTP or HTTPS for the URLs in your sitemaps\n* Compress your sitemaps using GZIP\n* Create multiple sitemaps and sitemap indexes for the same app\n* Supports apps using Flask blueprints\n* Supports apps serving multiple domains\n* Works with many different app structures\n\n# Sitemaps\n> Sitemaps are an easy way for webmasters to inform search engines about pages on their sites that are available for crawling. In its simplest form, a Sitemap is an XML file that lists URLs for a site along with additional metadata about each URL (when it was last updated, how often it usually changes, and how important it is, relative to other URLs in the site) so that search engines can more intelligently crawl the site.\n> &mdash; <cite>[sitemaps.org](https://www.sitemaps.org)</cite>\n\nFor more information about sitemaps and the sitemap protocol, visit [sitemaps.org](https://www.sitemaps.org)\n\n# Basic Code Example\n```python\nimport flask\nfrom flask_sitemapper import Sitemapper\n\nsitemapper = Sitemapper()\n\napp = flask.Flask(__name__)\nsitemapper.init_app(app)\n\n@sitemapper.include(lastmod="2022-02-08")\n@app.route("/")\ndef home():\n  return flask.render_template("home.html")\n\n@sitemapper.include(lastmod="2022-03-19")\n@app.route("/about")\ndef about():\n  return flask.render_template("about.html")\n\n@app.route("/sitemap.xml")\ndef sitemap():\n  return sitemapper.generate()\n\napp.run()\n```\n\nWith the above code running on localhost, `http://localhost/sitemap.xml` will serve the following XML sitemap:\n```xml\n<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>https://localhost/</loc>\n    <lastmod>2022-02-08</lastmod>\n  </url>\n  <url>\n    <loc>https://localhost/about</loc>\n    <lastmod>2022-03-19</lastmod>\n  </url>\n</urlset>\n```',
    'author': 'h-janes',
    'author_email': 'dev@hjanes.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/h-janes/flask-sitemapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
