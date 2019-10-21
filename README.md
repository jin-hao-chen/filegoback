# File Go

**File Go is a toy website combined with Vue.js, Flask, Nginx and MySQL**

---

# Contents

* [Instruction](#instruction)
* [Environment](#environment)
* [Installation](#installation)
    * [CentOS Users](#centos-users)
* [TODO](#todo)


## Instruction
filegoback is a file upload backend project, you can access the fontend project *filegofront* at this link(Wow, I'll add it later).

## Environment
1. OS version is CentOS 7
2. Python version is Python3
3. I recommend you to use python3 in virtual environment
4. Server can connect Baidu API :-)

## Installation

### CentOS Users

1. `pip install -r requirements.txt` install dependencies
2. `yum install vim nginx mariadb* -y`
8. `yum install kde-l10n-Chinese` support chinese
9. `yum groupinstall fonts`
9. `echo export LANG="en_US.UTF-8" >> ~/.bashrc`
12. `yum install system-config-language`
13. `system-config-language` set chinese
10. `init 6`
11. `setenforce 0`
3. `systemctl stop firewalld`
4. `systemctl start mariadb`
5. `mysql_secure_installation` set password for root
7. modify apps/__init__.py to set password correct

7. `mysql -uroot -pYourPassword` get into mysql shell to setup database
    1. `create database file_go character set=utf8mb4`
    2. `python manager.py db init`
    3. `python manager.py db migrate`
    4. `python manager.py db upgrade`
    5. `source ./data.sql` actually for private, ./data.sql won't be provided here, what data.sql do is insert some data into student and category tables
8. `mkdir sends uploads` if there is no `sends` and `uploads` dir at our project
9. `gunicorn -w 4 -b 127.0.0.1:5000 run:app` start api server
    1. if you want server to run in background, use `nohup gunicorn -w 4 -b 127.0.0.1:5000 run:app &`
    2. if you want run it in development mode, use `python manager.py runserver`
10. `cp nginx.conf /etc/nginx/nginx.conf` the template file is at ./nginx.conf
11. `nginx -t` check out if our config is right
12. `systemctl restart nginx`


## TODO
* [ ] Provide Docker version
* [ ] Add actual Admin mode
