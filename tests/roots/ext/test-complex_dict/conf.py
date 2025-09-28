from __future__ import annotations

extensions = ['sphinxext.rediraffe']

master_doc = 'index'
exclude_patterns = ['_build']

html_theme = 'basic'

rediraffe_redirects = {
    'f.rst': 'c.rst',
    'q.rst': 'w.rst',
    'F2/1.rst': 'x.rst',
    'c.rst': 'd.rst',
    'i.rst': 'j.rst',
    'k.rst': 'l.rst',
    'r.rst': 'w.rst',
    'm.rst': 'n.rst',
    'n.rst': 'o.rst',
    'u.rst': 'w.rst',
    'F1/1.rst': 'F1/2.rst',
    't.rst': 'w.rst',
    'b.rst': 'c.rst',
    'g.rst': 'd.rst',
    'h.rst': 'g.rst',
    'p.rst': 'z.rst',
    'a.rst': 'b.rst',
    'd.rst': 'e.rst',
    'w.rst': 'x.rst',
    'y.rst': 'x.rst',
    'x.rst': 'z.rst',
    'v.rst': 'u.rst',
    'F1/2.rst': 'F2/1.rst',
    's.rst': 'w.rst',
    'F5/F4/F3/F2/F1/1.rst': 'index.rst',
}
