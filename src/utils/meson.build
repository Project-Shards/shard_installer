pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'shard_installer/utils')

shard_installer_sources = [
    '__init__.py',
    'command.py',
    'diskutils.py',
    'fileutils.py',
]

install_data(shard_installer_sources, install_dir: moduledir)
