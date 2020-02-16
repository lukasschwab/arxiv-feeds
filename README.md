![Renaissance No. 5, Plate LXXVIII from Owen Jones's Grammar of Ornament](./static/header.jpg)

# arxiv-feeds

arXiv provides [RSS feeds for subject areas](https://arxiv.org/help/rss), but does not seem to provide hosted feeds by query. (See also: [arxiv/arxiv-rss](https://github.com/arXiv/arxiv-rss)).

This project provides hosted JSON and Atom feeds for [arbitrary arXiv queries](https://arxiv.org/help/api/user-manual#query_details).

## Getting started

1. Install [the Google Cloud SDK](https://cloud.google.com/sdk/install).

2. Install the application requirements: `make install`.

3. Run the dev server: `make run`.
    + Once the server is running, you can open it in your default browser: `make open`.

## Useful tools

+ [arxiv.py](https://github.com/lukasschwab/arxiv.py) provides the blood 'n' guts here.
+ Cribbed some CSS from [ditto](https://github.com/lukasschwab/ditto).
+ *A Dictionary of Color Combinations*.
+ [favicon.io](https://favicon.io/emoji-favicons/) for an emoji favicon.
+ [The JSON Feed spec](https://jsonfeed.org).

## TODO

- [ ] Cacheing.
- [ ] UI entry-point for `/atom/<all>` route.
