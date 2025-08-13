from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *

separator = '-' * 20


print(get_files_info('calculator', '.'))
print(separator)
print(get_files_info('calculator', 'pkg'))
print(separator)
print(get_files_info('calculator', '/bin'))
print(separator)
print(get_files_info('calculator', '../'))

'''
print(get_file_content('calculator', 'main.py'))
print(get_file_content('calculator', 'pkg/calculator.py'))
print(get_file_content('calculator', '/bin/cat'))
print(get_file_content('calculator', 'pkg/does_not_exist.py'))
'''
'''
print(write_file('calculator', 'lorem.txt', 'wait, this isn\'t lorem ipsum'))
print(write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet'))
print(write_file('calculator', '/tmp/temp.txt', 'this should not be allowed'))
'''
'''
print(run_python_file('calculator', 'main.py'))
print(run_python_file('calculator', 'main.py', ['3 + 5']))
print(run_python_file('calculator', 'tests.py'))
print(run_python_file('calculator', '../main.py'))
print(run_python_file('calculator', 'nonexistent.py'))
'''
