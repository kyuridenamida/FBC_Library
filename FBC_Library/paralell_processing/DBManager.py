#!/usr/bin/python
#coding:utf-8
# -*- coding:utf-8 -*-
import urllib
import MySQLdb
import sqlite3
import sys
import time
import argparse
import os
import subprocess
import tempfile
import client
import random

class DBManager:
	def query(self,queryString) : 
		self.cur.execute(queryString);
		res = self.cur.fetchall();
		# print res,"<<"
		return res
		
	
	def open(self,dbname): 
		self.connector = MySQLdb.connect(host="***", db="fbhc_queue", user="****", passwd="****", charset="utf8")
		self.cur = self.connector.cursor()
		
	def tableDelete(self):
		if self.query("SHOW TABLES FROM fbhc_queue LIKE 'qtable'") != () : 
			self.query("delete from qtable");
		
	def tableCreate(self):
		if self.query("SHOW TABLES FROM fbhc_queue LIKE 'qtable'") == () : 
			self.query('''create table qtable(runid integer primary key,name LONGBLOB,input LONGBLOB,cpp LONGBLOB,result LONGBLOB,status LONGBLOB)''')
		
	def upload(self,runid,name,input,cpp):
		self.query("delete from qtable where runid=%d and status!='ACCEPTED'"%runid);
		if self.query("select runid from qtable where runid=%d"%runid) == () : 
			self.query("insert into qtable values (%d ,'%s','%s','%s','%s','%s')" % (runid ,urllib.quote(name),urllib.quote(input),urllib.quote(cpp),'#','NEW') );
			return True
		else:
			return False
		
	
	def changeStatus(self,runid,status):
		self.query("update qtable set status = '%s' where runid = %d" % (urllib.quote(status),runid))
		
	def newToPending(self,runid):
		self.query("update qtable set status = '%s' where runid = %d and status='NEW'" % (urllib.quote("PENDING"),runid))
		rows_affected=self.cur.rowcount
		# print rows_affected
		return rows_affected > 0
	def changeResult(self,runid,result):
		self.query("update qtable set result = '%s' where runid = %d;" % (result,runid))
	
	def getNewRunID(self):
		res = self.query("select runid from qtable where status='NEW' limit 1")
		if res == () : return None;
		# res = list(res);
		# random.shuffle(res)
		return int(res[0][0])
	
	def getQuery(self,runid):
		res = self.query("select * from qtable where runid=%d limit 1" % runid)
		urllib.unquote(res[0][1])
		return res[0][0],urllib.unquote(res[0][1]),urllib.unquote(res[0][2]),urllib.unquote(res[0][3]),urllib.unquote(res[0][4]),urllib.unquote(res[0][5])

	
	def close(self) : 
		self.cur.close()
		self.connector.close()

	def readOnlyOpen(self,dbname) : 
		self.connector = MySQLdb.connect(host="***", db="fbhc_queue", user="****", passwd="****", charset="utf8")
		self.cur = self.connector.cursor()

	
	def readOnlyClose(self) : 
		self.cur.close()
		self.connector.close()

		
if __name__ == '__main__':
	dbmanager = DBManager();
	dbmanager.open("dbname");
	#dbmanager.close();
	