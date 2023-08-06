import pkg_resources
import random
import simplejson
import rich
import typer
import time

from .forward_sessions import prepare_table, show_active_sessions, in_active_sessions, update_state
from .cli_autocomplete import ac_schemas, ac_hosts
from .cli_autocomplete import sc_schemas, sc_hosts, ac_active_schemas, sc_active_remote_port, sc_active_hosts
from . import tools, forward_sessions
from .models import Session


app = typer.Typer(no_args_is_help=True)
tools.load_settings()


@app.command()
def schemas(schema_filter: str = typer.Argument(None, autocompletion=ac_schemas),
            json: bool = typer.Option(False, '--json', '-j', help="Output JSON")):
    """
    List configured schemas
    """
    settings = tools.settings()
    table = prepare_table(True, settings.show_schema_link, True)

    schema_list = tools.get_schemas_ids()
    for schema_name in schema_list:
        if schema_filter and schema_filter not in schema_name:
            continue

        schema = tools.get_schema(schema_name)

        for forward_definition in schema.sessions:
            row = [
                schema_name,
                forward_definition.hostname,
                forward_definition.type,
                forward_definition.local_address,
                'auto' if forward_definition.local_port == 0 else forward_definition.local_port.__str__(),
                forward_definition.remote_address,
                forward_definition.remote_port.__str__(),
                forward_definition.alias
            ]
            table.add_row(*row)

        table.rows[table.row_count - 1].end_section = True

    rich.print(table)


@app.command()
def start(schema_id: str = typer.Argument(..., autocompletion=ac_schemas),
          force: bool = typer.Option(None, help="Force sessions reconnection")):
    """
    Start a schema of forwarding sessions
    """
    settings = tools.settings()
    forward_sessions.update_state()

    schema = tools.get_schema(schema_id)
    active_ports = tools.get_ports_active()

    if schema is None:
        print("[b]Schema '{0}' is unknown[/b]".format(schema_id))
        exit(-1)

    for session in schema.sessions:
        session.schema_id = schema.id
        forward_sessions.start(session, force)

    time.sleep(settings.wait_after_start)
    show_active_sessions()


@app.command()
def stop(schema_id: str = typer.Argument(None, autocompletion=ac_active_schemas),
         hostname: str = typer.Option(None, shell_complete=sc_active_hosts),
         port: str = typer.Option(None, shell_complete=sc_active_remote_port)):
    """
    Stop sessions from active schema, host or port
    """

    if not schema_id and not hostname and not port:
        print("[b]Pick a schema, host or host and port or --all[/b]")
        exit(-1)

    settings = tools.settings()
    forward_sessions.update_state()

    if schema_id:
        schema = tools.get_schema(schema_id)
        for session in schema.sessions:
            if forward_sessions.filter_session(session, schema_id, hostname, port):
                print(f"Ignoring session {session.tmux_id}")
                continue

            # inspect(session)

            # print(f"Stop session {session.tmux_id}")
            forward_sessions.stop(session)

    time.sleep(settings.wait_after_stop)
    show_active_sessions()


@app.command()
def shutdown():
    """
    Stop all active sessions
    """

    settings = tools.settings()

    forward_sessions.update_state()
    schema_list = tools.get_schemas_ids()
    for schema_name in schema_list:
        schema = tools.get_schema(schema_name)
        for session in schema.sessions:
            if session.active:
                forward_sessions.stop(session)

    time.sleep(settings.wait_after_stop)

    show_active_sessions()


@app.command()
def forward(hostname: str = typer.Argument(..., autocompletion=ac_hosts),
            remote_port: int = typer.Argument(...),
            local_port: int = None,
            remote_address: str = '127.0.0.1',
            local_address: str = '127.0.0.1',
            remote: bool = False,
            schema: str = typer.Option('user-cli', shell_complete=ac_schemas)):
    """
    Start a forwarding session
    """

    settings = tools.settings()

    session_data = {
        'schema_id': 'manual-forward',
        'hostname': hostname,
        'local_port': local_port or remote_port,
        'local_address': local_address,
        'remote_port': remote_port,
        'remote_address': remote_address,
        'type': 'remote' if remote else 'local'
    }

    session = Session(**session_data)

    forward_sessions.start(session)
    time.sleep(settings.wait_after_start)

    show_active_sessions()


@app.command()
def status(schema: str = typer.Option(None, shell_complete=sc_schemas),
           host: str = typer.Option(None, shell_complete=sc_hosts),
           port: int = None,
           json: bool = typer.Option(False, '--json', '-j', help="Output JSON")):
    """
    Show active sessions
    """

    if json:
        sessions = forward_sessions.update_state()
        print(simplejson.dumps(sessions))
    else:
        show_active_sessions(schema, host, port)


@app.command()
def state():
    """
    Show active sessions
    """
    forward_sessions.update_state()
    print(tools.settings().json())


@app.command()
def version():
    """
    Show active sessions
    """

    current_version = pkg_resources.get_distribution("port-forward-manager").version
    print(f"Port Forward Manager [bold white]v{current_version}[/]")


def run():
    app()


if __name__ == "__main__":
    app()
