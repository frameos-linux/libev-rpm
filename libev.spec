#
# spec file for package libev
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild


Name:           libev
Version:        4.04
Release:        5%{?dist}
#
License:        BSD
Group:          Development/Libraries/C and C++
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#
URL:            http://software.schmorp.de/pkg/libev.html
Source:         http://dist.schmorp.de/libev/%{name}-%{version}.tar.gz
#
%if 0%{?suse_version} < 1000
BuildRequires:  pkgconfig
%else
BuildRequires:  pkg-config
%endif
#
Summary:        A full-featured and high-performance event loop library
%description
A full-featured and high-performance event loop that is loosely modelled after
libevent, but without its limitations and bugs. It is used, among others, in
the GNU Virtual Private Ethernet and rxvt-unicode packages.


Authors:
---------
    - Marc Lehmann
    - Emanuele Giaquinta

%define library_name libev4
%package -n %{library_name}
Group:          Development/Libraries/C and C++
#
Summary:        A full-featured and high-performance event loop library
%description -n %{library_name}
A full-featured and high-performance event loop that is loosely modelled after
libevent, but without its limitations and bugs. It is used, among others, in
the GNU Virtual Private Ethernet and rxvt-unicode packages.


This package holds the shared libraries of libev.


Authors:
---------
    - Marc Lehmann
    - Emanuele Giaquinta


%package devel
Group:          Development/Libraries/C and C++
Requires:       %{library_name} = %{version}
#
Summary:        Development files for libev
%description devel
A full-featured and high-performance event loop that is loosely modelled after
libevent, but without its limitations and bugs. It is used, among others, in
the GNU Virtual Private Ethernet and rxvt-unicode packages.


This package holds the development files for libev.


Authors:
---------
    - Marc Lehmann
    - Emanuele Giaquinta


%prep
%setup

%build
export CPPFLAGS="-DEV_FORK_ENABLE=0 -DEV_EMBED_ENABLE=0 -DEV_MULTIPLICITY=0"
export CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
%configure
%{__make}


%check
%{__make} check

%install
%makeinstall

%{__rm} -f %{buildroot}/%{_libdir}/libev.la

%clean
%{__rm} -rf %{buildroot}

%post   -n %{library_name} -p /sbin/ldconfig

%postun -n %{library_name} -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%doc LICENSE README ev.pod Changes
%{_includedir}/ev++.h
%{_includedir}/ev.h
%{_includedir}/event.h
%{_libdir}/libev.so
%{_libdir}/libev.a
%{_mandir}/man3/ev.3*

%files -n %{library_name}
%defattr(-,root,root,-)
%{_libdir}/libev.so.4*

%changelog
* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 4.04-5
- add Source URL

* Mon Feb 21 2011 efimovov@gmail.com
- remove *.la files from package
* Mon Feb 21 2011 efimovov@gmail.com
- update to latest release version (4.04)
- switch to bz2
* Mon Feb  7 2011 efimovov@gmail.com
- add "-DEV_FORK_ENABLE=0 -DEV_EMBED_ENABLE=0 -DEV_MULTIPLICITY=0" for Node.js
* Wed Feb  2 2011 efimovov@gmail.com
- update to latest release version (4.03)
* Sun Jan  9 2011 efimovov@gmail.com
- update to latest CVS version (4.01+)
* Sun Jan  9 2011 efimovov@gmail.com
- downgrade to version 4.00
* Fri Dec 24 2010 efimovov@gmail.com
- fork from stbuehler's source
* Sat Nov  6 2010 stbuehler@web.de
- build-require pkg-config to provide pkgconfig(libev)
- update to version 4.01
  - automake fucked it up, apparently, --add-missing -f is not quite enough
    to make it update its files, so 4.00 didn't install ev++.h and
    event.h on make install. grrr.
  - ev_loop(count|depth) didn't return anything (Robin Haberkorn).
  - change EV_UNDEF to 0xffffffff to silence some overzealous compilers.
  - use "(libev) " prefix for all libev error messages now.
