import os
import sys
from bottle import route, run, template

print("Running using: %s" % sys.executable)

html_template = r'''
<title>Python Env</title>
<body>
<h1>Python Env</h1>
<ul>
  % for name, value in envlist.items():
    <li><b>{{name}}</b>: <tt>{{value}}</tt></li>
  % end
</ul>
</body>
'''

@route('/')
def index():
    return template(html_template, envlist=os.environ)

run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
