%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name} 

Summary:	An alternative Flash Player implementation
Name:		lightspark
Version:	0.8.1
Release:	1
Group:		Networking/WWW
License:	LGPLv3+
URL:		http://lightspark.github.io/
Source0:	https://github.com/lightspark/lightspark/archive/%{name}-%{version}.tar.gz
# Droped patch, fixed by upstream. (penguin)
#Patch1:		lightspark-0.8.0-fix-compilation-with-llvm-5.0.patch
# Temporary disable patch, to see if it fixed by upstream. (penguin)
#Patch2:     lightspark-fix-template-codec.patch
BuildRequires:	cmake
BuildRequires:	nasm
BuildRequires:	boost-devel
BuildRequires:	llvm-devel
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(ftgl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxml++-2.6)
BuildRequires:	pkgconfig(libxul)
BuildRequires:	pkgconfig(sdl)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:	pkgconfig(SDL2_mixer)
BuildRequires:	pkgconfig(gtk+-2.0)
Requires:	fonts-ttf-liberation
Suggests:	%{name}-pulse

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
Summary:	%{name} libraries
Group:		System/Libraries

%description -n %{libname}
This is the libraries used by %{name}.

%package -n %{devname}
Summary:	Development libraries for %{name}
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for the %{name} libraries.

%package mozilla-plugin
Summary:	Mozilla compatible plugin for %{name}
Group:		Networking/WWW
Suggests:	gnash
Suggests:	%{name}-pulse
Conflicts:	gnash-firefox-plugin

%description mozilla-plugin
This is the Mozilla compatible plugin for %{name}

%package        ppapi-plugin
Summary:        PPAPI compatible plugin for %{name}
Group:          Networking/WWW
 	
%description    ppapi-plugin
This is the PPAPI compatible plugin for %{name}.

%prep
%setup -qn %{name}-%{name}-%{version}
#patch1 -p1
#patch2 -p0


%build
%define _disable_ld_no_undefined 1
%cmake \
    -DCOMPILE_PLUGIN=1 \
    -DPLUGIN_DIRECTORY="%{_libdir}/mozilla/plugins/" \
    -DENABLE_SOUND=1 \
    -DGNASH_EXE_PATH="%{_bindir}/gnash"

%make

%install
%makeinstall_std -C build

#(eandry) tell lightspark where the libs are
install -d -m 0755  %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/lightspark" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/lightspark.conf

install -Dpm 644 media/%{name}-logo.svg %{buildroot}%{_datadir}/%{name}

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING COPYING.LESSER ChangeLog
%config(noreplace) %{_sysconfdir}/xdg/lightspark.conf
%{_bindir}/%{name}
%{_bindir}/tightspark
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}.1*

%files -n %{libname}
%config %{_sysconfdir}/ld.so.conf.d/lightspark.conf
%{_libdir}/%{name}/lib%{name}.so.*

%files -n %{devname}
%{_libdir}/%{name}/lib%{name}.so

%files mozilla-plugin
%{_libdir}/mozilla/plugins/lib%{name}plugin.so

%files ppapi-plugin
%{_libdir}/PepperFlash/

