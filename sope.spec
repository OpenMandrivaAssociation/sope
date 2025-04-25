# Apparently we can't create debug packages for objective-c
%define debug_package %nil
#define _disable_lto 1
%define _disable_rebuild_configure 1

# Get rid of -Werror=format-security for now
%global Werror_cflags -Wformat

Name: sope
Version:	5.12.0
Release:	1
Source0:	https://packages.sogo.nu/sources/SOPE-%version.tar.gz
Source100: %{name}.rpmlintrc
Patch0: SOPE-2.1.1b-link.patch
Patch1: sope-5.8.0-enable-sqlite.patch
Patch2: SOPE-5.10.0-compile.patch
Patch3: SOPE-5.8.2-clang16.patch
Summary: The SOPE application server
URL: https://sogo.nu/
License: GPL
Group: System/Servers
BuildRequires: gnustep-make >= 2.6.2-3
BuildRequires: gnustep-base-devel gnustep-gui-devel
BuildRequires: pkgconfig(libobjc)
# Not strictly required, but the resulting SOPE gets more features
# if they're there
BuildRequires: pkgconfig(libxml-2.0) pkgconfig(ldap) pkgconfig(libssl) pkgconfig(libpq) pkgconfig(mariadb) pkgconfig(sqlite3)
# For config.guess
BuildRequires: libtool-base

%description
The SOPE application server, primarily used by SOGo

%package devel
Summary: Development files for the SOPE application server
Group: Development/Other
Requires: %name = %version-%release

%description devel
Development files for the SOPE application server

Install %name-devel if you wish to develop or compile
applications that use SOPE.

%prep
%autosetup -p1 -n SOPE
# For aarch64
cp -f %{_datadir}/libtool/config/config.{guess,sub} sope-core/NGStreams/
# just replace sparc64 with aarch64
# to fix _libdir path
sed -i 's!sparc64!aarch64!g' configure
cp -f %{_datadir}/libtool/config/config.guess sope-core/NGStreams/
# Not autoconf, even though it looks similar
# Not actually %_prefix/System -- the bogus configure script translates
# that to "GNUstep System installation"
# --enable-debug is the default, but builds with -O0, we don't want that.
# Aside from slowing things down, it doesn't allow _FORTIFY_SOURCE, which
# we should really have for server related packages.
./configure --prefix=%_prefix --disable-debug

%build
# FIXME we set ALL_LDFLAGS to "" just to avoid the combination of -r and -rdynamic
%make_build messages=yes OPTFLAG='%optflags -Wno-error=format-security' ALL_LDFLAGS=""

%install
%make_install GNUSTEP_INSTALLATION_DOMAIN=SYSTEM

%files
%_libdir/*.so*
%_libdir/sope-4.9
%_datadir/sope-4.9
%_bindir/wod
%_bindir/load-EOAdaptor
%_bindir/connect-EOAdaptor

%files devel
%_includedir/*
%_datadir/GNUstep/Makefiles/*.make
%_datadir/GNUstep/Makefiles/*/*.make
