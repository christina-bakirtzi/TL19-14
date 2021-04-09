import click
import datetime
from click_option_group import optgroup, RequiredMutuallyExclusiveOptionGroup
import requests
import json
import os
import os.path
from os import path
from os.path import expanduser
import urllib3
import re
urllib3.disable_warnings()
import pprint

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
def check(email): 
    if(re.search(regex,email)):  
        return True
    else:  
        return False 

def check_cred(u, p, e):
    if u.isalnum() == False:
        click.echo('Username must be alphanumeric')
        return False
    elif " " in p:
        click.echo('Password cannot contain spaces')
        return False
    elif check(e) == False:
        click.echo('Invalid email address')
        return False
    else:
        return True

home = expanduser("~")
tokenpath = "%s/softeng19bAPI.token" % home




def HealthCheck():
    url = 'https://localhost:8765/energy/api/HealthCheck'
    res = requests.get(url, verify= False)
    status = res.json()
    if status['status'] == 'OK':
        click.echo("Everything is running fine.")
    else:
        click.echo("Error")
    return res.status_code


def Reset():
    url = 'https://localhost:8765/energy/api/Reset'
    res = requests.post(url, verify=False)
    status = res.json()
    if status['status'] == 'OK':
        click.echo("DataBase is reset")
    else:
        click.echo("Error")
    



def Login(username, password):
    if path.exists(tokenpath):
        click.echo('User already logged in')
        return -1
        
    else:
        url = 'https://localhost:8765/energy/api/Login'
        d = {'username': username, 'password': password}
        res = requests.post(url, data=d, headers={'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
        if res.status_code == 200:
            rtoken = res.json()
            fileptr = open(tokenpath, "w+")
            json.dump(rtoken, fileptr)
            fileptr.close()
            click.echo('Login was successful!')
            
        else:
            click.echo(res.text)
        return res.status_code
    
  
    



def Logout():
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        url = 'https://localhost:8765/energy/api/Logout'
        res = requests.post(url, headers= {'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        fileptr.close()
        os.remove(tokenpath)
        if res.status_code==200:
            click.echo('User is now logged out')
            
        else:
            click.echo(res.text)
        return res.status_code
        
    else:
        click.echo('No user is logged in')
        return -1
        



def ActualTotalLoad(area, timeres, date, month, year, format):
    if date != None:
        mydate = date.strftime("%Y-%m-%d")
        datetype = 'date'
    elif month != None:
        mydate = month.strftime("%Y-%m")
        datetype = 'month'
    elif year != None:
        mydate = year.strftime("%Y")
        datetype = 'year'
    else:
        click.echo("No valid date in the form of YYYY-MM-DD or YYYY-MM or YYYY")
        return -1
    if format not in ['json', 'csv']:
        click.echo('Format must be either json or csv')
        return -1
    url = 'https://localhost:8765/energy/api/ActualTotalLoad/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json(), sort_dicts =False)
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)
        return res.status_code
        
    else:
        click.echo("You must be logged in to execute this command")
        return -1
        

ptList = ['Fossil Gas', 'Hydro Run-of-river and poundage', 'Hydro Pumped Storage', 'Hydro Water Reservoir', 'Fossil Hard coal', 'Nuclear', 
'Fossil Brown Coal/Lignite','Fossil Oil','Fossil Oil shale','Biomass','Fossil Peat','Wind Onshore','Other', 'Wind Offshore',
'Fossil Coal-derived gas', 'Waste', 'Solar', 'Geothermal', 'Other renewable', 'Marine', 'AC Link', 'Transformer', 'DC Link', 'Substation', 'AllType' ]



def AggregatedGenerationPerType(area, timeres, productiontype, date, month, year, format):
    if date != None:
        mydate = date.strftime("%Y-%m-%d")
        datetype = 'date'
    elif month != None:
        mydate = month.strftime("%Y-%m")
        datetype = 'month'
    elif year != None:
        mydate = year.strftime("%Y")
        datetype = 'year'
    else:
        click.echo("No valid date in the form of YYYY-MM-DD or YYYY-MM or YYYY")
        return -1
    if format not in ['json', 'csv']:
        click.echo("Format")
        return -1
    url = 'https://localhost:8765/energy/api/AggregatedGenerationPerType/' + area + '/' + productiontype + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json(), sort_dicts =False)
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)
        return res.status_code
        
    else:
        click.echo("You must be logged in to execute this command")
        return -1
        


def DayAheadTotalLoadForecast(area, timeres, date, month, year, format):
    if date != None:
        mydate = date.strftime("%Y-%m-%d")
        datetype = 'date'
    elif month != None:
        mydate = month.strftime("%Y-%m")
        datetype = 'month'
    elif year != None:
        mydate = year.strftime("%Y")
        datetype = 'year'
    else:
        click.echo("No valid date in the form of YYYY-MM-DD or YYYY-MM or YYYY")
        return -1
    if format not in ['json', 'csv']:
        click.echo("Format")
        return -1
    url = 'https://localhost:8765/energy/api/DayAheadTotalLoadForecast/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json(), sort_dicts =False)
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)
        return res.status_code
        
    else:
        click.echo("You must be logged in to execute this command")
        return -1
        


