#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import termios
import tty
import DBManager

def message(msg):
	print >>sys.stderr,msg,"..."
	
def yesno(message):
    result = ''
    sys.stdout.write(message)
    sys.stdout.flush()
    attribute = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    try:
        while True:
            char = sys.stdin.read(1)
            if char == 'y' or char == 'Y':
                result = 'y'
                break
            elif char == 'n' or char == 'N':
                result = 'n'
                break
    except KeyboardInterrupt:
        result = '^C'
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, attribute)
    print result
    return result


if __name__ == '__main__':
	result = yesno('よろしいですか? (y/n) ')
	if result == 'y':
		dbmanager = DBManager.DBManager();
		dbmanager.open("sqlite_test.db")
		dbmanager.tableDelete();
		dbmanager.close();
		message("データベースは削除されました");
	elif result == 'n':
		''''''
	elif result == '^C':
		''''''


# EOF