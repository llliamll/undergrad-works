import sqlite3 as lite
import csv
import re
import pandas as pd
import argparse
import collections
import json
import glob
import math
import os
import requests
import string
import sqlite3
import sys
import time
import xml


class Movie_db(object):
    def __init__(self, db_name):
        # db_name: "cs1656-public.db"
        self.con = lite.connect(db_name)
        self.cur = self.con.cursor()

    # q0 is an example
    def q0(self):
        query = '''SELECT COUNT(*) FROM Actors'''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q1(self):
        query = '''
            SELECT fname, lname
            FROM Actors as a, Movies as m, Movies as m1, Cast as c, Cast as c1
            WHERE c.aid = a.aid AND c.mid = m.mid AND m.year BETWEEN 1980 and 1990
                AND c1.aid = a.aid AND c1.mid = m1.mid AND m1.year >= 2000
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q2(self):
        self.cur.execute('''DROP VIEW IF EXISTS q2view''')
        self.cur.execute('''CREATE VIEW q2view as SELECT year, rank FROM Movies WHERE title = "Rogue One: A Star Wars Story" GROUP BY year''')
        query = '''
            SELECT title, m.year
            FROM Movies as m, q2view
            WHERE m.year == q2view.year AND m.rank > q2view.rank
            ORDER BY title asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q3(self):
        query = '''
            SELECT fname, lname, COUNT(*) as cnt
            FROM Cast as c, Actors as a, Movies as m
            WHERE c.aid = a.aid AND c.mid = m.mid AND m.title LIKE '%Star Wars%'
            GROUP BY fname, lname
            ORDER BY cnt desc, lname asc, fname asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q4(self):
        self.cur.execute('''DROP VIEW IF EXISTS post1980''')
        self.cur.execute('''
            CREATE VIEW post1980 as
            SELECT a2.fname, a2.lname 
            FROM Actors as a2, Cast as c2, Movies as m2
            WHERE c2.aid = a2.aid AND c2.mid = m2.mid AND m2.year >= 1980
        ''')
        query = '''
            SELECT a.fname, a.lname
            FROM Actors as a, Cast as c, Movies as m
            WHERE c.aid = a.aid AND c.mid = m.mid AND m.year < 1980 AND (a.fname NOT IN (SELECT fname FROM post1980)AND a.lname NOT IN (SELECT lname FROM post1980))
            GROUP BY a.fname, a.lname
            ORDER BY a.lname asc, a.fname asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q5(self):
        query = '''
            SELECT fname, lname, COUNT(*) as cnt
            FROM Movie_Director as md NATURAL JOIN Directors as d
            GROUP BY fname, lname
            ORDER BY cnt desc, lname asc, fname asc
            LIMIT 10
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q6(self):
        query = '''
            SELECT title, COUNT(*) as cnt
            FROM Cast as c NATURAL JOIN Movies as m
            GROUP BY c.mid
            HAVING cnt >= (SELECT min(cnt)
                FROM(SELECT COUNT(*) as cnt
                    FROM Cast as c
                    GROUP BY c.mid
                    ORDER BY cnt desc
                    LIMIT 10))
            ORDER BY cnt desc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q7(self):
        query = '''
            SELECT m.title, SUM(case when a.gender = 'Female' then 1 else 0 end) as f_cnt, SUM(case when a.gender = 'Male' then 1 else 0 end) as m_cnt
            FROM Cast as c NATURAL JOIN Actors as a NATURAL JOIN Movies as m
            GROUP BY m.title
            HAVING f_cnt > m_cnt
            ORDER BY m.title asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q8(self):
        self.cur.execute('''DROP VIEW IF EXISTS pair''')
        self.cur.execute('''
            CREATE VIEW pair AS
            SELECT a.fname as af, a.lname as al, d.fname as df, d.lname as dl
            FROM Actors as a, Cast as c, Movie_Director as md, Directors as d
            WHERE a.aid = c.aid AND md.mid = c.mid AND md.did = d.did
        ''')
        query = '''
            SELECT af, al, COUNT(DISTINCT df || dl) as cnt
            FROM pair
            WHERE af <> df AND al <> dl
            GROUP BY af, al
            HAVING cnt >= 7
            ORDER BY cnt desc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q9(self):
        self.cur.execute('''DROP VIEW IF EXISTS name_d''')
        self.cur.execute('''
            CREATE VIEW name_d as
            SELECT a.fname, a.lname, m.year as debut
            FROM Actors as a, Cast as c, Movies as m
            WHERE a.aid = c.aid AND c.mid = m.mid AND a.fname LIKE 'D%' AND m.year IN (
                SELECT min(year) FROM Movies as m2 NATURAL JOIN Cast as c2 NATURAL JOIN Actors as a2
                WHERE a2.fname = a.fname AND a2.lname = a.lname)
        ''')
        query = '''
            SELECT a.fname, a.lname, COUNT(*) as cnt
            FROM Actors as a, Cast as c, Movies as m, name_d
            WHERE a.aid = c.aid AND m.mid = c.mid 
                AND (m.year = name_d.debut AND a.fname = name_d.fname AND a.lname = name_d.lname)
            GROUP BY a.fname, a.lname
            ORDER BY cnt desc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q10(self):
       # self.cur.execute('''DROP VIEW IF EXISTS ''')
        query = '''
            SELECT a.lname, m.title
            FROM Actors as a, Cast as c, Movies as m, (
                SELECT d.lname, m.title
                FROM Movies as m, Movie_Director as md, Directors as d
                WHERE m.mid = md.mid AND d.did = md.did
            ) as d_name
            WHERE a.aid = c.aid AND m.mid = c.mid AND (a.lname = d_name.lname AND m.title = d_name.title)
            ORDER BY a.lname asc, m.title asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q11(self):
        self.cur.execute('''DROP VIEW IF EXISTS bacon_1''')
        self.cur.execute('''DROP VIEW IF EXISTS bacon_2''')
        self.cur.execute('''
            CREATE VIEW bacon_1 as 
            SELECT a.fname, a.lname, m.mid
            FROM Actors as a, Cast as c, Movies as m, (
                SELECT m.mid 
                FROM Actors as a, Cast as c, Movies as m
                WHERE a.aid = c.aid AND m.mid = c.mid AND (a.fname = 'Kevin' AND a.lname = 'Bacon')
            ) as bacon_movie
            WHERE a.aid = c.aid AND m.mid = c.mid AND m.mid = bacon_movie.mid AND ((a.fname || a.lname) <> 'KevinBacon')
        ''')
        self.cur.execute('''
            CREATE VIEW bacon_2 as
            SELECT a.fname, a.lname, c.mid
            FROM Actors as a, Cast as c
            WHERE a.aid = c.aid AND ((a.fname || a.lname) IN (SELECT fname||lname FROM bacon_1)) AND (c.mid NOT IN (SELECT mid FROM bacon_1))
        ''')
        query = '''
            SELECT a.fname, a.lname
            FROM Actors as a, Cast as c, bacon_2
            WHERE a.aid = c.aid AND c.mid = bacon_2.mid AND ((a.fname || a.lname) NOT IN (SELECT fname || lname FROM bacon_2))
            ORDER BY a.lname asc, a.fname asc
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows

    def q12(self):
        query = '''
            SELECT a.fname, a.lname, COUNT(*) as cnt, AVG(m.rank) as rank
            FROM Actors as a, Cast as c, Movies as m
            WHERE a.aid = c.aid AND m.mid = c.mid 
            GROUP BY a.fname, a.lname
            ORDER BY rank desc
            LIMIT 20
        '''
        self.cur.execute(query)
        all_rows = self.cur.fetchall()
        return all_rows


if __name__ == "__main__":
    task = Movie_db("cs1656-public.db")
    rows = task.q0()
    print(rows)
    print()
    rows = task.q1()
    print(rows)
    print()
    rows = task.q2()
    print(rows)
    print()
    rows = task.q3()
    print(rows)
    print()
    rows = task.q4()
    print(rows)
    print()
    rows = task.q5()
    print(rows)
    print()
    rows = task.q6()
    print(rows)
    print()
    rows = task.q7()
    print(rows)
    print()
    rows = task.q8()
    print(rows)
    print()
    rows = task.q9()
    print(rows)
    print()
    rows = task.q10()
    print(rows)
    print()
    rows = task.q11()
    print(rows)
    print()
    rows = task.q12()
    print(rows)
    print()
