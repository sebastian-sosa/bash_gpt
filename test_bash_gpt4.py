from unittest.mock import Mock, patch

import pytest

from bash_gpt import BashGPT


def test_get_response_from_gpt4():
    bash_gpt4 = BashGPT()
    bash_gpt4.openai_client.chat.completions.create = Mock(return_value=iter([Mock(choices=[Mock(delta=Mock(content="GPT-4: Received your input: 'test'"))])]))
    assert bash_gpt4.get_response_from_gpt4([{"role": "system", "content": bash_gpt4.system_prompt}, {"role": "user", "content": 'test'}]) == "GPT-4: Received your input: 'test'"


def test_parse_bash_commands():
    bash_gpt4 = BashGPT()
    assert bash_gpt4.parse_bash_commands('<bash>ls</bash>') == ['ls']
    assert bash_gpt4.parse_bash_commands('ls') is None
    assert bash_gpt4.parse_bash_commands('<bash>ls') is None
    assert bash_gpt4.parse_bash_commands('') is None
    with pytest.raises(ValueError):
        bash_gpt4.parse_bash_commands('<bash>ls</bash><bash>pwd</bash>')  # Multiple bash tags


@patch('subprocess.run')
def test_run_bash_command(mock_run):
    bash_gpt4 = BashGPT()
    mock_run.return_value = Mock(stdout='Hello\n')
    result = bash_gpt4.run_bash_command('echo Hello')
    assert result == 'Hello\n'
    mock_run.return_value = Mock(stderr='not found', returncode=1)
    result = bash_gpt4.run_bash_command('invalid_command')
    assert 'Error:\b not found' in result


@patch('builtins.input', return_value="")
@patch('subprocess.run')
def test_execute_commands(mock_run, mock_input):
    bash_gpt4 = BashGPT()
    mock_run.return_value = Mock(stdout='Hello\n', stderr=None)  # Change this line
    result = bash_gpt4.execute_commands(['echo Hello'])
    assert result == ['Hello\n']