def ActualvsForecast(area, timeres, date, month, year, format):
    if date != None:
        mydate = date.strftime("%Y-%m-%d")
        datetype = 'date'
    elif month != None:
        mydate = month.strftime("%Y-%m")
        datetype = 'month'
    elif year != None:
        mydate = year.strftime("%Y")
        datetype = 'year'
    else:
        click.echo("No valid date in the form of YYYY-MM-DD or YYYY-MM or YYYY")
        return -1
    if format not in ['json', 'csv']:
        click.echo("Format")
        return -1
    url = 'https://localhost:8765/energy/api/ActualvsForecast/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token'] }, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json(), sort_dicts =False)
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)
        return res.status_code
        
    else:
        click.echo("You must be logged in to execute this command")
        return -1
        



def Admin(newuser, moduser, userstatus, newdata, password, email, quota, source):
    if newuser != None:
        if password != None and email !=None and quota != None:
            if check_cred(newuser, password, email):
                url = 'https://localhost:8765/energy/api/Admin/users'
                if path.exists(tokenpath):
                    fileptr = open(tokenpath, 'r')
                    rtoken = json.load(fileptr)
                    fileptr.close()
                    userdata = {'username': newuser, 'password': password, 'email': email, 'quota': quota}
                    res = requests.post(url, data=userdata, headers={'X-OBSERVATORY-AUTH': rtoken['token'], 'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
                    click.echo(res.text)
                    return res.status_code
                
                else:
                    click.echo("You must be logged in and have adminstrator privileges to execute this command")
                    return -1
            else:
                return 0
        else:
            click.echo("Password, email or quota is missing")   
            return -1


    elif moduser != None:
        if password != None or email != None or quota != None:
            url = 'https://localhost:8765/energy/api/Admin/users/' + moduser
            b=True
            if path.exists(tokenpath):
                fileptr = open(tokenpath, 'r')
                rtoken = json.load(fileptr)
                fileptr.close()
                if password != None and email == None and quota == None:
                    userdata = {'username': moduser, 'password': password}
                if email != None and password == None and quota == None:
                    if check(email):
                        userdata = {'username': moduser, 'email': email}
                    else:
                        b=False
                if quota != None and password == None and email == None:
                    userdata = {'username': moduser, 'quota': quota}
                if password != None and email != None and quota == None:
                    if check(email):
                        userdata = {'username': moduser, 'password': password, 'email': email}
                    else:
                        b=False
                if password != None and email == None and quota != None:
                    userdata = {'username': moduser, 'password': password, 'quota': quota}
                if password == None and email != None and quota != None:
                    if check(email):
                        userdata = {'username': moduser, 'quota': quota, 'email': email}
                    else:
                        b=False
                if password != None and email != None and quota != None:
                    if check(email):
                        userdata = {'username': moduser, 'password': password, 'email': email, 'quota': quota}
                    else:
                        b=False
                if b:
                    res = requests.put(url, data=userdata, headers={'X-OBSERVATORY-AUTH': rtoken['token'],
                                                                'Content-Type': 'application/x-www-form-urlencoded'},
                                   verify=False)
                    click.echo(res.text)
                    return 0
                else:
                    click.echo("Non valid email")
                    return -1
            else:
                click.echo("You must be logged in and have adminstrator privileges to execute this command")
                return 0
        else:
            click.echo("No data for change given")
            return -1


    elif userstatus != None:
        url = 'https://localhost:8765/energy/api/Admin/users/' + userstatus
        if path.exists(tokenpath):
            fileptr = open(tokenpath, 'r')
            rtoken = json.load(fileptr)
            fileptr.close()
            res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token'], 'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
            click.echo(res.text)
            return res.status_code
            
        else:
            click.echo("You must be logged in and have adminstrator privileges to execute this command")
            return -1
            
    else:
        newdata = newdata.lower()
        if newdata == 'actualtotalload':
            url = 'https://localhost:8765/energy/api/Admin/ActualTotalLoad'
        elif newdata == 'aggregatedgenerationpertype':
            url = 'https://localhost:8765/energy/api/Admin/AggregatedGenerationPerType'
        elif newdata == 'dayaheadtotalloadforecast':
            url = 'https://localhost:8765/energy/api/Admin/DayAheadTotalLoadForecast'
        else:
            click.echo('Data must be ActualTotalLoad or AggregatedGenerationPerType or DayAheadTotalLoadForecast')
            return -1
        if path.exists(tokenpath):
            fileptr = open(tokenpath, 'r')
            rtoken = json.load(fileptr)
            fileptr.close()
            if path.exists(source):
                uploadfile = {'file': open(source, 'rb')}
                res = requests.post(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, files=uploadfile, verify=False)
                pprint.pprint(res.json(), sort_dicts =False)
                return res.status_code
                
            else:
                click.echo("Upload file path does not exist")
                return -1
                
        else:
            click.echo("You must be logged in and have adminstrator privileges to execute this command")
            return -1
            

