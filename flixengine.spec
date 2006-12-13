#
# Conditional build:
%bcond_with	tests		# build with tests
%bcond_without	tests		# build without tests
#
Summary:	flixengine
Name:		flixengine
Version:	8.0.7.0
Release:	0.1
License:	not distributable
Group:		Applications
# download demo from http://flix.on2.com/demos/
Source0:	%{name}linuxdemo.tar.gz
# Source0-md5:	ea7d3a0efaf08611aad9374259015d71
NoSource:	0
URL:		http://www.on2.com/developer/flix-engine-sdk
BuildRequires:	ffmpeg-libs
BuildRequires:	jre
BuildRequires:	lame-libs
BuildRequires:	perl-base
BuildRequires:	php-devel
BuildRequires:	python
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/libexec

%description
flix engine

%package libs
Summary:	flixengine libs
Group:		Libraries

%description libs
flixengine libs

%package devel
Summary:	Header files for flixengine library
Group:		Development/Libraries

%description devel
Header files for flixengin library.

%prep
%setup -q -n flix-engine-installer-linux-%{version}_DEMO

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

./flix-engine-installer-linux-%{version}_DEMO.bin \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	--just-install \
	--offline \
	--yesireadtheon2license \

# current ac has same with same soname
rm -f $RPM_BUILD_ROOT%{_libdir}/libmp3lame.so.0.0.0

# symlink without buildroot
ln -sf %{_prefix}/src/flixmodules/flixjava/doc $RPM_BUILD_ROOT%{_docdir}/on2/flixengine/javadoc

# use poldek -e
rm -f $RPM_BUILD_ROOT%{_sbindir}/flix-engine-uninstall.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_docdir}/on2
%attr(755,root,root) %{_sbindir}/flixd
%attr(755,root,root) %{_sbindir}/lget
%attr(755,root,root) %{_sbindir}/on2_host_info
%{_mandir}/man8/flixd.8*
%{_libexecdir}/on2/flixengine/mencoder
%{_datadir}/on2

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflixengine2.so.0.2
%attr(755,root,root) %{_libdir}/libflixengine2_core.so.0.2

# current ac has libavutil.so.49.1.0, libavcodec.so.51.25.0
%attr(755,root,root) %{_libdir}/libavcodec.so.51.11.0
%attr(755,root,root) %{_libdir}/libavutil.so.49.0.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/flixengine2
%{_prefix}/src/flixmodules
