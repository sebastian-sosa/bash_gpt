import os
import re
import subprocess
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI


class BashGPT:
    with open('system_prompt.txt', 'r') as file:
        system_prompt = file.read()

    def __init__(self):
        load_dotenv()
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response_from_gpt4(self, chat_history: List[str]) -> str:
        chat_stream = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=chat_history,
            stream=True,
        )
        gpt4_response = ""
        for part in chat_stream:
            gpt4_response += part.choices[0].delta.content or ""

        return gpt4_response

    def parse_bash_commands(self, gpt4_response: str) -> Optional[str]:
        bash_commands = re.findall(r'<bash>(.*?)</bash>', gpt4_response, re.DOTALL)
        return bash_commands if bash_commands else None

    def run_bash_command(self, command: str) -> str:
        command_result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if command_result.returncode != 0:
            return f'Error:\b {command_result.stderr}'
        return command_result.stdout

    def execute_commands(self, commands: List[str]) -> List[str]:
        results = []
        for command in commands:
            print(f"Command to run: {command}")
            execute = input("Press enter to execute, any other key to abort: ")
            if execute == "":
                result = self.run_bash_command(command)
                print(f"Command output: {result}")
                results.append(result)
            else:
                print("Command execution aborted by user.")
        return results


def main() -> None:
    while True:
        user_input = input("User: ")
        bash_gpt = BashGPT()
        chat_history = [
            {"role": "system", "content": bash_gpt.system_prompt},
            {"role": "user", "content": user_input},
        ]
        while True:
            gpt4_response = bash_gpt.get_response_from_gpt4(chat_history)
            bash_commands = bash_gpt.parse_bash_commands(gpt4_response)
            if bash_commands:
                results = bash_gpt.execute_commands(bash_commands)
                chat_history.append({"role": "assistant", "content": gpt4_response})
                for command, result in zip(bash_commands, results):
                    chat_history.append({
                        "role": "assistant",
                        "content": f'command: `{command}` result: `{result}`'
                    })
            else:
                print(gpt4_response)
                break


if __name__ == "__main__":
    main()
