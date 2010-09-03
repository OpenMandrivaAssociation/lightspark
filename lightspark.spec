%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname -d %{name} 

Name: lightspark
Version: 0.4.4.1
Release: %mkrel 1
Summary: An alternative Flash Player implementation
Group: Networking/WWW
License: LGPLv3+
URL: http://lightspark.sourceforge.net
Source: http://edge.launchpad.net/lightspark/trunk/%name-%version/+download/%name-%version.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: cmake
BuildRequires: llvm >= 2.7
BuildRequires: glew-devel >= 1.5.4
BuildRequires: ftgl-devel
BuildRequires: ffmpeg-devel
BuildRequires: nasm
BuildRequires: libSDL-devel
BuildRequires: gtkglext-devel
BuildRequires: pulseaudio-devel
BuildRequires: fontconfig-devel
BuildRequires: pcre-devel
BuildRequires: xulrunner-devel
BuildRequires: curl-devel
Requires: fonts-ttf-liberation

%description
Lightspark is a modern, free, open-source flash player implementation.
Lightspark features:

* JIT compilation of Actionscript to native x86 bytecode using LLVM
* Hardware accelerated rendering using OpenGL Shaders (GLSL)
* Very good and robust support for current-generation Actionscript 3
* A new, clean, codebase exploiting multithreading and optimized for 
modern hardware. Designed from scratch after the official Flash 
documentation was released.

%package -n %{libname}
Summary: %{name} libraries
Group: System/Libraries

%description -n %{libname}
This is the libraries used by %{name}.

%package -n %{develname}
Summary: Development libraries for %{name}
Group: Development/C++
Provides: %{name}-devel = %{version}-%{release}
Requires: %{libname} = %{version}-%{release}

%description -n %{develname}
Development files for the %{name} libraries.

%package mozilla-plugin
Summary: Mozilla compatible plugin for %{name}
Group: Networking/WWW
Suggests: gnash
Conflicts: gnash-firefox-plugin

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}

%prep
%setup -q

%build

%cmake -DCOMPILE_PLUGIN=1 \
       -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins/" \
       -DENABLE_SOUND=1 \
       -DGNASH_EXE_PATH="%{_bindir}/gnash" \
       -DCMAKE_BUILD_TYPE=Release
       
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

#(eandry) tell lightspark where the libs are
%__install -d -m 0755  %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/lightspark" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/lightspark.conf

install -Dpm 644 media/%{name}-ico.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dpm 644 media/%{name}-logo.svg %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_datadir}/applications
cat <<EOF >%{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=Lightspark
Comment=An alternative flash player
TryExec=lightspark
Exec=lightspark
Icon=lightspark
NoDisplay=true
Type=Application
Categories=GNOME;GTK;AudioVideo;Video;Player;
MimeType=application/x-shockwave-flash;application/futuresplash;
StartupNotify=true
EOF

%find_lang %name

%clean
rm -rf %{buildroot}

%files -f %name.lang
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER ChangeLog
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/man/man1/%{name}.1.*

%files -n %{libname}
%defattr(-,root,root)
%config %{_sysconfdir}/ld.so.conf.d/lightspark.conf
%{_libdir}/%{name}/lib%{name}.so*

%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/%{name}/lib%{name}.so

%files mozilla-plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/lib%{name}plugin.so
