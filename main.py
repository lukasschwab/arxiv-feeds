from bottle import route, request, response, run, template, static_file, Bottle
import arxiv
import time, sys, logging
from os import getenv

# Log to stdout in dev.
if not getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.info("Starting arxiv-feeds.")
app = Bottle()

# Serve index.
@app.route('/')
def entry():
    logging.info("Got entry request.")
    return static_file("entry.html", root='static/')

# Serve JSON feeds.
@app.route('/json/<all>')
def json(all):
    logging.info("Got feed request.", extra={"query": all})
    response.content_type = 'application/json'
    items = arxiv.query(
        search_query=all,
        max_results=20,
        sort_by="lastUpdatedDate",
        sort_order="descending",
        prune=True
    )
    logging.info("Serving feed.", extra={ "query": all, "len": len(items) })
    return {
        "version": "https://jsonfeed.org/version/1",
        "home_page_url": "https://arxiv.org/", # FIXME
        "icon": "https://arxiv-feeds.appspot.com/favicons/android-chrome-512x512.png",
        "favicon": "https://arxiv-feeds.appspot.com/favicons/favicon.ico",
        "title": "arXiv feed: `{}`".format(all),
        "description": "arXiv feed for the query `{}`".format(all),
        "feed_url": request.url,
        "items": [toFeedEntry(item) for item in items]
    }

def toFeedEntry(i):
    authors = {
        "name": ", ".join(i.authors),
        "url": getAuthorsSearch(i.authors)
    }
    # TODO: IDs should be immutable; these cahnge with versions.
    return {
        "id": i.id,
        "url": i.get("arxiv_url"),
        "title": i.get("title"),
        "summary": i.get("summary_detail.value"),
        "content_text": i.get("summary_detail.value"),
        "date_published": i.get("published"),
        "date_modified": i.get("date_modified"),
        "author": authors,
        "tags": [tag.term for tag in i.tags],
        "attachments": getAttachments(i)
    }

def getAttachments(i):
    return [{
        "url": i.pdf_url,
        "mime_type": "application/pdf",
        "title": "{} (PDF)".format(i.title)
    }]

def getAuthorsSearch(authors):
    rootSearchString = "https://arxiv.org/search/?query={}&searchtype=author"
    formattedAuthors = "+".join(authors).replace(" ", "+")
    return rootSearchString.format(formattedAuthors)

# Serve static files generically: helpful for linking CSS/JS from HTML.
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')
