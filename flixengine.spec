#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_without	python		# do not build Python bindings
%bcond_without	java		# do not build Java bindings
%bcond_with	tests		# perform "make test". needs running flixd on localhost
%bcond_without	demo	# use production tarball (you need one too:))
#
%ifarch %{x8664}
%undefine	with_python
%undefine	with_java
%endif
#
%define		full_version	%{version}%{?with_demo:_DEMO}%{?_extra}
%define		_extra	%{nil}
#
%include	/usr/lib/rpm/macros.perl
Summary:	On2 Flix Engine
Summary(pl.UTF-8):	Silnik On2 Flix
Name:		flixengine
Version:	8.0.10.1
Release:	0.2
License:	(probably) not distributable
Group:		Applications
# download demo from http://flix.on2.com/demos/
# check for newer versions at http://flix.on2.com/flix/download/
# Source0Download:	http://flix.on2.com/demos/flixenginelinuxdemo.tar.gz
%if %{with demo}
Source0:	%{name}linuxdemo-%{version}.tar.gz
# NoSource0-md5:	3d0accb19f6d9dcd6ea2cd139a150d9e
NoSource:	0
%endif
%if %{without demo}
# Source1Download:	http://flix.on2.com/flix/download/flix-engine-installer-linux-%{version}.tar.gz
Source1:	flix-engine-installer-linux-%{version}%{?_extra}.tar.gz
# NoSource1-md5:	ecf91acf067775e27059977b7a5a8da7
NoSource:	1
%endif
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Patch0:		%{name}-libdir.patch
Patch1:		%{name}-phploader.patch
URL:		http://www.on2.com/index.php?474
BuildRequires:	bash
%{?with_java:BuildRequires:	jre}
BuildRequires:	perl-base
BuildRequires:	php-devel
%{?with_python:BuildRequires:	python}
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.344
%if %{with autodeps}
BuildRequires:	ffmpeg-libs
BuildRequires:	lame-libs
%endif
Requires(post,postun):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	portmap
Requires:	rc-scripts >= 0.4.1.5
Provides:	group(flixd)
Provides:	user(flixd)
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# should not provide such deps
%define		_noautoprov libavutil.so.49 libavformat.so.50 libavcodec.so.51
# need to provide it for flixd, but we don't want package name dep here
%define		_noautoreq %{_noautoprov}

%define		_sysconfdir		/etc/on2

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

%description -l pl.UTF-8
Silnik On2 Flix Engine udostępnia wiele spośród możliwości
kodowania filmów Flash 8 wiodącego kodera On2 Flix Pro w postaci
potężnego SDK.

Silnik pozwala wykorzystywać możliwości i wydajność filmów Flash
z kodowaniem On2 VP6 w intranecie, na stronie WWW i w innych
zastosowaniach serwerowych, z zachowaniem kanału alpha na wyjściu
obrazu i innymi opcjami.

Główną cechą silnika On2 Flix Engine 8 jest obsługa filmów Adobe
Flash 8 z kodekiem On2 VP6 oraz wyjściem obrazu FLV, które można
odtwarzać bezpośrednio w odtwarzaczu Flash, przekazywać strumieniem
poprzez Adobe Flash Media Server lub importować do Flash Studio. Nowe
wyjście FLV jest także w pełni zgodne z formatem metadanych FLV i
standardami Adobe Flash Playera.

%package libs
Summary:	Shared libraries for On2 Flix Engine
Summary(pl.UTF-8):	Biblioteki współdzielone silnika On2 Flix
Group:		Libraries

%description libs
Shared libraries for On2 Flix Engine.

%description libs -l pl.UTF-8
Biblioteki współdzielone silnika On2 Flix.

%package devel
Summary:	Header files for On2 Flix Engine library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki silnika On2 Flix
Group:		Development/Libraries

%description devel
Header files for On2 Flix Engine library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki silnika On2 Flix.

%package -n java-flixengine
Summary:	Java bindings for On2 Flix Engine
Summary(pl.UTF-8):	Wiązania Javy dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	jpackage-utils

%description -n java-flixengine
Java bindings for On2 Flix Engine.

%description -n java-flixengine -l pl.UTF-8
Wiązania Javy dla silnika On2 Flix.

%package -n perl-flixengine
Summary:	Perl bindings for On2 Flix Engine
Summary(pl.UTF-8):	Wiązania perla dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-flixengine
Perl bindings for On2 Flix Engine.

%description -n perl-flixengine -l pl.UTF-8
Wiązania perla dla silnika On2 Flix.

