%define beta %nil
%define scmrev %nil
# Apparently we can't create debug packages for objective-c
%define debug_package %nil

Name: sope
Version: 2.0.6b
%if "%scmrev" == ""
%if "%beta" != ""
Release: 0.%beta.1
%else
Release: 2
%endif
Source: http://www.sogo.nu/files/downloads/SOGo/Sources/SOPE-%version%beta.tar.gz
%else
Release: 0.%scmrev.1ark
Source: SOPE-%scmrev.tar.xz
%endif
Summary: The SOPE application server
URL: http://sogo.nu/
License: GPL
Group: System/Servers
BuildRequires: gnustep-make >= 2.6.2-3
BuildRequires: gnustep-base-devel gnustep-gui-devel
BuildRequires: gcc-objc
# Not strictly required, but the resulting SOPE gets more features
# if they're there
BuildRequires: pkgconfig(libxml-2.0) openldap-devel pkgconfig(libssl) postgresql-devel mysql-devel

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

%track
prog sope = {
	version = %{version}
	url = http://www.sogo.nu/downloads/backend.html
	regex = SOGo-(__VER__)\.tar\.gz
}

%prep
%setup -q -n SOPE
# Not autoconf, even though it looks similar
# Not actually %_prefix/System -- the bogus configure script translates
# that to "GNUstep System installation"
# --enable-debug is the default, but builds with -O0, we don't want that.
# Aside from slowing things down, it doesn't allow _FORTIFY_SOURCE, which
# we should really have for server related packages.
./configure --prefix=%_prefix/System --with-gnustep --disable-debug

%build
make %?_smp_mflags CC="%__cc -fuse-ld=bfd"

%install
rm -rf $RPM_BUILD_ROOT
make %?_smp_mflags install DESTDIR="$RPM_BUILD_ROOT" GNUSTEP_INSTALLATION_DOMAIN=SYSTEM

%files
%_libdir/*.so*
%_libdir/GNUstep/*-4.9
%_libdir/GNUstep/Libraries/Resources/NGObjWeb
%_datadir/GNUstep/Makefiles/*.make
%_datadir/GNUstep/Makefiles/Additional/*.make
%_bindir/wod
%_bindir/load-EOAdaptor
%_bindir/connect-EOAdaptor

%files devel
%_includedir/*
