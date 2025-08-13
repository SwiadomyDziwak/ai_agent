import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes given content to a file. If file exist, overwrite it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text that should be written to a file."
                )
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_absolute = os.path.abspath(working_directory)
    file_path_absolute = os.path.abspath(os.path.join(working_directory, file_path))
    file_directory = os.path.dirname(file_path_absolute)

    if not file_path_absolute.startswith(working_dir_absolute):
        return f'\033[31mError: Cannot write to "{file_path}" as it is outside the permitted working directory\033[0m'

    if not os.path.exists(os.path.join(working_directory, file_directory)):
        os.makedirs(file_directory)

    with open(file_path_absolute, 'w') as file:
        file.write(content)
        
    return f'\033[32mSuccessfully wrote to "{file_path}" ({len(content)} characters written)\033[0m'
