%define major 1
%define libname %mklibname accounts-qt5_ %{major}
%define devname %mklibname accounts-qt5 -d

Summary:	Qt bindings for Accounts framework
Name:		libaccounts-qt
Version:	1.14
Release:	1
License:	LGPLv2.1+
Group:		System/Libraries
Url:		https://gitlab.com/accounts-sso/libaccounts-qt
# (tpg) wget https://gitlab.com/accounts-sso/libaccounts-qt/repository/archive.tar.bz2?ref=VERSION_1.14
Source0:	https://accounts-sso.googlecode.com/files/%{name}-%{version}.tar.xz
BuildRequires:	doxygen
BuildRequires:  qt5-devel
BuildRequires:	pkgconfig(libaccounts-glib)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Test)

%description
Qt bindings for Accounts framework.

#------------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Shared library for Qt bindings for Accounts framework.

%files -n %{libname}
%{_libdir}/libaccounts-qt5.so.%{major}*

#---------------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/KDE and Qt
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Provides:	accounts-qt = %{EVRD}

%description -n %{devname}
Development files for %{name}.

%files -n %{devname}
%{_bindir}/accountstest
%{_datadir}/libaccounts-qt-tests
%{_includedir}/accounts-qt5
%{_libdir}/libaccounts-qt5.so
%{_libdir}/cmake/AccountsQt5
%{_libdir}/pkgconfig/accounts-qt5.pc

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

%prep
%setup -q

%build
%qmake_qt5 \
	QMF_INSTALL_ROOT=%{_prefix} \
	LIBDIR=%{_libdir} \
	CONFIG+=release \
	accounts-qt.pro
%make

%install
make install INSTALL_ROOT=%{buildroot} STRIP=true