* Mon Oct 25 2010 mrueckert@suse.de
- update to version 4.00
  - "PORTING FROM LIBEV 3.X TO 4.X" (in ev.pod) is recommended
    reading.
  - ev_embed_stop did not correctly stop the watcher (very good
    testcase by Vladimir Timofeev).
  - ev_run will now always update the current loop time - it
    erroneously didn't when idle watchers were active, causing
    timers not to fire.
  - fix a bug where a timeout of zero caused the timer not to fire
    in the libevent emulation (testcase by Péter Szabó).
  - applied win32 fixes by Michael Lenaghan (also James Mansion).
  - replace EV_MINIMAL by EV_FEATURES.
  - prefer EPOLL_CTL_ADD over EPOLL_CTL_MOD in some more cases, as
    it seems the former is *much* faster than the latter.
  - linux kernel version detection (for inotify bug workarounds)
    did not work properly.
  - reduce the number of spurious wake-ups with the ports backend.
  - remove dependency on sys/queue.h on freebsd (patch by Vanilla
    Hsu).
  - do async init within ev_async_start, not ev_async_set, which
    avoids an API quirk where the set function must be called in
    the C++ API even when there is nothing to set.
  - add (undocumented) EV_ENABLE when adding events with kqueue,
    this might help with OS X, which seems to need it despite
    documenting not to need it (helpfully pointed out by Tilghman
    Lesher).
  - do not use poll by default on freebsd, it's broken (what isn't
    on freebsd...).
  - allow to embed epoll on kernels >= 2.6.32.
  - configure now prepends -O3, not appends it, so one can still
    override it.
  - ev.pod: greatly expanded the portability section, added a
    porting section, a description of watcher states and made lots
    of minor fixes.
  - disable poll backend on AIX, the poll header spams the
    namespace and it's not worth working around dead platforms
    (reported and analyzed by Aivars Kalvans).
  - improve header file compatibility of the standalone eventfd
    code in an obscure case.
  - implement EV_AVOID_STDIO option.
  - do not use sscanf to parse linux version number (smaller,
    faster, no sscanf dependency).
  - new EV_CHILD_ENABLE and EV_SIGNAL_ENABLE configurable settings.
  - update libev.m4 HAVE_CLOCK_SYSCALL test for newer glibcs.
  - add section on accept() problems to the manpage.
  - rename EV_TIMEOUT to EV_TIMER.
  - rename ev_loop_count/depth/verify/loop/unloop.
  - remove ev_default_destroy and ev_default_fork.
  - switch to two-digit minor version.
  - work around an apparent gentoo compiler bug.
  - use enum instead of #define for most constants.
  - improve compatibility to older C++ compilers.
  - (experimental) ev_run/ev_default_loop/ev_break/ev_loop_new have
    now default arguments when compiled as C++.
  - ev_loop_new no longer leaks memory when loop creation failed.
  - new ev_cleanup watcher type.
- move pkgconfig file to devel package
- updated compiler warnings patch:
  old name libev-3.9_compiler_warnings.patch
  new name libev-4.00_compiler_warnings.patch
* Mon Aug 23 2010 mrueckert@suse.de
- added libev-3.9_pkg-config.patch:
  patch by stbuehler.
* Wed Jul 14 2010 mrueckert@suse.de
- update to 3.9
  for the changes see /usr/share/doc/packages/libev-devel/Changes
* Thu Feb 19 2009 mrueckert@suse.de
- update to 3.53
  for the changes see /usr/share/doc/packages/libev-devel/Changes
* Tue Sep 16 2008 mrueckert@suse.de
- update to 3.43
  for the changes see /usr/share/doc/packages/libev-devel/Changes
* Thu Feb 28 2008 mrueckert@suse.de
- update to version 3.0:
  - API/ABI bump to version 3.0.
  - ev++.h includes "ev.h" by default now, not <ev.h>.
  - slightly improved documentation.
  - speed up signal detection after a fork.
  - only optionally return trace status changed in ev_child watchers.
  - experimental (and undocumented) loop wrappers for ev++.h.
- additional changes from 2.01:
  - separate Changes file.
  - fix ev_path_set => ev_stat_set typo.
  - remove event_compat.h from the libev tarball.
  - change how include files are found.
  - doc updates.
  - update licenses, explicitly allow for GPL relicensing.
* Sun Dec 23 2007 mrueckert@suse.de
- fix license
* Sun Dec 23 2007 mrueckert@suse.de
- initial package
