import os
from sys import argv
from sys import exit
from google import genai
from google.genai import types
from dotenv import load_dotenv
from time import sleep
# Import schemas for AI
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
# Import actual functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

# Variables
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

If no path is given, scan all the files in order to try and find the file. Always assume the 'main.py' as a main script file.
If something need to be fixed, run the script, analyze the output and then scan the file and fix it.

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

verbose_color = '\033[33m'
func_color = '\033[35m'
separator = '-' * 20

# Slow-printing effect
def print_slow(text):
    for letter in text:
        print(letter, end='', flush=True)
        sleep(0.01)
    print()

# Print full report
def print_full_report(prompt, response):
    print()
    print_slow(separator)
    print_slow(f'{verbose_color}User prompt:\033[0m {prompt}')
    print()
    print_slow(f'{verbose_color}Final response:\033[0m')
    if response.function_calls:
        function_result = call_function(response.function_calls[0], verbose=True)
        print_slow(function_result.parts[0].function_response.response['result'])
    else:
        print_slow(response.text)
    print()
    print_slow(f'{verbose_color}Prompt tokens:\033[0m {response.usage_metadata.prompt_token_count}')
    print_slow(f'{verbose_color}Response tokens:\033[0m {response.usage_metadata.candidates_token_count}')
    print_slow(separator)
    print()

# Print just the response
def print_response(response):
    print()
    print_slow(separator)
    print_slow(f'{verbose_color}Final response:\033[0m')
    if response.function_calls:
        function_result = call_function(response.function_calls[0])
        print_slow(function_result.parts[0].function_response.response['result'])
    else:
        print_slow(response.text)
    print_slow(separator)
    print()

# Check for arguments
def check_args(sys_arg):
    args = argv[1:]
    if not args:
        print_slow('\033[31mError! No prompt provided!\033[0m')
        print_slow('Usage: python main.py "Your prompt here" [optional --verbose]\033[0m')
        exit(1)
    if args[-1] == '--verbose':
        return ' '.join(args[:-1]), True
    else:
        return ' '.join(args), False

# Call a function
def call_function(function_call_part, verbose=False):
    available_functions = {
            'get_files_info': get_files_info,
            'get_file_content': get_file_content,
            'write_file': write_file,
            'run_python_file': run_python_file,
            }
    function_name = function_call_part.name

    if function_name not in available_functions:
        return types.Content(
                role='tool',
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={'error': f'\033[31mUnknown function: {function_name}\033[0m'},
                        )
                    ],
                )

    actual_function = available_functions[function_name]
    function_result = actual_function(working_directory='./calculator', **function_call_part.args)

    if verbose == True:
        print_slow(f'{func_color}Calling function:\033[0m {function_call_part.name}({function_call_part.args})')
    else:
        print_slow(f'{func_color} - Calling function:\033[0m {function_call_part.name}')

    return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={'result': function_result},
                    )
                ],
            )

# Main code
def main():
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')

    client = genai.Client(api_key=api_key)

    user_prompt, verbose = check_args(argv)

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        ]
    )

    messages = [
            types.Content(role='user', parts=[types.Part(text=user_prompt)])
    ]

    try:
        for i in range(20):
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                tools = [available_functions], 
                system_instruction=system_prompt
                ),
            )
            
            for candidate in response.candidates:
                messages.append(candidate.content)

            if response.function_calls:
                func_result = call_function(response.function_calls[0])
                messages.append(func_result)
            else:
                break

    except Exception as e:
        print_slow(f'\033[31mError: {e}\033[0m')
    
    if verbose:
        print_full_report(user_prompt, response)
    else:
        print_response(response)

if __name__ == '__main__':
    main()
