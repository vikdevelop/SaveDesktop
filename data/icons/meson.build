application_id = 'io.github.vikdevelop.SaveDesktop'

# Scalable app icons
scalable_apps_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  files(
    join_paths(scalable_apps_dir, ('@0@.svg').format(application_id)),
    join_paths(scalable_apps_dir, ('@0@.Devel.svg').format(application_id))
  ),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_apps_dir)
)

# Scalable status icon
scalable_status_dir = join_paths('hicolor', 'scalable', 'status')
install_data(
  files(join_paths(scalable_status_dir, 'done.svg')),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_status_dir)
)

# Symbolic app icon
symbolic_apps_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  files(join_paths(symbolic_apps_dir, ('@0@-symbolic.svg').format(application_id))),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_apps_dir)
)