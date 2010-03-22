bin_PROGRAMS = gnome-session-save

if BUILD_SESSION_SELECTOR
bin_PROGRAMS += gnome-session-selector
dist_bin_SCRIPTS = gnome-session-custom-session
endif

INCLUDES =					\
	$(WARN_CFLAGS)				\
	$(DISABLE_DEPRECATED_CFLAGS)		\
	$(GNOME_SESSION_CFLAGS)			\
	$(DBUS_GLIB_CFLAGS)			\
	$(GCONF_CFLAGS)				\
	-DGTKBUILDER_DIR=\""$(pkgdatadir)"\"	\
	-DLOCALE_DIR=\""$(datadir)/locale"\"

gnome_session_save_LDADD =			\
	$(SM_LIBS)				\
	$(ICE_LIBS)				\
	$(GNOME_SESSION_LIBS)			\
	$(DBUS_GLIB_LIBS)			\
	$(GCONF_LIBS)

gnome_session_save_SOURCES =			\
	gnome-session-save.c

if BUILD_SESSION_SELECTOR
gnome_session_selector_LDADD = 				\
	$(SESSION_SELECTOR_LIBS)

gnome_session_selector_SOURCES = 			\
	gnome-session-selector.c
endif

-include $(top_srcdir)/git.mk
