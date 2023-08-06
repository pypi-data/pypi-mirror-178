#!/usr/bin/env python3

import typer
from ascend.sdk.applier import DataflowApplier, DataServiceApplier, ConnectionApplier, CredentialApplier, ComponentApplier

from ascend_io_cli.commands.clone import _hydrate_dataflow, _hydrate_data_service, _hydrate_credential, _hydrate_connection, _hydrate_component
from ascend_io_cli.support import get_client

app = typer.Typer(name='apply', help='Apply local changes to remote data service, dataflow, or component', no_args_is_help=True)


@app.command(name='credential', help='Apply local changes to a credential')
def apply_credential(
    ctx: typer.Context,
    data_service: str = typer.Argument(None, help='Data Service id with changes', show_default=False),
    name: str = typer.Argument(..., help="Name for credential", show_default=False),
    credential_type: str = typer.Argument(..., help="Credential type: e.g ascend.mysql, mysql.custom.python...", show_default=False),
    details: str = typer.Argument(..., help="Location for credential", show_default=False),
):
  client = get_client(ctx)

  creds = _hydrate_credential(credential_id=name, credential_type=credential_type, credential_details=details)
  CredentialApplier(client).apply(data_service, creds)


@app.command(name='connection', help='Apply local changes to a connection')
def apply_connection(
    ctx: typer.Context,
    data_service: str = typer.Argument(None, help='Data Service id with changes', show_default=False),
    credential: str = typer.Argument(None, help='credential id associated with connection', show_default=False),
    name: str = typer.Argument(..., help="Name for connection", show_default=False),
    connection_type: str = typer.Argument(..., help="Credential type: e.g ascend.mysql, mysql.custom.python...", show_default=False),
    details: str = typer.Argument(..., help="Location for credential", show_default=False),
):
  client = get_client(ctx)

  conn = _hydrate_connection(connection_id=name, connection_type=connection_type, connection_details=details, credential_id=credential)
  ConnectionApplier(client).apply(data_service, conn)


@app.command(name='component', help='Apply local changes to a component (read, write, or transform)')
def apply_component(
    ctx: typer.Context,
    data_service: str = typer.Argument(..., help='Data Service id with component changes', show_default=False),
    dataflow: str = typer.Argument(..., help='Dataflow id with component changes', show_default=False),
    component_id: str = typer.Argument(..., help='Component id to update', show_default=False),
    base_dir: str = typer.Option('./ascend', help='Base directory for the data service containing the component'),
):
  client = get_client(ctx)

  component = _hydrate_component(data_service_id=data_service, dataflow_id=dataflow, component_id=component_id, base_dir=base_dir)
  ComponentApplier(client, {}).apply(data_service, dataflow, component)


@app.command(name='dataflow', help='Apply local changes to a dataflow')
def apply_dataflow(
    ctx: typer.Context,
    data_service: str = typer.Argument(..., help='Data Service id containing dataflow to apply', show_default=False),
    dataflow: str = typer.Argument(..., help='Dataflow id to apply', show_default=False),
    base_dir: str = typer.Option('./ascend', help='Base directory containing the dataflow'),
):
  client = get_client(ctx)

  flow = _hydrate_dataflow(data_service_id=data_service, dataflow_id=dataflow, new_dataflow_id=dataflow, base_dir=base_dir)
  DataflowApplier(client).apply(data_service_id=data_service, dataflow=flow)


@app.command(name='data-service', help='Apply local changes to a data service')
def apply_data_service(
    ctx: typer.Context,
    data_service: str = typer.Argument(..., help='Data Service id with changes to apply', show_default=False),
    base_dir: str = typer.Option('./ascend', help='Base directory containing the flow'),
):
  client = get_client(ctx)

  data_service = _hydrate_data_service(data_service_id=data_service, new_data_service_id=data_service, base_dir=base_dir)
  DataServiceApplier(client).apply(data_service=data_service)


if __name__ == "__main__":
  app()
