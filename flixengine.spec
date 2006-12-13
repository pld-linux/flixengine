Summary:	On2 Flix Engine
Name:		flixengine
Version:	8.0.7.0
Release:	0.2
License:	not distributable
Group:		Applications
# download demo from http://flix.on2.com/demos/
Source0:	%{name}linuxdemo.tar.gz
# Source0-md5:	ea7d3a0efaf08611aad9374259015d71
NoSource:	0
URL:		http://www.on2.com/developer/flix-engine-sdk
BuildRequires:	bash
BuildRequires:	ffmpeg-libs
BuildRequires:	jre
BuildRequires:	lame-libs
BuildRequires:	perl-base
BuildRequires:	php-devel
BuildRequires:	python
Requires:	%{name}-libs = %{version}-%{release}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
s,^initchk$,inittype=sysv1; INITDIR=$RPM_BUILD_ROOT/etc/rc.d/init.d,
s,clear 2>\$nullout,#&,
' install.sh

%build
cd .flix-engine-installation-files

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

./install.sh \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--mandir=$RPM_BUILD_ROOT%{_mandir} \
	--pidfile=/var/run/flixd.pid \
	--authdir=$RPM_BUILD_ROOT/var/lib/on2 \
	--just-install \
	--offline \
	--yesireadtheon2license \
	--no-compile \
	--no-init \
	--noprereqlibs \
	--install-all

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
if [ -s on2_host_info ]; then
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
%{_datadir}/on2

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libflixengine2.so.*.*
%attr(755,root,root) %{_libdir}/libflixengine2_core.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/flixengine2
%{_prefix}/src/flixmodules
