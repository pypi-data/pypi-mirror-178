import concurrent
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import typer
from ascend.sdk.render import TEMPLATES_V2, download_component, download_data_service, download_dataflow
from ascend_io_cli.support import get_client, print_response
from google.protobuf.json_format import MessageToDict

app = typer.Typer(help='Download local images of data services, dataflows, and components', no_args_is_help=True)


def _configure_write_dir(write_dir: str, data_service: str, unique: bool, purge: bool):
  write_dir = os.path.join(os.path.abspath(write_dir), f'{datetime.now().strftime("%Y%m%d%H%M%S") if unique else ""}')
  if purge and os.path.exists(write_dir):
    shutil.rmtree(write_dir)
  elif os.path.exists(write_dir):
    if data_service:
      shutil.rmtree(os.path.join(write_dir, data_service), ignore_errors=True)
    else:
      for ls_dir in os.listdir(write_dir):
        if ls_dir != '.git':
          shutil.rmtree(os.path.join(write_dir, ls_dir))
  if not os.path.exists(write_dir):
    os.makedirs(write_dir, exist_ok=True)
  return write_dir


@app.command()
def data_service(
    ctx: typer.Context,
    data_service: str = typer.Argument(None, help='Data Service id to download', show_default=False),
    write_dir: str = typer.Option('./ascend', help='Base directory to write to'),
    purge: bool = typer.Option(False, help='Include deleting .git and other data'),
    unique: bool = typer.Option(False, help='Create unique base directory'),
    template_dir: str = typer.Option(TEMPLATES_V2, '--template_dir', show_default=False),
):
  """Download service or all services (default)"""
  client = get_client(ctx)
  write_dir = _configure_write_dir(write_dir, data_service, unique, purge)

  def _download_service(ds):
    download_data_service(client=client, data_service_id=ds.id, resource_base_path=os.path.join(write_dir, ds.id), template_dir=template_dir)
    return ds

  futures = []
  with ThreadPoolExecutor(max_workers=ctx.obj.workers) as executor:
    for svc in client.list_data_services().data:
      if not data_service or (data_service and data_service == svc.id):
        futures.append(executor.submit(_download_service, svc))

  results = []
  for future in concurrent.futures.as_completed(futures):
    result = future.result(10)
    logging.debug(f'downloaded {result.id}')
    results.append(MessageToDict(result))
  print_response(ctx, results)


@app.command()
def dataflow(
    ctx: typer.Context,
    data_service: str = typer.Argument(..., help='Data Service id containing dataflow to download', show_default=False),
    dataflow: str = typer.Argument(..., help='Dataflow id to download', show_default=False),
    write_dir: str = typer.Option('./ascend', help='Base directory to write to'),
    purge: bool = typer.Option(False, help='Include deleting .git and other data'),
    unique: bool = typer.Option(False, help='Create unique base directory'),
    template_dir: str = typer.Option(TEMPLATES_V2, '--template_dir', show_default=False),
):
  """Download a dataflow"""
  client = get_client(ctx)
  write_dir = _configure_write_dir(write_dir, data_service, unique, purge)

  flow_obj = client.get_dataflow(data_service_id=data_service, dataflow_id=dataflow).data
  if flow_obj:
    download_dataflow(client,
                      data_service_id=data_service,
                      dataflow_id=flow_obj.id,
                      resource_base_path=os.path.join(write_dir, data_service, dataflow),
                      template_dir=template_dir)

  print_response(ctx, MessageToDict(flow_obj))


@app.command()
def component(
    ctx: typer.Context,
    data_service: str = typer.Argument(..., help='Data Service id with component to download', show_default=False),
    dataflow: str = typer.Argument(..., help='Dataflow id with component to download', show_default=False),
    component: str = typer.Argument(..., help='Component id to download', show_default=False),
    write_dir: str = typer.Option('./ascend', help='Base directory to write to'),
    purge: bool = typer.Option(False, help='Include deleting .git and other data'),
    unique: bool = typer.Option(False, help='Create unique base directory'),
    template_dir: str = typer.Option(TEMPLATES_V2, '--template_dir', show_default=False),
):
  """Download an individual component"""
  client = get_client(ctx)
  write_dir = _configure_write_dir(write_dir, data_service, unique, purge)

  components = client.list_dataflow_components(data_service_id=data_service, dataflow_id=dataflow).data
  target_component = list(filter(lambda c: c.id == component, components))
  download_component(client,
                     data_service_id=data_service,
                     dataflow_id=dataflow,
                     component_id=component,
                     resource_base_path=os.path.join(write_dir, data_service, dataflow, 'components'),
                     template_dir=template_dir)

  print_response(ctx, MessageToDict(target_component[0] if len(target_component) else {}))
