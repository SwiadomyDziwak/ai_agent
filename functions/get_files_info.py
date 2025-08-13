import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    files_info = []
    working_dir_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(working_dir_path)

    if not absolute_path.startswith(os.path.abspath(working_directory)):
        return f'\033[31mError: Cannot list "{directory}" as it is outside the permitted working directory\033[0m'

    if not os.path.isdir(absolute_path):
        return f'\033[33mError: "{directory}" is not a directory\033[0m'

    if len(os.listdir(absolute_path)) == 0:
        return f'\033[33mWarning: {directory} do not contain any files or directories\033[0m'

    for file in os.listdir(absolute_path):
        file_path = os.path.abspath(os.path.join(working_dir_path, file))
        color = '\033[1m'
        if os.path.isdir(file_path):
            color = '\033[94m'
        file_info = f'- {color}{file}: \033[90mfile_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\033[0m'
        files_info.append(file_info)

    return '\n'.join(files_info)
