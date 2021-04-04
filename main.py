from bottle import Bottle, redirect, request, response, static_file
import arxiv
import time
import sys
import logging
from os import getenv
from datetime import datetime
import jsonfeed as jf
import pytz

# Log to stdout in dev.
if not getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.info("Starting arxiv-feeds.")
app = Bottle()

MAX_RESULTS = 20
ICON = "https://arxiv-feeds.appspot.com/favicons/android-chrome-512x512.png"


# Serve index.
@app.route('/')
def entry():
    logging.info("Got entry request.")
    return static_file("entry.html", root='static/')


def to_search(query):
    return arxiv.Search(
        query=query,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
        max_results=MAX_RESULTS
    )


# Serve JSON feeds.
@app.route('/json/<all>')
def json(all):
    logging.info(
        "Got JOSN feed request: {all}".format(all=all),
        extra={"query": all}
    )
    response.content_type = 'application/json'
    items = list(to_search(all).get())
    logging.info("Serving feed.", extra={"query": all, "len": len(items)})
    feed = jf.Feed(
        title="arXiv feed: `{}`".format(all),
        home_page_url="https://arxiv-feeds.appspot.com/",
        feed_url=request.url,
        description="arXiv feed for the query `{}`".format(all),
        icon=ICON,
        favicon="https://arxiv-feeds.appspot.com/favicons/favicon.ico",
        items=[toFeedEntry(item) for item in items]
    )
    return feed.toJSON(indent="\t")


# Serve Atom feeds.
@app.route('/atom/<all>')
def atom(all):
    logging.info(
        "Got Atom feed request: {all}".format(all=all),
        extra={"query": all}
    )
    # Creates a search object to avoid duplicating URL-generation logic.
    search = to_search(all)
    arxiv_url = arxiv.Client()._format_url(search, 0, MAX_RESULTS)
    # 301: permanent redirect to the arXiv-hosted URL.
    redirect(arxiv_url, 301)


def toFeedEntry(i):
    # NOTE: doesn't use jsonfeed.converters because there are special arXiv
    # values to rearrange.
    def format(t):
        dt = datetime.fromtimestamp(time.mktime(t)).replace(tzinfo=pytz.UTC)
        return dt.isoformat()
    i = jf.Item(
        id=i.get_short_id(),
        url=i.entry_id,
        title=i.title,
        summary=i.summary,
        content_text=i.summary,
        date_published=format(i.published),
        date_modified=format(i.updated),
        authors=getAuthors(i),
        tags=i.categories,
        attachments=getAttachments(i)
    )
    return i


def getAuthors(i):
    author_search = "https://arxiv.org/search/?query={}&searchtype=author"

    def to_author(name):
        return jf.Author(
            name=name,
            url=author_search.format(name.replace(" ", "+"))
        )
    return [to_author(author.name) for author in i.authors]


def getAttachments(i):
    return [jf.Attachment(
        url=i.get_pdf_url(),
        mime_type="application/pdf",
        title="{} (PDF)".format(i.title)
    )]


def getAuthorsSearch(authors):
    rootSearchString = "https://arxiv.org/search/?query={}&searchtype=author"
    formattedAuthors = "+".join(authors).replace(" ", "+")
    return rootSearchString.format(formattedAuthors)


# Serve static files generically: helpful for linking CSS/JS from HTML.
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')
