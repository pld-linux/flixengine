#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
%bcond_without		python	# do not build Python bindings
%bcond_without		java	# do not build Java bindings
%bcond_with	tests		# perform "make test". needs running flixd on localhost
#
%ifarch %{x8664}
%undefine	with_python
%undefine	with_java
%endif
#
%include	/usr/lib/rpm/macros.perl
Summary:	On2 Flix Engine
Summary(pl):	Silnik On2 Flix
Name:		flixengine
Version:	8.0.7.1
Release:	0.8
License:	not distributable
Group:		Applications
# download demo from http://flix.on2.com/demos/
Source0:	%{name}linuxdemo.tar.gz
# NoSource0-md5:	fb7cc89ce2689d3c43434291620cfd0f
NoSource:	0
Source1:	%{name}.init
Patch0:		%{name}-libdir.patch
URL:		http://www.on2.com/developer/flix-engine-sdk
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
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	portmap
Requires:	rc-scripts
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME: FHS 2.x violation
%define		_libexecdir	%{_prefix}/libexec

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

%description -l pl
Silnik On2 Flix Engine udostêpnia wiele spo¶ród mo¿liwo¶ci kodowania
filmów Flash 8 wiod±cego kodera On2 Flix Pro w postaci potê¿nego SDK.

Silnik pozwala wykorzystywaæ mo¿liwo¶ci i wydajno¶æ filmów Flash z
kodowaniem On2 VP6 w intranecie, na stronie WWW i w innych
zastosowaniach serwerowych, z zachowaniem kana³u alpha na wyj¶ciu
obrazu i innymi opcjami.

G³ówn± cech± silnika On2 Flix Engine 8 jest obs³uga filmów Adobe Flash
8 z kodekiem On2 VP6 oraz wyj¶ciem obrazu FLV, które mo¿na odtwarzaæ
bezpo¶rednio w odtwarzaczu Flash, przekazywaæ strumieniem poprzez
Adobe Flash Media Server lub importowaæ do Flash Studio. Nowe wyj¶cie
FLV jest tak¿e w pe³ni zgodne z formatem metadanych FLV i standardami
Adobe Flash Playera.

%package libs
Summary:	Shared libraries for On2 Flix Engine
Summary(pl):	Biblioteki wspó³dzielone silnika On2 Flix
Group:		Libraries

%description libs
Shared libraries for On2 Flix Engine.

%description libs -l pl
Biblioteki wspó³dzielone silnika On2 Flix.

%package devel
Summary:	Header files for On2 Flix Engine library
Summary(pl):	Pliki nag³ówkowe biblioteki silnika On2 Flix
Group:		Development/Libraries

%description devel
Header files for On2 Flix Engine library.

%description devel -l pl
Pliki nag³ówkowe biblioteki silnika On2 Flix.

%package -n java-flixengine
Summary:	Java bindings for On2 Flix Engine
Summary(pl):	Wi±zania Javy dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n java-flixengine
Java bindings for On2 Flix Engine.

%description -n java-flixengine -l pl
Wi±zania Javy dla silnika On2 Flix.

%package -n perl-flixengine
Summary:	Perl bindings for On2 Flix Engine
Summary(pl):	Wi±zania perla dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n perl-flixengine
Perl bindings for On2 Flix Engine.

%description -n perl-flixengine -l pl
Wi±zania perla dla silnika On2 Flix.

%package -n php-flixengine
Summary:	PHP bindings for On2 Flix Engine
Summary(pl):	Wi±zania PHP dla silnika On2 Flix
%{?requires_php_extension}
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	php-common >= 4:5.0.4

%description -n php-flixengine
PHP bindings for On2 Flix Engine.

%description -n php-flixengine -l pl
Wi±zania PHP dla silnika On2 Flix.

%package -n python-flixengine
Summary:	Python bindings for On2 Flix Engine
Summary(pl):	Wi±zania Pythona dla silnika On2 Flix
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-flixengine
Python bindings for On2 Flix Engine.

