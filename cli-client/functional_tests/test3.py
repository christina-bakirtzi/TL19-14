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

def test_Logout():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.Logout)
    assert result.exit_code == 0
    assert result.output == 'No user is logged in\n'

def test_ActualTotalLoad():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.ActualTotalLoad, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert result.output == 'You must be logged in to execute this command\n'

def test_AggregatedGenerationPerType():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.AggregatedGenerationPerType, ['--area', 'Greece', '--timeres', 'PT60M','--productiontype', 'Fossil Oil',  '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert result.output == 'You must be logged in to execute this command\n'


def test_DayAheadTotalLoadForecast():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.DayAheadTotalLoadForecast, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert result.output == 'You must be logged in to execute this command\n'

def test_ActualvsForecast():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.ActualvsForecast, ['--area', 'Greece', '--timeres', 'PT60M', '--date', '2018-01-01'])
    assert result.exit_code == 0
    assert result.output == 'You must be logged in to execute this command\n'

def test_Admin_Functions():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.Admin, ['--newuser', 'giannis', '--password', '123', '--email', 'giannis@gmail.com', '--quota', '1'])
    assert result.exit_code == 0
    assert result.output == 'You must be logged in and have adminstrator privileges to execute this command\n'