import flask
from flask import request

import argparse
import sys
import os
from datetime import datetime
from subprocess import Popen, PIPE

app = flask.Flask(__name__)

@app.route('/picket')
def think():
	board = request.args.get('board')
	gameid = request.args.get('id')
	iterations = request.args.get('iterations', 100000)

	if(not board.isdigit() or len(board) != 65):
		return flask.Response('invalid board')

	p = Popen(('/home/richard/code/picket/picketweb', '-i', iterations, board), stdin=PIPE, stdout=PIPE, stderr=PIPE)
	p.wait()

	move = p.stdout.readline().strip().decode('utf-8')
	rawlog = p.stderr.read().strip().decode('utf-8')
	log = rawlog.replace('\n', '\\n')
	banner = log.split('\\n')[0]
	banner += ' ' + Popen(('/bin/md5sum', 'thirdrankwin.dat'), stdout=PIPE).stdout.read().decode('utf-8').split(' ')[0]
	Popen(('/usr/bin/mkdir', '-p', os.path.join('log', banner)), shell=False).wait()
	f = open(os.path.join('log', banner, gameid), 'a')
	f.write(str(datetime.now()))
	f.write('\n')
	f.write(rawlog)
	f.write('\n')
	f.close()

	r = flask.Response('{"board": "%s", "log": "%s"}' % (move, log))
	r.headers['Content-Type'] = 'application/json'
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

app.run(debug=False, port=5000)
