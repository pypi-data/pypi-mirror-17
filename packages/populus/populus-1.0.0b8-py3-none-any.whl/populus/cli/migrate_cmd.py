import click

from populus.utils.cli import (
    select_chain,
    show_chain_sync_progress,
    get_unlocked_deploy_from_address,
)
from populus.migrations.migration import (
    get_migration_classes_for_execution,
)
from populus.migrations.validation import (
    validate_migration_classes,
)

from .main import main


@main.command('migrate')
@click.argument('chain_name', nargs=1, required=False)
@click.pass_context
def migrate(ctx, chain_name):
    """
    Run project migrations
    """
    project = ctx.obj['PROJECT']

    if not project.migrations:
        raise click.Abort((
            "The project does not appear to have any migrations.  You can use "
            "the `populus makemigration command to generate project migrations"
        ))

    # Validate the project migrations
    validate_migration_classes(project.migrations)

    # Determine which chain should be used.
    if not chain_name:
        chain_name = select_chain(project)

    chain_config = project.config.chains[chain_name]

    # Determine if the chain is *migratable*
    if 'registrar' not in chain_config:
        # TODO: this should be a property of the chain object itself.
        # Something like `chain.is_ready_for_migrations`.
        if chain_name not in {'testrpc', 'temp'}:
            # ignore `testrpc` and `temp` because they lazily create their
            # registrar contracts.
            # TODO: We can present the use with the option to just initialize
            # the chain right here rather than throwing an error.
            raise click.Abort((
                "The chain {0!r} is not ready for migrations.  Please initialize this "
                "chain with the `populus migrate init` command".format(chain_name)
            ))

    with project.get_chain(chain_name) as chain:
        if chain_name in {'mainnet', 'morden'}:
            show_chain_sync_progress(chain)

        account = get_unlocked_deploy_from_address(chain)
        chain.web3.eth.defaultAccount = account

        # Wait for chain sync if this is a public network.
        if chain_name in {'mainnet', 'morden'}:
            show_chain_sync_progress(chain)

        # Determine if we have any migrations to run.
        migrations_to_execute = get_migration_classes_for_execution(
            project.migrations,
            chain,
        )

        if not migrations_to_execute:
            raise click.Abort(("All migrations have been run."))

        click.echo("Migration operations to perform:")

        for migration in migrations_to_execute:
            click.echo(''.join((
                "  ",
                migration.migration_id,
                " ({0} operations)".format(len(migration.operations)),
                ":",
            )))
            for operation_index, operation in enumerate(migration.operations):
                click.echo(''.join((
                    "    ",
                    str(operation_index),
                    " - ",
                    str(operation),
                )))

        click.echo("Executing migrations:")
        for migration in migrations_to_execute:
            click.echo(''.join((
                "  ",
                migration.migration_id,
                "... ",
            )), nl=False)
            migration.execute()
            click.echo(" DONE")
