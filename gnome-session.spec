%define glib2_version 2.2.0
%define pango_version 1.2.0
%define gtk2_version 2.2.0
%define libgnome_version 2.3.0
%define libgnomeui_version 2.3.0
%define libbonobo_version 2.3.0
%define libbonoboui_version 2.3.0
%define gnome_vfs2_version 2.3.0
%define gconf2_version 2.2.0

%define po_package gnome-session-2.0

Summary: GNOME session manager
Name: gnome-session
Version: 2.4.0
Release: 3
URL: http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/gnome-session/%{name}-%{version}.tar.bz2
Source1: Gnome.session
Source2: redhat-default-session
Source3: gnome.desktop
License: GPL 
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root

Requires: redhat-artwork >= 0.20
Requires: /usr/share/pixmaps/splash/gnome-splash.png
# required to get gconf-sanity-check-2 in the right place
Requires: GConf2 >= %{gconf2_version}
# Needed for gnome-settings-daemon
Requires: control-center

## we conflict with gdm that contains the GNOME gdm session
Conflicts: gdm < 1:2.4.0.7-7

Patch1: gnome-session-2.2.2-icons.patch
Patch2: gnome-session-2.0.5-login.patch
Patch3: gnome-session-2.0.5-dithering.patch
## http://bugzilla.gnome.org/show_bug.cgi?id=106450
Patch4: gnome-session-2.2.0.2-splash-repaint.patch
Patch5: gnome-session-2.4.0.rh.patch
Patch6: gnome-session-2.4.0-work-with-2-6-glib.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: pango-devel >= %{pango_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libbonoboui-devel >= %{libbonoboui_version}
BuildRequires: gnome-vfs2-devel >= %{gnome_vfs2_version}
BuildRequires: fontconfig

# this is so the configure checks find /usr/bin/halt etc.
BuildRequires: usermode

%description

gnome-session manages a GNOME desktop session. It starts up the other core 
GNOME components and handles logout and saving the session.

%prep
%setup -q

%patch1 -p1 -b .icons
%patch2 -p1 -b .login
%patch3 -p1 -b .dithering
%patch4 -p1 -b .splash-repaint
%patch5 -p1 -b .rh
%patch6 -p1 -b .work-with-2-6-glib

%build
automake-1.4
autoheader
autoconf

%configure --with-halt-command=/usr/bin/poweroff --with-reboot-command=/usr/bin/reboot
make

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%makeinstall
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

./mkinstalldirs $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/GNOME

./mkinstalldirs $RPM_BUILD_ROOT/etc/X11/dm/Sessions/
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT/etc/X11/dm/Sessions/

/bin/rm $RPM_BUILD_ROOT%{_datadir}/gnome/default.session
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/gnome/default.session

#/bin/rm -r $RPM_BUILD_ROOT/var/scrollkeeper

## remove splash screen
rm -r $RPM_BUILD_ROOT%{_datadir}/pixmaps/splash

%find_lang %{po_package}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-session.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
done
/sbin/ldconfig

%files -f %{po_package}.lang
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog NEWS README

%{_datadir}/gnome
%{_datadir}/control-center-2.0
%{_datadir}/man/man*/*
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_sysconfdir}/X11/gdm
%{_sysconfdir}/X11/dm/Sessions/*

%changelog
* Wed Mar 31 2004 Mark McLoughlin <markmc@redhat.com> 2.4.0-3
- Fix X lock up on logout with glib-2.4 installed (bug #119253)

* Wed Nov 05 2003 Than Ngo <than@redhat.com> 2.4.0-2
- don't show gnome-session-properties in KDE (bug #102533)

* Fri Aug 29 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-3
- fix up gnome.desktop location

* Fri Aug 29 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-2
- add gnome.desktop session for new gdm

* Wed Aug 27 2003 Alexander Larsson <alexl@redhat.com> 2.3.7-1
- update to 2.3.7
- require control-center (#100562)

* Fri Aug 15 2003 Alexander Larsson <alexl@redhat.com> 2.3.6.2-1
- update for gnome 2.3

* Sun Aug 10 2003 Elliot Lee <sopwith@redhat.com> 2.2.2-4
- Rebuild

* Tue Jul 22 2003 Jonathan Blandford <jrb@redhat.com>
- at-startup patch to add let at's start

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May 27 2003 Alexander Larsson <alexl@redhat.com> 2.2.2-1
- Update to 2.2.2
- Add XRandR backport
- Fix up old patches, patch7 was upstream

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com> 2.2.0.2-5
- Wait for GSD to start before continuing with session

* Tue Feb 18 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-4
- repaint proper area of text in splash screen, #84527

* Tue Feb 18 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-3
- change icon for magicdev to one that exists in Bluecurve theme
  (part of #84491)

* Thu Feb 13 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-2
- load icons from icon theme

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.2.0.2-1
- 2.2.0.2

* Tue Feb  4 2003 Jonathan Blandford <jrb@redhat.com>
- remove extraneous separator.  Still ugly.

* Wed Jan 29 2003 Havoc Pennington <hp@redhat.com>
- add icons for the stuff in the default session #81489

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan 11 2003 Havoc Pennington <hp@redhat.com>
- 2.1.90
- drop purgedelay patch, as it was increased upstream (though only to 2 minutes instead of 5)

* Fri Dec  6 2002 Tim Waugh <twaugh@redhat.com> 2.1.2-2
- Add eggcups to default session.

* Wed Nov 13 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Tue Sep  3 2002 Owen Taylor <otaylor@redhat.com>
- Up purge delay for session manager to 5 minutes to avoid problem 
  with openoffice.org timing out

* Wed Aug 28 2002 Havoc Pennington <hp@redhat.com>
- put gdm session in here, conflict with old gdm
- use DITHER_MAX for dithering to make splash screen look good in 16
  bit

* Tue Aug 27 2002 Havoc Pennington <hp@redhat.com>
- fix missing icons and misaligned text in splash

* Fri Aug 23 2002 Tim Waugh <twaugh@redhat.com>
- Fix login sound disabling (bug #71664).

* Wed Aug 14 2002 Havoc Pennington <hp@redhat.com>
- put rhn applet in default session

* Wed Aug 14 2002 Havoc Pennington <hp@redhat.com>
- fix the session file, should speed up login a lot
- put magicdev in default session

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 2.0.5 with more translations

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.4
- remove gnome-settings-daemon from default session

* Wed Jul 31 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3
- remove splash screen, require redhat-artwork instead

* Wed Jul 24 2002 Owen Taylor <otaylor@redhat.com>
- Set GTK_RC_FILES so we can change the gtk1 theme

* Tue Jul 16 2002 Havoc Pennington <hp@redhat.com>
- pass --with-halt-command=/usr/bin/poweroff
  --with-reboot-command=/usr/bin/reboot

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0.1, fixing missing po files

* Wed Jun 19 2002 Havoc Pennington <hp@redhat.com>
- put in new default session with pam-panel-icon
- disable schema install in make install, fixes rebuild failure.

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild with new libraries

* Thu Jun 13 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Jun 13 2002 Havoc Pennington <hp@redhat.com>
- add fix from Nalin to build require usermode

* Tue Jun 11 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- install the schemas, so we get a logout dialog and splash
- put in the splash from 7.3

* Sun Jun 09 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Sun Jun 09 2002 Havoc Pennington <hp@redhat.com>
- rebuild in new environment, require newer gtk2

* Sun Jun  9 2002 Havoc Pennington <hp@redhat.com>
- remove obsoletes/provides gnome-core

* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.5.21

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.5.19
- add more build reqs to chill out build system
- provide gnome-core

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- obsolete gnome-core
- 1.5.18

* Fri Apr 19 2002 Havoc Pennington <hp@redhat.com>
- default to metacity

* Tue Apr 16 2002 Havoc Pennington <hp@redhat.com>
- Initial build.


