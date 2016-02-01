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
import random

def message(msg):
	print >>sys.stderr,msg,"..."

if __name__ == '__main__':
	random.seed(os.getpid())
	dbmanager = DBManager.DBManager();
	dbmanager.open("db");
	for x in dbmanager.query("select name,result,status from qtable order by runid"):
		message(x)
		
	for x in dbmanager.query("select name,result,status from qtable order by runid"):
		print x[1]
	dbmanager.close()	
			
	
