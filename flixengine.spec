#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_with	tests	# perform "make test". needs running flixd on localhost
#
%include	/usr/lib/rpm/macros.perl
Summary:	On2 Flix Engine
Name:		flixengine
Version:	8.0.7.0
Release:	0.5
License:	not distributable
Group:		Applications
# download demo from http://flix.on2.com/demos/
Source0:	%{name}linuxdemo.tar.gz
# Source0-md5:	ea7d3a0efaf08611aad9374259015d71
NoSource:	0
URL:		http://www.on2.com/developer/flix-engine-sdk
%if %{with autodeps}
BuildRequires:	ffmpeg-libs
BuildRequires:	lame-libs
%endif
BuildRequires:	bash
BuildRequires:	jre
BuildRequires:	perl-base
BuildRequires:	php-devel
BuildRequires:	python
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/libexec
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

%description
The On2 Flix Engine provides many of the Flash 8 video encoding
features of our industry leading On2 Flix Pro video encoder in a
powerful software SDK.

The Engine enables you to add the power and efficiency of Flash video
with On2 VP6 encoding to your intranet, website and other server-based
applications, preserve alpha channel in the video output, and much
more.

The major feature of the On2 Flix Engine 8 is support for Adobe Flash
8 video with the On2 VP6 codec and FLV video output that can be played
directly in the Flash Player, streamed through the Adobe Flash Media
Server, or imported into Flash Studio. The new FLV output also is
fully compliant with FLV format metadata and Adobe Flash Player
standards.

%package libs
Summary:	Shared libraries for On2 Flix Engine
Group:		Libraries

%description libs
Shared libraries for On2 Flix Engine.

%package devel
Summary:	Header files for On2 Flix Engine library
Group:		Development/Libraries

%description devel
Header files for On2 Flix Engine library.

%package -n java-flixengine
Summary:	Java bindings for On2 Flix Engine
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n java-flixengine
Java bindings for On2 Flix Engine.

%package -n perl-flixengine
Summary:	Perl bindings for On2 Flix Engine
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-flixengine
Perl bindings for On2 Flix Engine.

%package -n php-flixengine
Summary:	PHP bindings for On2 Flix Engine
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n php-flixengine
PHP bindings for On2 Flix Engine.

%package -n python-flixengine
Summary:	Python bindings for On2 Flix Engine
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-flixengine
Python bindings for On2 Flix Engine.

%prep
%setup -q -n flix-engine-installer-linux-%{version}_DEMO
bin=flix-engine-installer-linux-%{version}_DEMO.bin
tar=flix-engine-linux-%{version}_DEMO.tar.gz

OFFSET=$( awk -F= '/OFFSET=/{print $2; exit}' $bin)
dd bs=8 if=$bin of=$tar skip=$OFFSET
%{__tar} zxf $tar

%{__sed} -ne '/## FUNCTIONS common/,/## END - common function/p' $bin > functions.sh
cat <<'EOF' > install.sh
#!/bin/bash
export VERSION=%{version}_DEMO
export FLIXENGINEDEMO=1
export nullout=/dev/null
export tempdir=%{_builddir}/flix-engine-installer-linux-%{version}_DEMO

. $(dirname "$0")/functions.sh
cd .flix-engine-installation-files

export -f getinput inset ynanswer
./install.sh "$@"
EOF
chmod +x install.sh

cd .flix-engine-installation-files
%{__sed} -i -e '
# force installing initscript into buildroot without detection
s,^initchk$,inittype=sysv1; INITDIR=$RPM_BUILD_ROOT/etc/rc.d/init.d,

# cls is annoying
s,clear 2>\$nullout,#&,

# we want to install examples, but not compile them in install
# and somewhy --no-compile didn not work, had to specify also --no-modules,
# which made no modules installed either, chicken-egg problem.
s,COMPILEMODULES=y,COMPILEMODULES=n,
s,INSTALLEDPERLFILES="n",INSTALLEDPERLFILES="y",
s,INSTALLEDPHPFILES="n",INSTALLEDPHPFILES="y",
s,INSTALLEDPYTHONFILES="n",INSTALLEDPYTHONFILES="y",
s,INSTALLEDFLIXLIBRARIES="n",INSTALLEDFLIXLIBRARIES="y",
s,INSTALLEDJAVAFILES="n",INSTALLEDJAVAFILES="y",

