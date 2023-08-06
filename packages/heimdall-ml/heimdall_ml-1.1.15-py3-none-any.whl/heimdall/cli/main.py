import click
from heimdall import Heimdall


@click.group()
@click.pass_context
@click.option(
    "-c",
    "--config",
    type=str,
    required=False,
    default="heimdall_config.yml",
    show_default=True,
    help="Name of the config file",
)
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj["CONFIG"] = config


@cli.command("run")
@click.pass_context
def run(ctx):
    config = ctx.obj["CONFIG"]
    Heimdall(config).run()


if __name__ == "__main__":
    cli()
