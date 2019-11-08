from bottle import Bottle, redirect, request, response, route, run, static_file
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

# Serve Atom feeds.
@app.route('/atom/<all>')
def atom(all):
    logging.info("Got Atom feed request.", extra={"query": all})
    # Creates a search object to avoid duplicating URL-generation logic.
    search = arxiv.Search(
        query=all,
        id_list='',
        sort_by="lastUpdatedDate",
        sort_order="descending",
        prune=True,
        max_chunk_results=1000
    )
    # 301: permanent redirect to the arXiv-hosted URL.
    arxiv_url = search._get_url(max_results=20)
    redirect(arxiv_url, 301)

def toFeedEntry(i):
    authors = {
        "name": ", ".join(i.authors),
        "url": getAuthorsSearch(i.authors)
    }
    maybeSummary = i.get("summary_detail")
    return {
        "id": i.id,
        "url": i.get("arxiv_url"),
        "title": i.get("title"),
        "summary": maybeSummary.value if maybeSummary else None,
        "content_text": maybeSummary.value if maybeSummary else None,
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
