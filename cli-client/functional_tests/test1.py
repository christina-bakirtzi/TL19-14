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

def test_Logout():
    urllib3.disable_warnings()
    runner = CliRunner()
    result = runner.invoke(energy_group14.Logout)
    assert result.exit_code == 0
    assert result.output == 'User is now logged out\n'
