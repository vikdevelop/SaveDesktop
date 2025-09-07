pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'savedesktop'
localedir = join_paths(get_option('prefix'), get_option('localedir'))

gnome = import('gnome')
python = import('python')

# === GResource ===
gnome.compile_resources(
  'savedesktop',
  'savedesktop.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# === Configure wrapper (savedesktop.in -> savedesktop) ===
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('pkgdatadir', pkgdatadir)
conf.set('localedir', localedir)

configure_file(
  input: 'savedesktop.in',
  output: 'savedesktop',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x',
)

# === Install Python sources ===
savedesktop_sources = [
  '__init__.py',
  'main.py',
  'globals.py',
]

install_data(savedesktop_sources, install_dir: moduledir)

subdir('core')
subdir('gui')
