import subprocess
import os
import json
import string
import uuid
import re
import time
import platform


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value


def get_appsettings(root_dir):
    appsettings = {}
    if os.path.exists(os.path.join(root_dir, 'appsettings.json')):
        appsettings = json.load(open(os.path.join(root_dir, 'appsettings.json')))
    if os.path.exists(os.path.join(root_dir, 'appsettings.Development.json')):
        merge(json.load(open(os.path.join(root_dir, 'appsettings.Development.json'))), appsettings)
    return appsettings


def get_connection_string_parts(connection_string):
    _ = {}
    args = []
    for part in str(connection_string).split(';'):
        kv = part.split('=')
        if len(kv) == 2:
            _[kv[0]] = kv[1]
        elif len(kv):
            args.append(part)
    _['args'] = args
    return _


def find_dotnet_sdk(version):
    root = 'dotnet'
    try:
        check_system_command_is_found([root, '--list-sdks'], version, 'dotnet' + version + ' not found in path')
    except ModuleNotFoundError:
        root = os.path.join(os.environ.get('DOTNET'), root)
        check_system_command_is_found([root, '--list-sdks'], version, 'dotnet' + version +
                                      ' not found in pyenv $DOTNET')
    return root


def create_database_script_postgresql(db_name):
    sql_template = string.Template("SELECT 'CREATE DATABASE \"$db_name\"'" +
                                   "WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$db_name')\\gexec")
    return sql_template.substitute(db_name=db_name)

def run_command(args):
    shell = ' '.join(find_system_shell())
    return subprocess.call(f"{shell} '{' '.join(args)}'", shell=True)


def check_system_command_is_found(args, expected_response_contains, error_message, regex=False, log_error=True,
                                  log_found=True):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    found = False
    for c in proc.communicate():
        if found is False:
            try:
                if regex is True:
                    found = re.search(expected_response_contains, str(c).removeprefix(str(b''))) is not None
                else:
                    str(c).removeprefix(str(b'')).index(expected_response_contains)
                    found = True
            except ValueError:
                found = False
    if found is False:
        if log_error is True:
            print(error_message)
        raise ModuleNotFoundError(error_message)
    if log_found is True:
        print('Found ' + args[0])


def find_system_shell():
    operating_system = platform.uname().system
    _ = []
    try:
        operating_system.lower().index('windows')
        raise NotImplementedError
    except ValueError:
        try:
            operating_system.lower().index('darwin')
            _.extend(['/bin/zsh', '-i', '-c'])
        except ValueError:
            raise NotImplementedError
    return _


def check_system_command_is_found_in_shell(args, expected_response_contains, error_message, regex=False):
    check_system_command_is_found(get_system_shell_command(args), expected_response_contains,
                                  error_message, regex, log_error=True, log_found=False)


def get_system_shell_command(args):
    _ = find_system_shell()
    s = ' '.join(args)
    _.append(s)
    return _


def run_system_command(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return str(proc.communicate()[0])


def run_system_shell_command(args):
    proc = subprocess.Popen(get_system_shell_command(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return str(proc.communicate()[0]).removeprefix('b\'').removesuffix('\'')


def psql_installed():
    check_system_command_is_found(['psql', '--version'], 'PostgreSQL', 'psql not found in PATH')


def execute_psql_command(connection_string_parts, sql):
    script = str(uuid.uuid4()) + '.sql'
    _template = string.Template('psql "user=$user ' +
                                'password=$password ' +
                                'host=$host" -f ' + script)

    try:
        with open(script, 'w') as psqlScript:
            psqlScript.write(sql)
        os.system(_template.substitute(user=connection_string_parts["User Id"],
                                       password=connection_string_parts["Password"],
                                       host=connection_string_parts["Server"]))
    finally:
        if os.path.exists(script):
            os.remove(script)


def docker_installed():
    check_system_command_is_found(['docker', '--version'], 'Docker version', 'Docker not found in PATH')


def docker_ensure_container_running(container_name, run_command):
    response = run_system_command(['docker', 'ps'])
    try:
        response.index(container_name)
        print("Docker: " + container_name + " running")
    except ValueError:
        try:
            response = run_system_command(['docker', 'ps', '-a'])
            response.index(container_name)
            os.system('docker start ' + container_name)
            print("Docker: " + container_name + " started, sleeping 10 seconds")
            time.sleep(10)
        except ValueError:
            os.system('docker run ' + '--name ' + container_name + ' ' + run_command)


def sqlpackage_installed():
    check_system_command_is_found(['sqlpackage', '/version:True'], '([0,9]+|.{1})+', 'SqlPackage not found in PATH',
                                  True)


def nvm_installed(version):
    check_system_command_is_found_in_shell(['nvm', '--version'], '([0,9]+|.{1})+', 'No shell command found for nvm',
                                           True)
    nvm_use(version)


def using_nvm_execute(version, args):
    response = run_system_shell_command(['nvm', 'ls', str(version)])
    try:
        response.index(f"v{str(version)}")
    except ValueError:
        run_command(['nvm', 'install', str(version)])
    return run_command(['nvm', 'exec', str(version), ' '.join(args)])


def using_nvm_run(version, args):
    return run_system_shell_command(['nvm', 'exec', str(version), ' '.join(args)])


def npm_aurelia_cli_installed(version):
    response = using_nvm_run(version, ['npm', 'list', '-g', '--depth', '0', '|', 'grep', 'aurelia-cli'])
    response.index('aurelia-cli')