%package -n php-flixengine
Summary:	PHP bindings for On2 Flix Engine
Summary(pl.UTF-8):	Wiązania PHP dla silnika On2 Flix
%{?requires_php_extension}
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	php-common >= 4:5.0.4

%description -n php-flixengine
PHP bindings for On2 Flix Engine.

%description -n php-flixengine -l pl.UTF-8
Wiązania PHP dla silnika On2 Flix.

%package -n python-flixengine
Summary:	Python bindings for On2 Flix Engine
Summary(pl.UTF-8):	Wiązania Pythona dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-flixengine
Python bindings for On2 Flix Engine.

%description -n python-flixengine -l pl.UTF-8
Wiązania Pythona dla silnika On2 Flix.

%package apidocs
Summary:	HTML API Documentation for On2 Flix Engine
Summary(pl.UTF-8):	Dokumentacja HTML API dla silnika On2 Flix
Group:		Documentation
Obsoletes:	flixengine-docs

%description apidocs
HTML API Documentation for On2 Flix Engine.

%description apidocs -l pl.UTF-8
Dokumentacja HTML API dla silnika On2 Flix.

%prep
%setup -q -T -b %{?with_demo:0}%{!?with_demo:1} -n flix-engine-installer-linux-%{full_version}
bin=flix-engine-installer-linux-%{full_version}.bin
tar=flix-engine-linux-%{full_version}.tar.gz

OFFSET=$( awk -F= '/OFFSET=/{print $2; exit}' $bin)
dd bs=8 if=$bin of=$tar skip=$OFFSET
%{__tar} zxf $tar

%patch0 -p1
%patch1 -p1

%{__sed} -ne '/## FUNCTIONS common/,/## END - common function/p' $bin > functions.sh
cat <<'EOF' > install.sh
#!/bin/bash
export VERSION=%{full_version}
%{?with_demo:export FLIXENGINEDEMO=1}
export nullout=/dev/null
export tempdir=%{_builddir}/flix-engine-installer-linux-%{full_version}

. $(dirname "$0")/functions.sh
cd .flix-engine-installation-files

