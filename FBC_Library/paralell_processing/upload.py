#!/usr/bin/python
#coding:utf-8
# -*- coding:utf-8 -*-
import urllib
import sqlite3
import sys
import time
import argparse
import os
import subprocess
import tempfile 
import DBManager

def message(msg):
	print >>sys.stderr,msg,"..."

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='For Facebook hackercup or GCJ')
	parser.add_argument('-g', dest='generator', action='store', help='exec binary of Generator',required=True);
	parser.add_argument('-i', dest='input', action='store', help='inputfile(original)',required=True);
	parser.add_argument('-s', dest='source', action='store', help='sourcefile',required=True);
	args = parser.parse_args()
	
	_ = open(args.source,'r');
	sourceContent = _.read();
	_.close();
	message('deleting directory "./in"')
	subprocess.check_call(["rm","-rf","./in/"]);
	message('recreating directory "./in"')
	subprocess.check_call(["mkdir","./in/"]);
	message('executing parser')
	subprocess.check_call([args.generator,args.input]);
	
	
	dbmanager = DBManager.DBManager();
	dbmanager.open("sqlite_test.db")
	dbmanager.tableCreate();
	message('uploading')
	for (runid,i) in zip(xrange(1,123456789),os.listdir("./in/")):
		_ = open("./in/"+i);
		inputContent = _.read();
		_.close();
		print >>sys.stderr,'uploading #case %02d' % runid,
		message('' if dbmanager.upload(runid,str(runid),inputContent,sourceContent) else 'SKIP')
	dbmanager.close()
	message('successful')