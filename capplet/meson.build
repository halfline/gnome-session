install_data(
  install_dir: session_bindir
)

deps = session_deps + [
  glib_dep,
  gtk_dep,
  x11_dep,
  sm_dep,
  ice_dep,
  dbus_glib_dep
]

cflags = [
  '-DLOCALE_DIR="@0@"'.format(session_localedir),
  '-DGTKBUILDER_DIR="@0@"'.format(session_pkgdatadir)
]

sources = files(
  '../gnome-session/gsm-util.c',
  'gsm-app-dialog.c',
  'gsm-properties-dialog.c',
  'gsp-app.c',
  'gsp-app-manager.c',
  'gsp-keyfile.c',
  'main.c'
)

executable(
  'gnome-session-properties',
  sources,
  include_directories: [ top_inc, include_directories('../gnome-session') ],
  dependencies: deps,
  c_args: cflags,
  install: true,
  install_dir: session_bindir
)