export -f getinput inset ynanswer
instlog=install.log
./install.sh "$@" | tee -i $instlog
if [ -f "$instlog" ]; then
	echo "Local system info:" >>$instlog
	uname -a 2>/dev/null >>$instlog
	head /etc/*version* 2>/dev/null >>$instlog
	head /etc/*release* 2>/dev/null >>$instlog
	cat /proc/cpuinfo 2>/dev/null >>$instlog
	/lib/ld-linux.so.2 /lib/libc.so.6 2>/dev/null >>$instlog
	echo "---" 2>/dev/null >>$instlog
	/lib/ld-linux.so.2 /lib32/libc.so.6 2>/dev/null >>$instlog
	echo "---" 2>/dev/null >>$instlog
	/lib/libc.so.6 2>/dev/null >>$instlog
	echo "---" 2>/dev/null >>$instlog
	file /lib/libc.so.6 2>/dev/null >>$instlog
	echo "---" 2>/dev/null >>$instlog
	/sbin/ifconfig -a 2>/dev/null >>$instlog

	echo "A log of this installation can be found here:"
	echo "  $instlog"
	echo
fi
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

# remove backups from patching as we use globs to package files to buildroot
find flixsamples '(' -name '*~' -o -name '*.orig' ')' | xargs -r rm -v

%build
cd .flix-engine-installation-files
PWD=$(pwd)

ln -snf flixhdrs flixengine2
export C_INCLUDE_PATH=$PWD

%ifarch %{x8664}
export LD_LIBRARY_PATH=$PWD/testing/lib64
ldconfig -n testing/lib64
%else
export LD_LIBRARY_PATH=$PWD/flixlibs
ldconfig -n flixlibs
%endif
export LIBRARY_PATH=$LD_LIBRARY_PATH

# PHP
%{__make} -C flixphp \
	CC="%{__cc}" \
	-f target.mk

# Perl
cd flixperl
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"
%{?with_tests:%{__make} test}
cd ..

%if %{with python}
cd flixpython
%{__python} setup.py build
cd ..
%endif

%if %{with java}
%{__make} -C flixjava \
	CC="%{__cc}" \
	-f target.mk
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

./install.sh \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	--mencoderbin=$RPM_BUILD_ROOT%{_bindir} \
	--flixsamples=$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	--pidfile=$RPM_BUILD_ROOT/var/run/flixd/flixd.pid \
	--authdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	--just-install \
	--offline \
	--yesireadtheon2license \
	--no-compile \
	--no-modules \
	--no-init \
	--noprereqlibs

rm -f $RPM_BUILD_ROOT/etc/rc.d/init.d/flixengine
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/flixd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/flixd

# mencoder-flixengine searches for codecs from /usr/lib/win32 and there's no
# way to override it by commandline arg or env var.
ln -s codecs $RPM_BUILD_ROOT%{_prefix}/lib/win32

cd .flix-engine-installation-files
install lget on2_host_info $RPM_BUILD_ROOT%{_sbindir}

# symlink without buildroot
ln -snf %{_docdir}/on2/flixengine/html/c/cli.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/c/README-cli.html

# install bindings
# PHP
%{__make} -C flixphp \
	install \
	PHPINST=%{php_extensiondir} \
	DESTDIR=$RPM_BUILD_ROOT \
	-f target.mk
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/flixengine.ini
; Enable flixengine extension module
;extension=flixengine2.so
EOF
# symlink without buildroot
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/php
ln -snf %{_docdir}/on2/flixengine/html/phpcgi.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/php/README-cgi.html
ln -snf %{_docdir}/on2/flixengine/html/phpcli.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/php/README-cli.html

# Perl
cd flixperl
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/On2/flixengine2/.packlist
cd ..
# symlink without buildroot
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/perl
ln -snf %{_docdir}/on2/flixengine/html/perlcgi.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/perl/README-cgi.html
ln -snf %{_docdir}/on2/flixengine/html/perlcli.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/perl/README-cli.html

%if %{with python}
cd flixpython
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean
cd ..
# symlink without buildroot
ln -snf %{_docdir}/on2/flixengine/html/pythoncgi.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/python/README-cgi.html
ln -snf %{_docdir}/on2/flixengine/html/pythoncli.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/python/README-cli.html
%endif

rm -f $RPM_BUILD_ROOT%{_docdir}/on2/flixengine/javadoc
%if %{with java}
%{__make} -C flixjava \
	SOINST=$RPM_BUILD_ROOT%{_libdir} \
	JARINST=$RPM_BUILD_ROOT%{_javadir} \
	install \
	-f target.mk

# symlink without buildroot
ln -snf %{_prefix}/src/flixmodules/flixjava/doc $RPM_BUILD_ROOT%{_docdir}/on2/flixengine/javadoc
ln -snf %{_docdir}/on2/flixengine/html/javacli.html $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/java/README-cli.html
%endif

%ifarch %{x8664}
cp -a testing/lib64/libflixengine2.so* $RPM_BUILD_ROOT%{_libdir}
# flixd linked statically and other libs are 64 bit
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/libflixengine2*.so*
%endif

# we have already newer soname for libavformat.so in ffmpeg-libs
# copy from bundled ones.
install supportlibs/libavformat.so.51.12.2 $RPM_BUILD_ROOT%{_prefix}/lib
install supportlibs/libavcodec.so.51.41.0 $RPM_BUILD_ROOT%{_prefix}/lib
install supportlibs/libavutil.so.49.5.0 $RPM_BUILD_ROOT%{_prefix}/lib

# avoid collision from mplayer package
mv $RPM_BUILD_ROOT%{_bindir}/mencoder{,-flixengine}

# do not put hardware fingerprint to rpm package
> $RPM_BUILD_ROOT%{_sysconfdir}/hostinfo
touch $RPM_BUILD_ROOT%{_sysconfdir}/flixengine.lic
install -d $RPM_BUILD_ROOT/var/run/flixd
install -d $RPM_BUILD_ROOT/var/log
touch $RPM_BUILD_ROOT/var/log/flixd.log

# use poldek -e
rm -f $RPM_BUILD_ROOT%{_sbindir}/flix-engine-uninstall.sh

# make it somewhat easier to acquire license registration
install -d $RPM_BUILD_ROOT%{_sysconfdir}
cat > $RPM_BUILD_ROOT%{_sysconfdir}/flixd-license.conf <<'EOF'
FLIX_USERNAME='<username>'
FLIX_SERIAL='<serial>'
EOF

install -d $RPM_BUILD_ROOT%{_sbindir}
cat > $RPM_BUILD_ROOT%{_sbindir}/flixd-license-get <<'EOF'
#!/bin/sh
set -e

. %{_sysconfdir}/flixd-license.conf
if [ -z "$FLIX_USERNAME" -o -z "$FLIX_SERIAL" ]; then
	echo >&2 "Please fill FLIX_USERNAME and FLIX_SERIAL!"
	exit 1
fi

%{_sbindir}/lget -u "$FLIX_USERNAME" -s "$FLIX_SERIAL" -i %{_sysconfdir}/hostinfo -o %{_sysconfdir}/flixengine.lic -a 'On2FlixEngine/%{full_version} (%(uname -o))'
echo ""
echo "Serial registered and saved into %{_sysconfdir}/flixengine.lic"
echo ""
echo "Run \"/sbin/service flixd start\" to start flixd"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 179 flixd
%useradd -u 179 -g flixd -c "On2 Flixd" flixd

%post
/sbin/ldconfig
/sbin/chkconfig --add flixd
if [ ! -f /var/log/flixd.log ]; then
	touch /var/log/flixd.log
	chown root:flixd /var/log/flixd.log
	chmod 660 /var/log/flixd.log
fi
if [ ! -s %{_sysconfdir}/hostinfo ]; then
	%{_sbindir}/on2_host_info > %{_sysconfdir}/hostinfo
%banner -e %{name} <<EOF
Put your username and serial key to %{_sysconfdir}/flixd-license.conf
and invoke:
%{_sbindir}/flixd-license-get

You can register evaluation demo at <http://flix.on2.com/demos/>.
EOF
fi
%service flixd restart

%preun
if [ "$1" = "0" ]; then
	%service -q flixd stop
	/sbin/chkconfig --del flixd
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%userremove flixd
	%groupremove flixd
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post -n php-flixengine
%php_webserver_restart

%postun -n php-flixengine
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc doc/*
%{?with_java:%exclude %{_docdir}/on2/flixengine/javadoc}
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flixd-license.conf
%attr(640,root,flixd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/hostinfo
%attr(640,root,flixd) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/flixengine.lic
%attr(755,root,root) %{_prefix}/lib/libavformat.so.*.*.*
%attr(755,root,root) %{_prefix}/lib/libavcodec.so.*.*.*
%attr(755,root,root) %{_prefix}/lib/libavutil.so.*.*.*
%attr(755,root,root) %{_sbindir}/flixd
%attr(755,root,root) %{_sbindir}/flixd-license-get
%attr(755,root,root) %{_sbindir}/lget
%attr(755,root,root) %{_sbindir}/on2_host_info
%attr(754,root,root) /etc/rc.d/init.d/flixd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/flixd
%{_prefix}/lib/win32

%{_mandir}/man8/flixd.8*
%dir %attr(771,root,flixd) /var/run/flixd
%ghost %attr(660,root,flixd) /var/log/flixd.log
%attr(755,root,root) %{_bindir}/mencoder-flixengine

%files libs
%defattr(644,root,root,755)
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libflixengine2.so.*.*
%else
%attr(755,root,root) %{_libdir}/libflixengine2.so.*.*
%attr(755,root,root) %{_libdir}/libflixengine2_core.so.*.*
%endif
%dir %{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libflixengine2.so
%else
%attr(755,root,root) %{_libdir}/libflixengine2.so
%attr(755,root,root) %{_libdir}/libflixengine2_core.so
%endif
%{_includedir}/flixengine2
%{_examplesdir}/%{name}-%{version}/c

%if %{with java}
%files -n java-flixengine
%defattr(644,root,root,755)
%doc %{_docdir}/on2/flixengine/javadoc
# perhaps these should be:
# /usr/%{_lib}/jvm/java-sun-1.6.0/jre/lib/%{arch}/libflixengine2_jni.so
# /usr/%{_lib}/jvm/java-sun-1.6.0/jre/lib/ext/flixengine2.jar
%attr(755,root,root) %{_libdir}/libflixengine2_jni.so
%{_javadir}/flixengine2.jar
%{_examplesdir}/%{name}-%{version}/java
%endif

%files -n perl-flixengine
%defattr(644,root,root,755)
%dir %{perl_vendorarch}/On2
%{perl_vendorarch}/On2/flixengine2.pm
%dir %{perl_vendorarch}/auto/On2
%dir %{perl_vendorarch}/auto/On2/flixengine2
%{perl_vendorarch}/auto/On2/flixengine2/flixengine2.bs
%attr(755,root,root) %{perl_vendorarch}/auto/On2/flixengine2/flixengine2.so
%{_examplesdir}/%{name}-%{version}/perl

%files -n php-flixengine
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/flixengine.ini
%attr(755,root,root) %{php_extensiondir}/flixengine2.so
%{_prefix}/lib/flixengine2.php
%{_examplesdir}/%{name}-%{version}/php

%if %{with python}
%files -n python-flixengine
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_flixengine2.so
%{py_sitedir}/flixengine2.pyc
%{py_sitedir}/flixengine2.pyo
%{_examplesdir}/%{name}-%{version}/python
%endif

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/on2
