%define major 1
%define oldlibname %mklibname accounts-qt5_ 1
%define libname %mklibname accounts-qt5
%define devname %mklibname accounts-qt5 -d
%define lib6name %mklibname accounts-qt6
%define dev6name %mklibname accounts-qt6 -d

%bcond_without qt5
%bcond_without qt6

Summary:	Qt bindings for Accounts framework
Name:		libaccounts-qt
Version:	1.16
Release:	6
License:	LGPLv2.1+
Group:		System/Libraries
Url:		https://gitlab.com/accounts-sso/libaccounts-qt
Source0:	https://gitlab.com/accounts-sso/libaccounts-qt/-/archive/VERSION_%{version}/libaccounts-qt-VERSION_%{version}.tar.bz2
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libaccounts-glib)
%if %{with qt5}
BuildRequires:  qt5-devel
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Test)
%endif
%if %{with qt6}
BuildRequires:  cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Test)
%endif

%description
Qt bindings for Accounts framework.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
Shared library for Qt bindings for Accounts framework.

%if %{with qt5}
%files -n %{libname}
%{_libdir}/libaccounts-qt5.so.%{major}*
%endif

#---------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	accounts-qt = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%if %{with qt5}
%files -n %{devname}
%{_bindir}/accountstest
%{_includedir}/accounts-qt5
%{_libdir}/libaccounts-qt5.so
%{_libdir}/cmake/AccountsQt5
%{_libdir}/pkgconfig/accounts-qt5.pc
%endif

#------------------------------------------------------------------------------

%package -n %{lib6name}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{lib6name}
Shared library for Qt bindings for Accounts framework.

%if %{with qt6}
%files -n %{lib6name}
%{_libdir}/libaccounts-qt6.so.%{major}*
%endif

#---------------------------------------------------------------------------------

%package -n %{dev6name}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{lib6name} = %{EVRD}

%description -n %{dev6name}
Development files for %{name}.

%if %{with qt6}
%files -n %{dev6name}
%{_includedir}/accounts-qt6
%{_libdir}/libaccounts-qt6.so
%{_libdir}/cmake/AccountsQt6
%{_libdir}/pkgconfig/accounts-qt6.pc
%endif

#------------------------------------------------------------------------------

%package doc
Summary:	Documentation for %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%files doc
%dir %{_defaultdocdir}/accounts-qt
%{_defaultdocdir}/accounts-qt/*

#------------------------------------------------------------------------------

%global optflags %{optflags} -I..

%prep
%autosetup -n %{name}-VERSION_%{version} -p1
echo 'INCLUDEPATH += ..' >>Accounts/Accounts.pro
mkdir -p qt5
mv $(ls |grep -v qt5) qt5/
cp -a qt5 qt6
# tests are currently broken for qt6 (qmake not
# knowing "testlib")
sed -i -e 's, tests,,' qt6/*.pro
find qt6 -name "*5*" |while read i; do
	mv $i ${i/5/6}
done
find qt6 -type f |xargs sed -i -e 's,Qt5,Qt6,g;s,qt5,qt6,g'

%if %{with qt5}
cd qt5
%qmake_qt5 \
	QMF_INSTALL_ROOT=%{_prefix} \
	LIBDIR=%{_libdir} \
	CONFIG+=release \
	accounts-qt.pro
cd ..
%endif

%if %{with qt6}
cd qt6
qmake-qt6 \
	QMF_INSTALL_ROOT=%{_prefix} \
	LIBDIR=%{_libdir} \
	CONFIG+=release \
	accounts-qt.pro
%endif

%build
%if %{with qt5}
%make_build -C qt5
%endif
%if %{with qt6}
%make_build -C qt6
%endif

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
%if %{with qt5}
make -C qt5 install INSTALL_ROOT=%{buildroot} STRIP=true
cat >%{buildroot}%{_libdir}/pkgconfig/accounts-qt5.pc <<EOF
Name: libaccounts-qt5
Description: Accounts Library
Libs: -laccounts-qt5
Requires: Qt5Core Qt5Xml
Cflags: -I%{_includedir}/accounts-qt5
EOF
%endif
%if %{with qt6}
make -C qt6 install INSTALL_ROOT=%{buildroot} STRIP=true
cat >%{buildroot}%{_libdir}/pkgconfig/accounts-qt6.pc <<EOF
Name: libaccounts-qt6
Description: Accounts Library
Libs: -laccounts-qt6
Requires: Qt6Core Qt6Xml
Cflags: -I%{_includedir}/accounts-qt6
EOF
%endif
