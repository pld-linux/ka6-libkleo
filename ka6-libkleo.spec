#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.12.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		libkleo
Summary:	Kleo library
Summary(pl.UTF-8):	Biblioteka kleo
Name:		ka6-%{kaname}
Version:	24.12.0
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	4a4bfe78512aac80d6c70a8d5d52f5b4
URL:		http://www.kde.org/
BuildRequires:	Qt6Gui-devel >= 5.11.1
BuildRequires:	Qt6Widgets-devel
BuildRequires:	boost-devel >= 1.34.0
BuildRequires:	gettext-devel
BuildRequires:	gpgme-qt6-devel >= 1:1.23.2
BuildRequires:	ka6-kpimtextedit-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kitemmodels-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kleo library.

%description -l pl.UTF-8
Biblioteka kleo.

%package devel
Summary:	Header files for libkipi development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for libkipi development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
/etc/xdg/libkleopatrarc
%dir %{_datadir}/libkleopatra
%dir %{_datadir}/libkleopatra/pics
%{_datadir}/libkleopatra/pics/smartcard.xpm
%{_datadir}/qlogging-categories6/libkleo.categories
%{_datadir}/qlogging-categories6/libkleo.renamecategories
%attr(755,root,root) %{_libdir}/libKPim6Libkleo.so.*.*
%ghost %{_libdir}/libKPim6Libkleo.so.6

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/Libkleo
%{_libdir}/cmake/KPim6Libkleo
%{_libdir}/libKPim6Libkleo.so
%{_datadir}/KPim6Libkleo
