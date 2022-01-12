AUTHOR = "Tom Carrick"
SITENAME = "Tom Carrick"
SITEURL = "http://localhost:8000"

HTML_TITLE_SUBTITLE = "Web development consultat using Pythong &amp; Django"

PATH = "content"
THEME = "themes/carrick-eu"

TIMEZONE = "Europe/Amsterdam"

DEFAULT_DATE_FORMAT = r"%-d %B %-Y"
DEFAULT_LANG = "en-GB"

USE_FOLDER_AS_CATEGORY = False

ARTICLE_PATHS = ["articles"]
ARTICLE_SAVE_AS = "blog/{slug}/index.html"
ARTICLE_URL = "blog/{slug}/"
INDEX_SAVE_AS = "blog/index.html"
PAGE_SAVE_AS = "{slug}/index.html"
PAGE_URL = "{slug}/"

PAGE_ORDER_BY = "order"

# Feed generation is usually not desired when developing.
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll.
LINKS = []

# Social widget.
SOCIAL = [
    ("GitHub", "https://github.com/knyghty"),
]

DEFAULT_PAGINATION = 10

# Sitemap.
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "pages": 0.5, "indexes": 0.2},
    "changefreqs": {"articles": "yearly", "pages": "monthly", "indexes": "weekly"},
}

# Webassets.
WEBASSETS_CONFIG = [
    ("url_expire", True),
]
