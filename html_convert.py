import re
import os
import sys

def str_to_c_str(s):
    #s='a\nb\\n1\\\n'
    #print(s)
    #print(str(s))
    # s = re.sub(r'\/\/(.*?)[\r\n]', r'/* \1 */ ', s) # handle js single line comments
    
    # s = s.replace('\r', ' ') # convert to single line
    # s = s.replace('\n', ' ') # convert to single line
    
    # while '  ' in s: # replace double with single spaces (left because of indentation)
    #     s = s.replace('  ', ' ')
    
    # c string escapes
    s = s.replace('\\', r'\\') # must be first
    s = s.replace('\a', r'\a')
    s = s.replace('\b', r'\b')
    s = s.replace('\e', r'\e')
    s = s.replace('\f', r'\f')
    s = s.replace('\n', r'\n')
    s = s.replace('\r', r'\r')
    s = s.replace('\t', r'\t')
    s = s.replace('\v', r'\v')
    s = s.replace("\'", r"\'")
    s = s.replace('\"', r'\"')
    s = s.replace('\?', r'\?')
    
    s = s.replace('\n', '\\n')
    #print('-' * 8)
    #print(str(s))
    #print('-' * 4)
    return s

def detect_type(filename):
    try:
        extension = filename.split('.')[1]
    except:
        extension = None
        
    if extension == None:
        return 'text/html'
    if extension == 'html':
        return 'text/html'
    if extension == 'txt':
        return 'text/plain'
    if extension == 'js':
        return 'text/javascript'
    if extension == 'css':
        return 'text/css'
    if extension == 'rcpp':
        return 'rcpp'
    
    return 'text/plain'

def create_lambda_handler_str(url, method, f_type, f_contents):
    out = ''
    
    if method == 'GET':
        method == 'HTTP_GET'
    if method == 'POST':
        method == 'HTTP_POST'
    
    out +=  f'''    server->on("{url}", {method}, [](AsyncWebServerRequest *request){{
    
        request->send(200, "{f_type}", "{str_to_c_str(f_contents)}");
    }});'''
    
    return out

def create_fn_handler_str(fn_name, f_type, f_contents):
    out = ''
    
    out +=  f'''void {fn_name}(AsyncWebServerRequest *request){{

    request->send(200, "{f_type}", "{str_to_c_str(f_contents)}");
}}'''
    
    return out


# -stdout - write to stdout
# -f - one file only
# -c - show only c string - only works with -f
def fukit():
    print('Usage:')
    print(f'python3 {dict_args[0]} /html/dir [-o html_files.h] [-special_index] [-stdout]')
    print(f'python3 {dict_args[0]} -f file [-o html_files.h] [-special_index] [-stdout]')
    print(f'python3 {dict_args[0]} -f file [-special_index] [-c] # only c string')
    exit(1)

def clean_exit():
    if '-stdout' in dict_args:
        pass
    else:    
        output.close()
    exit(0)


import pydictarg
dict_args = pydictarg.args_to_dict(sys.argv)

working_dir = os.getcwd()
if '-o' in dict_args:
    output_file = os.path.join(working_dir, dict_args['-o'])
else:    
    output_file = os.path.join(working_dir, 'html_files.h')
    
files_path = ''
files = []
try:
    if '-f' in dict_args:
        files_path = working_dir
        files = [dict_args['-f']]
    else:
        files_path = os.path.join(working_dir, dict_args[1])
        files = [f for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, f))]
except:
    fukit()

if files_path == '':
    fukit()

special_index = '-special_index' in dict_args

if '-c' in dict_args:
    if '-f' in dict_args:
        with open(os.path.join(files_path, files[0]), 'r') as f:
            print(f'"{str_to_c_str(f.read())}"')
            #print(str_to_c_str(f.read()))
            #print('\\\\' in str_to_c_str(f.read()))
        exit(0)
    else:
        fukit()

if '-stdout' in dict_args:
    output = sys.stdout
else:    
    output = open(output_file, "w")

    
print('', file=output)

if special_index:
    for file_name in files:
        if 'index' in file_name:
            file_path = os.path.join(files_path, file_name)
            with open(file_path, 'r') as f:
                print(
                    create_fn_handler_str('handle_index', detect_type(file_name), f.read()),
                    file=output
                )

# Open the function that needs to be included from the main code
print('void html_files(AsyncWebServer* server) {', file=output)

# Create a handler for every file
for file_name in files:
    file_path = os.path.join(files_path, file_name)
    with open(file_path, 'r') as f:
        if 'index' in file_name and special_index:
            pass
        else:
            print(
                create_lambda_handler_str(f'/{file_name}', 'HTTP_GET', detect_type(file_name), f.read()),
                file=output
            )

# Close the incude function
print('}', file=output)


clean_exit()
