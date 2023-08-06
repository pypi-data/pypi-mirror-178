import argparse
import getopt
import logging
import os
import pathlib
import sys
import signal
from logging.handlers import RotatingFileHandler
from os.path import expanduser

from c8yrc.rest_client.c8yclient import CumulocityClient
from c8yrc.tcp_socket.tcp_server import TCPServer
from c8yrc.websocket_client.ws_client import WebsocketClient

PIDFILE = '/var/run/c8yrc/c8yrc'


class ExitCommand(Exception):
    pass


def signal_handler(signal, frame):
    raise ExitCommand()


def prepare_c8y_proxy(host, device, extype, config_name, tenant, user, password,
                      token, port, tfacode, use_pid, kill_instances, ignore_ssl_validate, reconnects,
                      tcp_size, tcp_timeout, script_mode, event=None):
    validate_parameter(host, device, extype, config_name,
                       tenant, user, password, token)
    if use_pid:
        upsert_pid_file(device, host, config_name, user)
    if kill_instances:
        if use_pid:
            kill_existing_instances()
        else:
            logging.warning(f'WARNING: Killing existing instances is only support when "--use-pid" is used.')
    client = CumulocityClient(host, tenant, user, password, tfacode, ignore_ssl_validate)
    tenant_id_valid = client.validate_tenant_id()
    if tenant_id_valid is not None:
        logging.warning(f'WARNING: Tenant ID {tenant} does not exist. Try using this Tenant ID {tenant_id_valid} next time!')
    session = None
    if token:
        client.validate_token()
    else:
        session = client.retrieve_token()
    mor = client.read_mo(device, extype)
    config_id = client.get_config_id(mor, config_name)
    device_id = client.get_device_id(mor)

    is_authorized = client.validate_remote_access_role()
    if not is_authorized:
        logging.error(f'User {user} is not authorized to use Cloud Remote Access. Contact your Cumulocity Admin!')
        return None
    websocket_client = WebsocketClient(
        host, tenant, user, password, config_id, device_id, session, token, ignore_ssl_validate, reconnects)
    wst = websocket_client.connect()
    tcp_server = TCPServer(port, websocket_client, tcp_size, tcp_timeout, wst, script_mode, event)
    websocket_client.tcp_server = tcp_server
    return tcp_server


def verbose_log():
    logging.info(f'Verbose logging activated.')
    logging.getLogger().setLevel(logging.DEBUG)
    for handler in logging.getLogger().handlers:
        handler.setLevel(logging.DEBUG)


def upsert_pid_file(device, url, config, user):
    try:
        clean_pid_file(None)
        pid_file_text = get_pid_file_text(device, url, config, user)
        logging.debug(f'Adding {pid_file_text} to PID-File {PIDFILE}')
        if not os.path.exists(PIDFILE):
            if not os.path.exists(os.path.dirname(PIDFILE)):
                os.makedirs(os.path.dirname(PIDFILE))
            file = open(PIDFILE, 'w')
            file.seek(0)
        else:
            file = open(PIDFILE, 'a+')
            file.seek(0)
        file.write(pid_file_text)
        file.write('\n')
    except PermissionError:
        logging.error(
            f'Could not write PID-File {PIDFILE}. Please create the folder manually and assign the correct permissions.')
        sys.exit(1)


def get_pid_file_text(device, url, config, user):
    pid = str(os.getpid())
    return f'{pid},{url},{device},{config},{user}'


def get_pid_from_line(line):
    return int(str.split(line, ',')[0])


