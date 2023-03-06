pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'shard_installer')

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('pkgdatadir', pkgdatadir)
configure_file(
            input: 'shard_installer.in',
           output: 'shard_installer',
    configuration: conf,
          install: true,
      install_dir: get_option('bindir')
)

shard_installer_sources = [
    '__init__.py',
    'main.py'
]

install_data(shard_installer_sources, install_dir: moduledir)
subdir('utils')
subdir('funtions')
