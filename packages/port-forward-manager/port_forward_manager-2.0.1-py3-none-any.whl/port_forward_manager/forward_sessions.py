import subprocess
import random
from rich import inspect, print
from rich.table import Table
from . import tools
from .models import Session


def execute(command):
    # print(command)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # inspect(result)
    # exit(1)
    if result.returncode != 0:
        print(f"Command [b]{command}[/] failed:\n {result.stderr}")
        exit(3)

    return result


def stop(session: Session):
    if session.active:
        print("Stop session {tmux_id}.".format(tmux_id=session.tmux_id))
        stop_command = "tmux kill-session -t '{tmux_id}'".format(tmux_id=session.tmux_id)
        execute(stop_command)


def in_active_sessions(definition, active_sessions):
    for session in active_sessions:
        shared_items = {k: session[k] for k in session if k in definition and session[k] == definition[k]}
        # print(len(shared_items))
        if len(shared_items) >= 7:
            return True

    return False


def generate_new_port(port_list):
    while True:
        port = str(random.randint(9100, 9500))
        if port not in port_list:
            port_list.append(port)
            return port


def start(session, reconnect: bool = False):
    settings = tools.settings()
    if reconnect and session.active:
        # print(f"[b]Stopping '{session_name}'[/b]")
        stop(session)

    if not session.active:
        generate_port = False

        if 'local_port' not in session:
            generate_port = True

        if session.local_port in settings.ports_active:
            print(f"[b]Warning[/b]: Local port {session.local_port} already in use, assigning new port")
            generate_port = True

        if generate_port:
            session.local_port = generate_new_port(settings.ports_active)

        session_data = session.dict()
        print("Start {type} forward on [b]{hostname}[/b] {remote_address}:{remote_port}.".format(**session_data))

        session_data['tmux_id'] = session.tmux_id

        session_data['shell_command'] = 'ping localhost'

        if session_data.get('type') == 'remote':
            ssh = 'ssh -o ExitOnForwardFailure=yes -R {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}'
        else:
            ssh = 'ssh -o ExitOnForwardFailure=yes -L {local_address}:{local_port}:{remote_address}:{remote_port} {hostname}'

        session_data['ssh_command'] = ssh.format(**session_data)

        # start_command = "screen -dmS '{name}' {ssh_command}  -- {shell_command}"
        start_command = "tmux new-session -d -s '{tmux_id}' '{ssh_command} -- {shell_command}'"
        # inspect(session_definition)
        result = execute(start_command.format(**session_data))
        return result
    else:
        print("Ignoring {type} forward on [b]{hostname}[/b] {remote_address}:{remote_port}.".format(**session.dict()))


def update_state():
    settings = tools.settings()

    # Reset state
    settings.ports_active = []
    schema_list = tools.get_schemas_ids()
    for schema_name in schema_list:
        schema = tools.get_schema(schema_name)
        schema.active = False

        for session in schema.sessions:
            session.active = False

    # Update state from tmux sessions
    command = "tmux ls | grep 'pfm_session' | cut -d ':' -f 1"
    result = execute(command)

    session_id_list = result.stdout.split("\n")

    for session_id in session_id_list:
        if len(session_id) == 0:
            continue

        session_data = session_id.replace('_', '.').replace(':', '')
        # print(f"Active -> {session_id}")
        values = session_data.split('|')

        if len(values) == 8:
            filler, schema_id, hostname, remote_host, remote_port, local_address, local_port, forward_type = values

            schema = tools.get_schema(schema_id)
            schema.active = True
            session = schema.get_session(hostname, int(remote_port))
            session.schema_id = schema.id
            session.active = True
            session.local_address = local_address
            session.local_port = local_port
            settings.ports_active.append(local_port)


def filter_session(session: Session, schema: str = None, host: str = None, port: str = None):
    if schema and schema not in session.schema_id:
        return True
    if host and host not in session.hostname:
        return True
    if port and port != session.remote_port:
        return True


def list_from_active(key, filter_string: str = ''):
    items = []

    schema_list = tools.get_schemas_ids()
    for schema_name in schema_list:
        schema = tools.get_schema(schema_name)

        for session in schema.sessions:
            if not session.active:
                continue

            item = session.dict().get(key)
            if filter_string not in item:
                continue
            if item not in items:
                items.append(item)

    return items


def prepare_table(show_alias: bool = False, show_link: bool = False, show_schema: bool = True, title: str = 'Schemas'):
    settings = tools.settings()
    table = Table(show_edge=settings.show_table_border)

    if show_schema:
        table.add_column("Schema", style="green", width=20)

    table.add_column("Hostname", justify="left", style="yellow", width=30)
    table.add_column("Type", justify="right", style="yellow", width=8)
    table.add_column("Local host", justify="right", style="white", width=15)
    table.add_column("Local port", justify="right", style="white", width=7)
    table.add_column("Remote host", justify="right", style="yellow", width=15)
    table.add_column("Remote port", justify="right", style="yellow", width=7)

    if show_alias:
        table.add_column("Alias", justify="left", style="cyan", width=25)

    if show_link:
        table.add_column("URL", style="cyan", width=60)

    return table


def show_active_sessions(schema: str = None, host: str = None, port: int = None):
    update_state()

    schema_list = tools.get_schemas_ids()
    settings = tools.settings()
    table = prepare_table(True, True, True)
    session_count = 0
    for schema_name in schema_list:
        schema = tools.get_schema(schema_name)

        schema_rows = False
        for session in schema.sessions:
            if not session.active:
                continue

            schema_rows = True

            row = [
                schema_name,
                session.hostname,
                session.type,
                session.local_address,
                'auto' if session.local_port == 0 else session.local_port.__str__(),
                session.remote_address,
                session.remote_port.__str__(),
                session.alias,
                session.url
            ]
            table.add_row(*row)
            session_count += 1
        if schema_rows:
            table.rows[table.row_count - 1].end_section = True

    if session_count > 0:
        print(table)
    else:
        print("Nothing to see here")


def get_session_definition(session):
    schema = tools.get_schema(session.get('schema'))
    for session_definition in schema:
        if session_definition.get('hostname') != session.get('hostname'):
            continue
        if session_definition.get('remote_port') != session.get('remote_port'):
            continue

        return session_definition

