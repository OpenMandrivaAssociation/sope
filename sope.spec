%define beta %nil
%define scmrev %nil
# Apparently we can't create debug packages for objective-c
%define debug_package %nil

Name: sope
Version: 2.0.0
%if "%scmrev" == ""
%if "%beta" != ""
Release: 0.%beta.1
%else
Release: 1
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
BuildRequires: gnustep-make gnustep-base-devel gnustep-gui-devel
BuildRequires: gcc-objc

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
%setup -q -n SOPE
# Not autoconf, even though it looks similar
# Not actually %_prefix/System -- the bogus configure script translates
# that to "GNUstep System installation"
./configure --prefix=%_prefix/System --with-gnustep

%build
make %?_smp_mflags

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
