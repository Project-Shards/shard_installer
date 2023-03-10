pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'shard_installer/functions')

shard_installer_sources = [
    '__init__.py',
    'partition.py',
    'localization.py',
    'shards.py',
    'user.py',
    'bootloader.py',
    'hostname.py'
]

install_data(shard_installer_sources, install_dir: moduledir)
