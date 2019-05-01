%define beta %nil
%define scmrev %nil
# Apparently we can't create debug packages for objective-c
%define debug_package %nil
%define _disable_lto 1
%define _disable_rebuild_configure 1

Name: sope
Version: 4.0.7
%if "%scmrev" == ""
%if "%beta" != ""
Release: 1.%beta.1
%else
Release: 1
%endif
Source0: http://www.sogo.nu/files/downloads/SOGo/Sources/SOPE-%version%beta.tar.gz
%else
Release: 1.%scmrev.1ark
Source0: SOPE-%scmrev.tar.xz
%endif
Source100: %{name}.rpmlintrc
Patch0: SOPE-2.1.1b-link.patch
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

%track
prog sope = {
	version = %{version}
	url = http://www.sogo.nu/downloads/backend.html
	regex = SOGo-(__VER__)\.tar\.gz
}

%prep
%setup -q -n SOPE
%apply_patches
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
make %?_smp_mflags CC="gcc -fuse-ld=bfd" messages=yes OPTFLAG='%optflags'

%install
rm -rf $RPM_BUILD_ROOT
make %?_smp_mflags install DESTDIR="$RPM_BUILD_ROOT" GNUSTEP_INSTALLATION_DOMAIN=SYSTEM

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
