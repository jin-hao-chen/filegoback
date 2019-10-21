#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJ_DIR)
import pymysql
import datetime
import fire
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from libs import email_sender
from apps import utils

sender = email_sender.EmailSender(sender='jin_hao_chen',
                                  password='Man12138',
                                  receiver='jin_hao_chen@163.com')

connection = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='Ac_superman',
                             db='file_go',
                             charset='utf8mb4')

scheduler = BlockingScheduler()

def send_zipfile_to_teacher():
    print('Running send_zipfile_to_teacher')
    cursor = connection.cursor()
    sql = """
    SELECT name FROM category WHERE is_current = 1 
    """
    cursor.execute(sql)
    category = cursor.fetchone()[0]
    cursor.close()
    email_sender.zip_dir('./uploads/' + category, './sends/' + category + '.zip')
    msg = sender.make_msg_with_zipfile('计科1701算法导论作业: ' + category,
                                 utils.get_datetime(),
                                 '计科1701算法导论作业: ' + category,
                                 './sends/', category + '.zip')
    sender.send(msg)
    print('DONE')
    scheduler.remove_job('send_zipfile_to_teacher')


def run(year, month, day, hour, minute):
    target = datetime.datetime(year, month, day, hour, minute)
    scheduler.add_job(func=send_zipfile_to_teacher,
                      next_run_time=target,
                      id='send_zipfile_to_teacher')
    scheduler.start()


def main():
    fire.Fire()


if __name__ == '__main__':egg
    main()