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
    if (re.search(regex, email)):
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


@click.group()
def main():
    pass


@main.command(name='HealthCheck', help='Check connectivity with DataBase')
def HealthCheck():
    url = 'https://localhost:8765/energy/api/HealthCheck'
    res = requests.get(url, verify=False)
    status = res.json()
    if status['status'] == 'OK':
        click.echo("Everything is running fine.")
    else:
        click.echo("Error")


@main.command(name='Reset', help='Resets the DataBase')
def Reset():
    url = 'https://localhost:8765/energy/api/Reset'
    res = requests.post(url, verify=False)
    status = res.json()
    if status['status'] == 'OK':
        click.echo("DataBase is reset")
    else:
        click.echo("Error")


@main.command(name='Login', help='User login if valid')
@click.option('--username', '-u', required=True, type=str, help='Username of the user')
@click.option('--password', '-p', required=True, type=str, help='Password of the user')
def Login(username, password):
    if path.exists(tokenpath):
        click.echo('User already logged in')

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


@main.command(name='Logout', help='User logout if already logged in')
def Logout():
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        url = 'https://localhost:8765/energy/api/Logout'
        res = requests.post(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        fileptr.close()
        os.remove(tokenpath)
        if res.status_code == 200:
            click.echo('User is now logged out')
        else:
            click.echo(res.text)

    else:
        click.echo('No user is logged in')


@main.command(name='ActualTotalLoad', help='Actual total energy load consumed in an area')
@click.option('--area', '-a', required=True, type=str, help='Area of interest')
@click.option('--timeres', '-t', required=True, type=str,
              help='Timeres for the data, can be one of PT15M, PT30M or PT60M')
@optgroup.group('Date', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Date of interest, can be either a date of the form YYYY-MM-DD, month of form YYYY-MM or year of form YYYY')
@optgroup.option('--date', '-d', type=click.DateTime(formats=['%Y-%m-%d']))
@optgroup.option('--month', '-m', type=click.DateTime(formats=["%Y-%m"]))
@optgroup.option('--year', '-y', type=click.DateTime(formats=["%Y"]))
@click.option('--format', '-f', default='json',
              help='Format in which the data appears, can be either json (default) or csv')
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
    if format not in ['json', 'csv']:
        click.echo('Format must be either json or csv')
    url = 'https://localhost:8765/energy/api/ActualTotalLoad/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json())
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)

    else:
        click.echo("You must be logged in to execute this command")


ptList = ['Fossil Gas', 'Hydro Run-of-river and poundage', 'Hydro Pumped Storage', 'Hydro Water Reservoir',
          'Fossil Hard coal', 'Nuclear',
          'Fossil Brown Coal/Lignite', 'Fossil Oil', 'Fossil Oil shale', 'Biomass', 'Fossil Peat', 'Wind Onshore',
          'Other', 'Wind Offshore',
          'Fossil Coal-derived gas', 'Waste', 'Solar', 'Geothermal', 'Other renewable', 'Marine', 'AC Link',
          'Transformer', 'DC Link', 'Substation', 'AllType']


@main.command(name='AggregatedGenerationPerType', help='Total energy produced in an area depending on production type')
@click.option('--area', '-a', required=True, help='Area of interest')
@click.option('--timeres', '-t', required=True, help='Timeres for the data, can be one of PT15M, PT30M or PT60M')
@click.option('--productiontype', '-pt', required=True, type=click.Choice(ptList),
              help='Production type, must be written inside " " ')
@optgroup.group('Date2', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Date of interest, can be either a date of the form YYYY-MM-DD, month of form YYYY-MM or year of form YYYY')
@optgroup.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]))
@optgroup.option('--month', '-m', type=click.DateTime(formats=["%Y-%m"]))
@optgroup.option('--year', '-y', type=click.DateTime(formats=["%Y"]))
@click.option('--format', '-f', default='json',
              help='Format in which the data appears, can be either json (default) or csv')
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
    if format not in ['json', 'csv']:
        click.echo("Format")
    url = 'https://localhost:8765/energy/api/AggregatedGenerationPerType/' + area + '/' + productiontype + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json())
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)

    else:
        click.echo("You must be logged in to execute this command")


@main.command(name='DayAheadTotalLoadForecast', help='Prediction of the total energy demand in an area the day after')
@click.option('--area', '-a', required=True, help='Area of interest')
@click.option('--timeres', '-t', required=True, help='Timeres for the data, can be one of PT15M, PT30M or PT60M')
@optgroup.group('Date3', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Date of interest, can be either a date of the form YYYY-MM-DD, month of form YYYY-MM or year of form YYYY')
@optgroup.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]))
@optgroup.option('--month', '-m', type=click.DateTime(formats=["%Y-%m"]))
@optgroup.option('--year', '-y', type=click.DateTime(formats=["%Y"]))
@click.option('--format', '-f', default='json',
              help='Format in which the data appears, can be either json (default) or csv')
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
    if format not in ['json', 'csv']:
        click.echo("Format")
    url = 'https://localhost:8765/energy/api/DayAheadTotalLoadForecast/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json())
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)

    else:
        click.echo("You must be logged in to execute this command")


