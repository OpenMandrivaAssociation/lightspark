Name: lightspark
Version: 0.4.4
Release: %mkrel 1
Summary: An alternative Flash Player implementation
Group: Networking/WWW
License: LGPLv3+
URL: http://lightspark.sourceforge.net
Source: http://edge.launchpad.net/lightspark/trunk/%name-%version/+download/%name-%version.tar.gz
Patch0: lightspark-0.4.3-cmakelists.patch
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

%package mozilla-plugin
Summary: Mozilla compatible plugin for %{name}
Group: Networking/WWW
Suggests: gnash
Conflicts: gnash-firefox-plugin

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}

%prep
%setup -q
#patch0 -p1

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

#remove devel file from package
rm -f %{buildroot}%{_libdir}/%{name}/lib%{name}.so

#(eandry) move libs where binary want it to be (need a real fix)
mv %{buildroot}%{_libdir}/%{name}/lib%{name}.so* %{buildroot}%{_libdir}/

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER ChangeLog
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/man/man1/%{name}.1.*
%{_libdir}/lib%{name}.so*

%files mozilla-plugin
%defattr(-,root,root,-)
%{_libdir}/mozilla/plugins/lib%{name}plugin.so
