from flask import Flask, request, render_template
import json
import time
import sys
from collections import defaultdict
from threading import Thread
import requests
import os
import traceback
import time
import threading

__version__ = __VERSION__ = '0.0.2'

app = Flask("ipywidget-jsonschema",
           static_url_path='/static', 
            static_folder=f'{os.path.dirname(__file__)}/build/static',
            template_folder=f'{os.path.dirname(__file__)}/build')

# 跨域支持
def after_request(response):
    #JS前端跨域支持
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "x-requested-with,content-type"
    return response


@app.route("/", methods=['get', 'POST'])
def web():
    return render_template('index.html', content="Hello World!")

@app.route("/schema", methods=['get', 'POST'])
def schema():
    channel = request.args.get("channel")
    jsonSchema = get_state()['channel'][channel]['jsonSchema']
    uiSchema = get_state()['channel'][channel]['uiSchema']
    formData = get_state()['channel'][channel]['formData']
    return {"jsonSchema": jsonSchema,
            "uiSchema": uiSchema,
           "formData": formData}

@app.route("/event", methods=['GET', 'POST', 'OPTIONS'])
def event():
    channel = request.args.get("channel")
    action = request.args.get("action")
    form_data = request.get_json(silent=True)
    try:
        get_state()['channel'][channel][action](form_data)
    except:
        pass
    return {"status": 'success'}, 200

app.after_request(after_request)

def get_avail_port():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def daemon(a):
    global JSState
    import logging
    log = logging.getLogger('werkzeug')
    log.disabled = True
    port = get_avail_port()
    JSState['port'] = port
    app.run(host="0.0.0.0", 
        port=port, 
        debug=False, 
        use_reloader=False)
    
import threading
import time
import sys
from io import StringIO
JSState = None
channel_max = 0
def daemon_init():
    global JSState
    if JSState is None:
        JSState = {'channel':{}}
        _o = sys.stdout
        sys.stdout = StringIO()
        threading.Thread(target=daemon, args=(None, )).start()
        time.sleep(0.2)
        sys.stdout = _o
        
def allocate_channel():
    global channel_max
    channel_max += 1
    return str(channel_max - 1)

def get_state():
    global JSState
    return JSState
    
def create_jsonschema(jsonschema = {},
                      uischema = {},
                      formdata = {},
        changed = lambda x: None,
        submitted = lambda x: None,
        errors = lambda x: None,
    ):
    c = allocate_channel()
    cs = {
        'jsonSchema': jsonschema,
        'uiSchema': uischema,
        'formData': formdata,
        'changed': changed,
        'submitted': submitted,
        'errors': errors
    }
    get_state()['channel'][c]  = cs
    return c, get_state()['port']
    
def jsonschema_emit(channel,
        changed = None,
        submitted = None,
        errors = None):
    cs = get_state()['channel'][c] 
    if changed is not None:
        cs['changed'] = changed
    if submitted is not None:
        cs['submitted'] = submitted
    if errors is not None:
        cs['errors'] = errors
    return True

from IPython.display import IFrame
from ipywidget_jsonschema_embed import jsonschema_emit, create_jsonschema, get_state
class JSONSchemaEmbed():
    def __init__(self, json_schema={}, ui_schema={}, form_data={}, width="100%", height="200px"):
        # super(self).__init__()
        daemon_init()
        c, p = create_jsonschema(json_schema, 
                         ui_schema,
                         form_data,
                      changed=lambda x: None,
                      submitted=lambda x: None,
                      errors=lambda x: None
                     )
        self.channel = c
        self.port = p
        self.iframe = IFrame(src=f"/proxy/{p}/?channel={c}", width=width, height=height)
        
    def state(self):
        return get_state()
    
    def __repr__(self):
        display(self.iframe)
        return ""
    

