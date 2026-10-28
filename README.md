# Bitcoin from Scratch: Interactive Edition

The full text of **Bitcoin from Scratch: Build Your Own Bitcoin Chain**, as a website where
every code cell runs in your browser.

**Read it:** https://aaron-recompile.github.io/bitcoin-from-scratch-interactive/

Eighteen chapters build Bitcoin from a single byte to a multi-node network using nothing but
the Python standard library. Code cells run client-side in [Pyodide](https://pyodide.org), so
there is no server, no Binder queue, and nothing to install.

Other formats: [PDF / EPUB on Leanpub](https://leanpub.com/bitcoin-from-scratch) ·
[code-only notebooks](https://github.com/aaron-recompile/bitcoin-from-scratch-code)

## How the site is built

```
book/            chapters: Jupyter notebooks (prose + code) and Markdown pages
index.md         landing page and table of contents
myst.yml         site config (Jupyter Book 2 / MyST); `jupyter.lite: true` turns on in-browser Python
tools/           import script and the Pyodide test runner
```

Every push to `main` runs [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml):

1. runs every code cell of every chapter in Pyodide (the same Python readers get), then
2. builds the site with `myst build --html --execute --strict`, executing every notebook so the
   outputs on the page are real, and failing on any error, then
3. deploys to GitHub Pages.

## Editing

Open the repo in **Codespaces** (Code → Codespaces → Create). The dev container installs
everything; then run `npm start` for a live preview on port 3000.

The chapters in `book/` are generated from the author's manuscript with
`python tools/import_from_book.py <manuscript-repo>`. Edit the manuscript and re-import rather
than editing `book/` by hand.

## License

Text: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). Code: MIT.
See [LICENSE](LICENSE).

**This is teaching code. Never use it with real money.**