%description -n python-flixengine -l pl
Wi±zania Pythona dla silnika On2 Flix.

%package docs
Summary:	HTML Documentation for On2 Flix Engine
Group:		Documentation

%description docs
HTML Documentation for On2 Flix Engine

%prep
%setup -q -n flix-engine-installer-linux-%{version}_DEMO
bin=flix-engine-installer-linux-%{version}_DEMO.bin
tar=flix-engine-linux-%{version}_DEMO.tar.gz

OFFSET=$( awk -F= '/OFFSET=/{print $2; exit}' $bin)
dd bs=8 if=$bin of=$tar skip=$OFFSET
%{__tar} zxf $tar

%patch0 -p1

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

%ifarch %{x8664}
export LD_LIBRARY_PATH=$(pwd)/testing/lib64
ldconfig -n testing/lib64
%else
export LD_LIBRARY_PATH=$(pwd)/flixlibs
ldconfig -n flixlibs
%endif
export LIBRARY_PATH=$LD_LIBRARY_PATH

# PHP
%{__make} -C flixphp \
	LIBDIR=$LIBRARY_PATH \
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

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/flixd

cd .flix-engine-installation-files

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
extension=flixengine2.so
EOF

# Perl
cd flixperl
%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{perl_vendorarch}/auto/On2/flixengine2/.packlist
cd ..

%if %{with python}
cd flixpython
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean
cd ..
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
%endif

%ifarch %{x8664}
cp -a testing/lib64/libflixengine2.so* $RPM_BUILD_ROOT%{_libdir}
%endif

# do not put hardware fingerprint to rpm package
> $RPM_BUILD_ROOT/var/lib/on2/hostinfo

# use poldek -e
rm -f $RPM_BUILD_ROOT%{_sbindir}/flix-engine-uninstall.sh

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
/sbin/chkconfig --add flixd
if [ ! -s /var/lib/on2/hostinfo ]; then
	%{_sbindir}/on2_host_info > /var/lib/on2/hostinfo
%banner -e %{name} <<EOF
To register your copy of flixd invoke:
# %{_sbindir}/lget -u '<username>' -s '<serial>' -i /var/lib/on2/hostinfo -o /var/lib/on2/on2product.lic -a 'On2FlixEngine/%{version}_DEMO (%(uname -o))'
EOF
fi
%service flixd restart

%preun
if [ "$1" = "0" ]; then
	%service -q flixd stop
	/sbin/chkconfig --del flixd
fi

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
%attr(755,root,root) %{_sbindir}/flixd
%attr(755,root,root) %{_sbindir}/lget
%attr(755,root,root) %{_sbindir}/on2_host_info
%attr(754,root,root) /etc/rc.d/init.d/flixd
%{_mandir}/man8/flixd.8*
%dir /var/lib/on2
%config(noreplace) %verify(not md5 mtime size) /var/lib/on2/hostinfo
# TODO: FHS fix
%dir %{_libexecdir}
%dir %{_libexecdir}/on2
%dir %{_libexecdir}/on2/flixengine
%attr(755,root,root) %{_libexecdir}/on2/flixengine/mencoder

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/libflixengine2.so.*.*
%attr(755,root,root) %{_prefix}/lib/libflixengine2_core.so.*.*
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libflixengine2.so.*.*
%endif
%dir %{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/lib/libflixengine2.so
%attr(755,root,root) %{_prefix}/lib/libflixengine2_core.so
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/libflixengine2.so
%endif
%{_includedir}/flixengine2
%{_examplesdir}/%{name}-%{version}/c

%if %{with java}
%files -n java-flixengine
%defattr(644,root,root,755)
%doc %{_docdir}/on2/flixengine/javadoc
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

%files docs
%defattr(644,root,root,755)
%doc %{_docdir}/on2
