icons = [
  '16x16',
  '22x22',
  '24x24',
  '32x32',
  '48x48'
]

foreach icon: icons
  install_data(
    join_paths(icon, 'session-properties.png'),
    install_dir: join_paths(session_datadir, 'icons', 'hicolor', icon, 'apps')
  )
endforeach

install_data(
  'scalable/session-properties.svg',
  install_dir: join_paths(session_datadir, 'icons', 'hicolor', 'scalable', 'apps')
)

install_data(
  'symbolic/session-properties-symbolic.svg',
  install_dir: join_paths(session_datadir, 'icons', 'hicolor', 'symbolic', 'apps')
)
