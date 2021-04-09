import pytest
from click.testing import CliRunner
import energy_group14
import urllib3
urllib3.disable_warnings()



def test_HealthCheck():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.HealthCheck)
    assert result.exit_code == 0
    assert result.output == 'Everything is running fine.\n'

def test_Login():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.Login, ['--username', 'admin', '--password' ,'321nimda'])
    assert result.exit_code == 0
    assert result.output == 'Login was successful!\n'

def test_ActualTotalLoad():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.ActualTotalLoad, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert '4767.82' in result.output 

def test_AggregatedGenerationPerType():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.AggregatedGenerationPerType, ['--area', 'Greece', '--timeres', 'PT60M','--productiontype', 'Fossil Gas',  '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert '1242.00' in result.output


def test_DayAheadTotalLoadForecast():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.DayAheadTotalLoadForecast, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert '4627.00' in result.output

def test_ActualvsForecast():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.ActualvsForecast, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert '5147.00' in result.output

def test_Logout():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.Logout)
    assert result.exit_code == 0
    assert result.output == 'User is now logged out\n'