def pid_is_active(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def clean_pid_file(pid):
    if os.path.exists(PIDFILE):
        logging.debug(f'Cleaning Up PID {pid} in PID-File {PIDFILE}')
        pid = pid if pid is not None else os.getpid()
        with open(PIDFILE, "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if get_pid_from_line(line) != pid:
                    file.write(line)
            file.truncate()
            if os.path.getsize(PIDFILE) == 0:
                os.remove(PIDFILE)


def kill_existing_instances():
    if os.path.exists(PIDFILE):
        file = open(PIDFILE)
        pid = int(os.getpid())
        #logging.info(f'Current PID {pid}')
        for line in file:
            other_pid = get_pid_from_line(line)
            if pid != other_pid and pid_is_active(other_pid):
                logging.info(
                    f'Killing other running Process with PID {other_pid}')
                os.kill(get_pid_from_line(line), 9)
            clean_pid_file(other_pid)


def validate_parameter(host, device, extpye, config_name, tenant, user, password, token):
    if not host:
        logging.error(f'Hostname is missing!')
        print('Mandatory parameter -h, --hostname is missing')
        print(_help_message())
        sys.exit(1)

    if not device:
        logging.error(f'Device Name is missing!')
        print('Mandatory parameter -d, --device is missing')
        print(_help_message())
        sys.exit(1)

    if not config_name:
        logging.error(f'Configuration Name is missing!')
        print('Mandatory parameter -c, --config is missing')
        print(_help_message())
        sys.exit(1)

    if not tenant and not token:
        logging.error(f'Tenant is missing!')
        print('Mandatory parameter -t, --tenant is missing')
        print(_help_message())
        sys.exit(1)

    if not user and not token:
        logging.error(f'User is missing!')
        print('Mandatory parameter -u, --user is missing')
        print(_help_message())
        sys.exit(1)

    if not password and not token:
        logging.error(f'Password is missing!')
        print('Mandatory parameter -p, --password is missing')
        print(_help_message())
        sys.exit(1)


def _help_message() -> str:
    return str('Usage: c8yrc [params]\n'
               '\n'
               'Parameter:\n'
               ' --help                 show this help message and exit\n'
               ' -h, --hostname         REQUIRED, the Cumulocity Hostname\n'
               ' -d, --device           REQUIRED, the Device Name (ext. Id of Cumulocity)\n'
               ' --extype               OPTIONAL, the external Id Type. Default: "c8y_Serial"\n'
               ' -c, --config           OPTIONAL, the name of the C8Y Remote Access Configuration. Default: "Passthrough"\n'
               ' -t, --tenant           REQUIRED, the tenant Id of Cumulocity\n'
               ' -u, --user             REQUIRED, the username of Cumulocity\n'
               ' -p, --password         REQUIRED, the password of Cumulocity\n'
               ' --tfacode              OPTIONAL, the TFA Code when an user with the Option "TFA enabled" is used\n'
               ' --port                 OPTIONAL, the TCP Port which should be opened. Default: 2222\n'
               ' -k, --kill             OPTIONAL, kills all existing processes of c8yrc\n'
               ' --tcpsize              OPTIONAL, the TCP Package Size. Default: 32768\n'
               ' --tcptimeout           OPTIONAL, Timeout in sec. for inactivity. Can be activited with values > 0. Default: Deactivated\n'
               ' -v, --verbose          OPTIONAL, Print Debug Information into the Logs and Console when set.\n'
               ' -s, --scriptmode       OPTIONAL, Stops the TCP Server after first connection. No automatical restart!\n'
               ' --ignore-ssl-validate  OPTIONAL, Ignore Validation for SSL Certificates while connecting to Websocket'
               ' --use-pid              OPTIONAL, Will create a PID-File in /var/run/c8yrc to store all Processes currently running.\n'
               ' --reconnects           OPTIONAL, The number of reconnects to the Cloud Remote Service. 0 for infinite reconnects. Default: 5'
               '\n')


def start_c8y_proxy(tcp_server, use_pid):
    try:
        tcp_server.start()
    except Exception as ex:
        logging.error(f'Error on TCP-Server {ex}')
    finally:
        if use_pid:
            clean_pid_file(None)
        tcp_server.stop()


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected, got {}'.format(v))


def start():
    signal.signal(signal.SIGUSR1, signal_handler)
    home = expanduser('~')
    path = pathlib.Path(home + '/.c8yrc')
    loglevel = logging.INFO
    path.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(loglevel)
    log_file_formatter = logging.Formatter(
        '%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s')
    log_console_formatter = logging.Formatter('%(message)s')

    # Set default log format
    if len(logger.handlers) == 0:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_console_formatter)
        console_handler.setLevel(loglevel)
        logger.addHandler(console_handler)
    else:
        handler = logger.handlers[0]
        handler.setFormatter(log_console_formatter)

    # Max 5 log files each 10 MB.
    rotate_handler = RotatingFileHandler(filename=path / 'c8yclient.log', maxBytes=10000000,
                                         backupCount=5)
    rotate_handler.setFormatter(log_file_formatter)
    rotate_handler.setLevel(loglevel)
    # Log to Rotating File
    logger.addHandler(rotate_handler)
    parser = argparse.ArgumentParser(prog='main.py')
    subparsers = parser.add_subparsers()
    subparsers.required = True
    subparsers.dest = 'command'
    # Proxy command
    subparser = subparsers.add_parser("PROXY", help="Start C8Y Proxy")
    subparser.add_argument('-h', '--hostname', required=True, help="the Cumulocity Hostname")
    subparser.add_argument('-d', '--device', required=True, help='the Device Name (ext. Id of Cumulocity))')
    subparser.add_argument('--extype', default='c8y_Serial', help='the external Id Type. Default: "c8y_Serial"')
    subparser.add_argument('-c', '--config', default='Passthrough',
                           help='the name of the C8Y Remote Access Configuration. Default: "Passthrough"')
    subparser.add_argument('-t', '--tenant', help='the tenant Id of Cumulocity')
    subparser.add_argument('-u', '--username', help='the username of Cumulocity')
    subparser.add_argument('-p', '--password', help='the password of Cumulocity')
    subparser.add_argument('--tfacode', help='the TFA Code when an user with the Option "TFA enabled" is used')
    subparser.add_argument('--port', nargs='?', const=2222, type=int,
                           help='the TCP Port which should be opened. Default: 2222')
    subparser.add_argument('-k', '--kill', type=str2bool, action='store',
                            default='True', nargs='?', help='kills all existing processes of c8yrc]:')
    subparser.add_argument('--tcpsize', nargs='?', const=32768, type=int, help='the TCP Package Size. Default: 32768')
    subparser.add_argument('--tcptimeout', nargs='?', const=0, type=int,
                           help='Timeout in sec. for inactivity. Can be activited with values > 0. Default: Deactivated')
    subparser.add_argument('-v', '--verbose', type=str2bool, action='store',
                           default='False', nargs='?',
                           help='Print Debug Information into the Logs and Console when set.')
    subparser.add_argument('-s', '--scriptmode', type=str2bool, action='store',
                           default='True', nargs='?',
                           help='Stops the TCP Server after first connection. No automatical restart!')
    subparser.add_argument('--ignore-ssl-validate', type=str2bool, action='store',
                           default='True', nargs='?',
                           help='Ignore Validation for SSL Certificates while connecting to Websocket')
    subparser.add_argument('--use-pid', type=str2bool, action='store',
                           default='True', nargs='?',
                           help='Will create a PID-File in /var/run/c8yrc to store all Processes currently running.')
    subparser.add_argument('--reconnects', type=int,
                    help='The number of reconnects to the Cloud Remote Service. 0 for infinite reconnects. Default: 5')

    # REST Command
    subparser = subparsers.add_parser("UPLOAD_IMAGE", help="Upload Image to Cumulocity")
    subparser.add_argument('-h', '--hostname', required=True, help="the Cumulocity Hostname")
    subparser.add_argument('-t', '--tenant', help='the tenant Id of Cumulocity')
    subparser.add_argument('-u', '--username', help='the username of Cumulocity')
    subparser.add_argument('-p', '--password', help='the password of Cumulocity')
    subparser.add_argument('--tfacode', help='the TFA Code when an user with the Option "TFA enabled" is used')
    subparser.add_argument('--ignore-ssl-validate', type=str2bool, action='store',
                           default='True', nargs='?',
                           help='Ignore Validation for SSL Certificates while connecting to Websocket')

    args = parser.parse_args()

    if args.command == '"PROXY':

        if args.verbose:
            verbose_log()

        s = prepare_c8y_proxy(args.host, args.device, args.extype, args.config, args.tenant, args.username,
                              args.password, args.token, args.port, args.tfacode, args.use-pid, args.kill,
                              args.ignore_ssl_validate, args.reconnects, args.tcpsize, args.tcptimeout, args.scriptmode)
        start_c8y_proxy(s, args.use-pid)
        sys.exit(0)


if __name__ == '__main__':
    start()