' install.sh

%build
cd .flix-engine-installation-files

ln -snf flixhdrs flixengine2
export C_INCLUDE_PATH=$(pwd)

ldconfig -n flixlibs
export LD_LIBRARY_PATH=$(pwd)/flixlibs
export LIBRARY_PATH=$(pwd)/flixlibs

# PHP
%{__make} -C flixphp \
	CC="%{__cc}" \
	-f target.mk \

# Perl
cd flixperl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"
%{?with_tests:%{__make} test}
cd ..

# Python
cd flixpython
%{__python} setup.py build
cd ..

# Java
%{__make} -C flixjava \
	CC="%{__cc}" \
	-f target.mk

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

./install.sh \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	--flixsamples=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	--pidfile=$RPM_BUILD_ROOT/var/run/flixd.pid \
	--authdir=$RPM_BUILD_ROOT/var/lib/on2 \
	--just-install \
	--offline \
	--yesireadtheon2license \
	--no-compile \
	--no-modules \
	--no-init \
	--noprereqlibs

# install bindings
cd .flix-engine-installation-files
# PHP
%{__make} -C flixphp \
	install \
	PHPINST=$RPM_BUILD_ROOT%{extensionsdir} \
	-f target.mk

# Perl
cd flixperl
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/On2/flixengine2/.packlist
cd ..

# Python
cd flixpython
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean
cd ..

# Java
%{__make} -C flixjava \
	SOINST=$RPM_BUILD_ROOT%{_libdir} \
	JARINST=$RPM_BUILD_ROOT%{_javadir} \
	install \
	-f target.mk

# symlink without buildroot
ln -snf %{_prefix}/src/flixmodules/flixjava/doc $RPM_BUILD_ROOT%{_docdir}/on2/flixengine/javadoc

# do not put hardware fingerprint to rpm package
> $RPM_BUILD_ROOT/var/lib/on2/hostinfo

# use poldek -e
rm -f $RPM_BUILD_ROOT%{_sbindir}/flix-engine-uninstall.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
if [ ! -s /var/lib/on2/hostinfo ]; then
	%{_sbindir}/on2_host_info > /var/lib/on2/hostinfo
fi

%files
%defattr(644,root,root,755)
%doc %{_docdir}/on2
%attr(755,root,root) %{_sbindir}/flixd
%attr(755,root,root) %{_sbindir}/lget
%attr(755,root,root) %{_sbindir}/on2_host_info
%attr(754,root,root) /etc/rc.d/init.d/flixengine
%{_mandir}/man8/flixd.8*
%dir /var/lib/on2
%config(noreplace) %verify(not md5 mtime size) /var/lib/on2/hostinfo
%{_libexecdir}/on2/flixengine/mencoder

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflixengine2.so.*.*
%attr(755,root,root) %{_libdir}/libflixengine2_core.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflixengine2.so
%attr(755,root,root) %{_libdir}/libflixengine2_core.so
%{_includedir}/flixengine2

%dir %{_examplesdir}/%{name}-%{version}
%{_examplesdir}/%{name}-%{version}/c
%{_examplesdir}/%{name}-%{version}/java
%{_examplesdir}/%{name}-%{version}/perl
%{_examplesdir}/%{name}-%{version}/php
%{_examplesdir}/%{name}-%{version}/python

%files -n java-flixengine
%defattr(644,root,root,755)
%{_libdir}/libflixengine2_jni.so
%{_javadir}/flixengine2.jar

%files -n perl-flixengine
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/On2
%{perl_vendorarch}/On2/flixengine2.pm
%dir %{perl_vendorarch}/auto/On2
%dir %{perl_vendorarch}/auto/On2/flixengine2
%{perl_vendorarch}/auto/On2/flixengine2/flixengine2.bs
%attr(755,root,root) %{perl_vendorarch}/auto/On2/flixengine2/flixengine2.so

%files -n php-flixengine
%defattr(644,root,root,755)
%{extensionsdir}/flixengine2.so
%{_libdir}/flixengine2.php

%files -n python-flixengine
%defattr(644,root,root,755)
%{py_sitedir}/_flixengine2.so
%{py_sitedir}/flixengine2.pyc
%{py_sitedir}/flixengine2.pyo
