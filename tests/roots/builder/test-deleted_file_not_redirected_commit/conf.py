from __future__ import annotations

import subprocess
from pathlib import Path

extensions = ['sphinxext.rediraffe']

master_doc = 'index'
exclude_patterns = ['_build']

html_theme = 'basic'

rediraffe_redirects = 'redirects.txt'

rediraffe_branch = subprocess.check_output(
    ('git', 'rev-parse', 'HEAD~1'), cwd=Path(__file__).parent
).decode('utf-8')