@main.command(name='ActualvsForecast', help='Comparison of the actual total load vs the predicted one in an area')
@click.option('--area', '-a', required=True, help='Area of interest')
@click.option('--timeres', '-t', required=True, help='Timeres for the data, can be one of PT15M, PT30M or PT60M')
@optgroup.group('Date4', cls=RequiredMutuallyExclusiveOptionGroup,
                help='Date of interest, can be either a date of the form YYYY-MM-DD, month of form YYYY-MM or year of form YYYY')
@optgroup.option('--date', '-d', type=click.DateTime(formats=["%Y-%m-%d"]))
@optgroup.option('--month', '-m', type=click.DateTime(formats=["%Y-%m"]))
@optgroup.option('--year', '-y', type=click.DateTime(formats=["%Y"]))
@click.option('--format', '-f', default='json',
              help='Format in which the data appears, can be either json (default) or csv')
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
    if format not in ['json', 'csv']:
        click.echo("Format")
    url = 'https://localhost:8765/energy/api/ActualvsForecast/' + area + '/' + timeres + '/' + datetype + '/' + mydate + '?format=' + format
    if path.exists(tokenpath):
        fileptr = open(tokenpath, 'r')
        rtoken = json.load(fileptr)
        fileptr.close()
        res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, verify=False)
        if res.status_code == 200 and format == 'json':
            pprint.pprint(res.json())
        elif res.status_code == 200 and format == 'csv':
            click.echo(res.text)
        else:
            click.echo(res.text)

    else:
        click.echo("You must be logged in to execute this command")


@main.command(name='Admin', help='Adminstrator functions')
@optgroup.group('AdminActions', cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option('--newuser', '-nu', type=str, help='Username of the user to be created in the DataBase')
@optgroup.option('--moduser', '-mu', type=str, help='Username of an already existing user to be modified')
@optgroup.option('--userstatus', '-us', type=str, help='Username of an already existing user whose data is to be shown')
@optgroup.option('--newdata', '-nd', type=str,
                 help='Type of data to be added to the DataBase, can be one of ActualTotalLoad, AggregatedGenerationPerType or DayAheadTotalLoadForecast')
@click.option('--password', '-p', type=str, help='Password to be assigned to user or modified')
@click.option('--email', '-em', type=str, help='Email address to be assigned to user or modified')
@click.option('--quota', '-q', type=str, help="Time limit of user's actions to be assigned or modified")
@click.option('--source', '-src', help='Path to the data file to be added to the DataBase')
def Admin(newuser, moduser, userstatus, newdata, password, email, quota, source):
    if newuser != None:
        if password != None and email != None and quota != None:
            if check_cred(newuser, password, email):
                url = 'https://localhost:8765/energy/api/Admin/users'
                if path.exists(tokenpath):
                    fileptr = open(tokenpath, 'r')
                    rtoken = json.load(fileptr)
                    fileptr.close()
                    userdata = {'username': newuser, 'password': password, 'email': email, 'quota': quota}
                    res = requests.post(url, data=userdata, headers={'X-OBSERVATORY-AUTH': rtoken['token'],
                                                                     'Content-Type': 'application/x-www-form-urlencoded'},
                                        verify=False)
                    click.echo(res.text)

                else:
                    click.echo("You must be logged in and have adminstrator privileges to execute this command")
            else:
                return 0
        else:
            click.echo("Password, email or quota is missing")



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
                else:
                    click.echo("Non valid email")
            else:
                click.echo("You must be logged in and have adminstrator privileges to execute this command")
        else:
            click.echo("No data for change given")

    elif userstatus != None:
        url = 'https://localhost:8765/energy/api/Admin/users/' + userstatus
        if path.exists(tokenpath):
            fileptr = open(tokenpath, 'r')
            rtoken = json.load(fileptr)
            fileptr.close()
            res = requests.get(url, headers={'X-OBSERVATORY-AUTH': rtoken['token'],
                                             'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
            click.echo(res.text)

        else:
            click.echo("You must be logged in and have adminstrator privileges to execute this command")

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
        if path.exists(tokenpath):
            fileptr = open(tokenpath, 'r')
            rtoken = json.load(fileptr)
            fileptr.close()
            if path.exists(source):
                uploadfile = {'file': open(source, 'rb')}
                res = requests.post(url, headers={'X-OBSERVATORY-AUTH': rtoken['token']}, files=uploadfile,
                                    verify=False)
                pprint.pprint(res.json())

            else:
                click.echo("Upload file path does not exist")

        else:
            click.echo("You must be logged in and have adminstrator privileges to execute this command")


if __name__ == '__main__':
    main()
