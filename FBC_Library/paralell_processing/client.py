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
	pid = str(os.getpid())
	cppfilename = "/tmp/" + pid + ".cpp";
	exefilename = "/tmp/" + pid + ".out";
	infilename = "/tmp/" + pid + ".in";
	subprocess.check_call(["rm","-f",cppfilename]);
	subprocess.check_call(["rm","-f",exefilename]);
	subprocess.check_call(["touch",cppfilename]);
	random.seed(os.getpid())
	while True:
		try:
			dbmanager.open("sqlite_test.db")
			runid = dbmanager.getNewRunID()
			if runid != None :
			
				_,name,input,cpp,_,_ = dbmanager.getQuery(runid);
				
				if dbmanager.newToPending(runid): 
					dbmanager.close();
					try:
						_ = open(cppfilename,"r");
						# コンパイル
						if cpp != _.read() : 
							_.close()
							_ = open(cppfilename,"w")
							_.write(cpp)
							_.close()
							subprocess.check_call(["g++","-O3","-std=c++11","-o",exefilename,cppfilename]);
						else:
							_.close()
						# 入力ファイルの作成
						_ = open(infilename,"w")
						_.write(input)
						_.close()
						res = subprocess.check_output([exefilename,infilename]).rstrip();
						dbmanager.open("sqlite_test.db")
						dbmanager.changeResult(runid,res)
						dbmanager.changeStatus(runid,"ACCEPTED");
						dbmanager.close();
						message("finished"+str(runid))
					except Exception as e:
						message(str(type(e)))
						dbmanager.open("sqlite_test.db")
						dbmanager.changeStatus(runid,str(type(e)));
						dbmanager.close();
				else:
					dbmanager.close();
					#message("COLLIDED");
					time.sleep(random.random())
			else:
				dbmanager.close();
				message("NO DATA");
				time.sleep(0.8+random.random()/5.)
		except Exception as e:
			message(str(type(e)))
			time.sleep(0.8+random.random()/5.)
	dbmanager.close()	
			
	
