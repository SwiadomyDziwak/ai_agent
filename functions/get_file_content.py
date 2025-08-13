import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file, constrained to the working directory. if the file contain more then 10000 characters it gets trunctuated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to list content from, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    file_path_absolute = os.path.abspath(os.path.join(working_directory, file_path))
    working_dir_absolute = os.path.abspath(working_directory)

    max_length = 10000

    if not file_path_absolute.startswith(working_dir_absolute):
        return f'\033[31mError: Cannot read "{file_path}" as it is outside the permitted working directory\033[0m'

    if not os.path.isfile(file_path_absolute):
        return f'\033[31mError: File not found or is not a regular file: "{file_path}"\033[0m'

    with open(file_path_absolute, 'r') as file:
        file_content = file.read()

    if len(file_content) > max_length:
        file_content = file_content[:max_length] + f'\n\033[33m[...File "{file_path}" truncated at 10000 characters]\033[0m'

    return file_content
