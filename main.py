from bottle import route, request, response, run, template, static_file
import arxiv
import time

@route('/')
def entry():
    return static_file("entry.html", root='static/')

# Atom feeds aren't operational: need to get unparsed atom string from arxiv.py.
#
# @route('/atom/<all>')
# def atom(all):
#     response.content_type = 'text/xml'
#     res = arxiv.query(search_query=all, max_results=20, sort_by="lastUpdatedDate",
#         sort_order="descending", prune="True")
#     entries = ["<entry>" + e + "</entry>" for e in res].join("\n")
#
#     return """
#     <?xml version="1.0" encoding=\"utf-8\"?>
#     <feed xmlns=\"http://www.w3.org/2005/Atom\">
#     <title type=\"text\">
#     """ + entries + "</feed>"

@route('/json/<all>')
def json(all):
    response.content_type = 'application/json'
    items = arxiv.query(
        search_query=all,
        max_results=20,
        sort_by="lastUpdatedDate",
        sort_order="descending",
        prune=True
    )
    items = [timesToStrings(item) for item in items]
    # TODO: order reuturn values to have feed metadata at the top.
    return {
        "version": "https://jsonfeed.org/version/1",
        "title": "arXiv feed: " + all, # FIXME
        "home_page_url": "https://lukasschwab.github.io", # FIXME
        "feed_url": request.url,
        "items": items
    }

def timesToStrings(entry):
    for timekey in ['updated_parsed', 'published_parsed']:
        entry[timekey] = time.strftime('%Y-%m-%dT%H:%M:%SZ', entry[timekey])
    return entry

# Serve static files generically: helpful for linking CSS/JS from HTML.
@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

run(host='localhost', port=8080, reloader=True)
