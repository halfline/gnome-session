%define glib2_version 2.0.0
%define gtk2_version 2.0.3-3
%define libgnome_version 1.117.2
%define libgnomeui_version 1.117.2
%define libbonobo_version 2.0.0
%define libbonoboui_version 1.118.0
%define gnome_vfs2_version 1.9.16
%define bonobo_activation_version 1.0.0

Summary: GNOME session manager
Name: gnome-session
Version: 2.0.0
Release: 3
URL: http://www.gnome.org
Source0: ftp://ftp.gnome.org/pub/GNOME/pre-gnome2/sources/gnome-session/%{name}-%{version}.tar.bz2
Source1: gnome-redhat-splash.png
License: GPL 
Group: User Interface/Desktops
BuildRoot: %{_tmppath}/%{name}-root

Patch1: gnome-session-1.5.16-metacity-default.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnome-devel >= %{libgnome_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libbonoboui-devel >= %{libbonoboui_version}
BuildRequires: gnome-vfs2-devel >= %{gnome_vfs2_version}
BuildRequires: bonobo-activation-devel >= %{bonobo_activation_version}
BuildRequires: Xft
BuildRequires: fontconfig

# this is so the configure checks find /usr/bin/halt etc.
BuildRequires: usermode

%description

gnome-session manages a GNOME desktop session. It starts up the other core 
GNOME components and handles logout and saving the session.

%prep
%setup -q

%patch1 -p1 -b .metacity-default

cp -f %{SOURCE1} gnome-session/gnome-splash.png

## temporary hack until I rebuild libs
perl -pi -e 's/REQUIRED=2.0.0/REQUIRED=1.117.0/g' configure configure.in

%build

%configure
make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-session.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S > /dev/null
done
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)

%doc AUTHORS COPYING ChangeLog NEWS README

%{_datadir}/pixmaps
%{_datadir}/gnome
%{_datadir}/control-center-2.0
%{_datadir}/omf
%{_datadir}/man/man*/*
%{_bindir}/*
%{_sysconfdir}/gconf/schemas/*.schemas

%changelog
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


