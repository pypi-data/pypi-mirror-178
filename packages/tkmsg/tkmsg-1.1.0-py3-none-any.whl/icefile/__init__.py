'''
Author BiliBili UID:1964068259
'''
import sys
import os
import glob

now = os.getcwd()
def current():
    return now
def write(filename,contents,mode):
    dic = f'{now}\\{filename}'
    f = open(dic,mode)
    f.write(contents)
    f.close()
def read(filename):
    dic = f'{now}\\{filename}'
    f = open(dic, "r")
    data = f.read()
    return data
def cmd(command):
    os.system(command)
def remove(path):
    os.remove(path)
def exists(path):
    if(os.path.isfile(path)):
        response = True
    else:
        response = False
    return response
def rm_all(path):
    for file in glob.glob(f'{now}/{path}/*'):
        os.remove(file)
