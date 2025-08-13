import subprocess
import os
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified Python script. If user gives no arguments, run the script without them and without asking.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the script to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the called functions.",
                items=(types.Schema(type=types.Type.STRING)),
                )
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    working_dir_absolute = os.path.abspath(working_directory)
    file_path_absolute = os.path.abspath(os.path.join(working_directory, file_path))
    output_data = []
    args_list = ['python3', file_path_absolute]
    for arg in args:
        args_list.append(arg)

    if not file_path_absolute.startswith(working_dir_absolute):
        return f'\033[31mError: Cannot execute "{file_path}" as it is outside the permitted working directory\033[0m'

    if not os.path.exists(file_path_absolute):
        return f'\033[31mError: File "{file_path}" not found.\033[0m'

    if not file_path_absolute.endswith('.py'):
        return f'\033[31mError: "{file_path}" is not a Python file.\033[0m'

    try:
        completed_process = subprocess.run(args_list, timeout=30, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return f'Error: executing Python file: {e}'

    output_data.append(f'STDOUT: {completed_process.stdout}')
    output_data.append(f'STDERR: {completed_process.stderr}')
    if completed_process.returncode != 0:
        output_data.append(f'Process exited with code {completed_process.returncode}')
    if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
        output_data.append(f'No output produced')

    return '\n'.join(output_data)
