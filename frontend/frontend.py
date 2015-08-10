import os
import sys
from bottle import route, view, run, template, static_file
#from bottle.Bottle import get_url

print("Running using: %s" % sys.executable)

#old_html_template = r'''
#<title>Python Env</title>
#<body>
#<h1>Python Env</h1>
#<ul>
#  % for name, value in envlist.items():
#    <li><b>{{name}}</b>: <tt>{{value}}</tt></li>
#  % end
#</ul>
#</body>
#'''

html_template = r'''
<title>Frontend</title>
<body>
<h1>Frontend</h1>
<p> Hello world! </p>
</body>
'''

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/')
@view('index')
def index():
    return # { 'get_url': get_url } #template(maps_page, envlist=os.environ)

run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))
