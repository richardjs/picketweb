import flask
from flask import request

import argparse
import sys
from subprocess import Popen, PIPE

app = flask.Flask(__name__)

@app.route('/picket')
def think():
	board = request.args.get('board')
	gameid = request.args.get('id')

	if(not board.isdigit() or len(board) != 65):
		return flask.Response('invalid board')

	p = Popen(('/home/richard/code/picket/picket', board), stdin=PIPE, stdout=PIPE, stderr=PIPE)
	p.wait()

	move = p.stdout.readline().strip().decode('utf-8')
	log = p.stderr.read().strip().decode('utf-8').replace('\n', '\\n')

	r = flask.Response('{"board": "%s", "log": "%s"}' % (move, log))
	r.headers['Content-Type'] = 'application/json'
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

app.run(debug=False, port=5000)
