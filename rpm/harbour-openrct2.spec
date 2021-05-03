#
# spec file for package openrct2
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define lib_suffix %{nil}
%define _unpackaged_files_terminate_build 0
%ifarch x86_64
  %define lib_suffix 64
%endif
%define title_version 0.1.2
%define title_version_url %{title_version}c
%define objects_version 1.0.20
Name:           harbour-openrct2
Version:        0.3.3
Release:        0
Summary:        An open source re-implementation of Roller Coaster Tycoon 2
License:        GPL-3.0
Group:          Amusements/Games/Strategy/Other
URL:            https://openrct2.io/
Source0:        https://github.com/OpenRCT2/OpenRCT2/archive/v%{version}/OpenRCT2-%{version}.tar.gz
#Source1:        https://github.com/OpenRCT2/title-sequences/archive/v%%{title_version_url}/title-sequences-%%{title_version_url}.tar.gz
#Source2:        https://github.com/OpenRCT2/objects/archive/v%%{objects_version}.tar.gz#/objects-%%{objects_version}.tar.gz
# https://github.com/OpenRCT2/OpenRCT2/issues/4401#issuecomment-511570036
# PATCH-FIX-OPENSUSE no-werror.patch -- Do not use werror, as wno-clobbered does not work
#Patch0:         no-werror.patch
# Autotools related packages are required by speexdsp
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
# Required by OpenRCT2
BuildRequires: git
BuildRequires:  cmake >= 3.9
#BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
#BuildRequires:  hicolor-icon-theme
#BuildRequires:  nlohmann_json-devel
BuildRequires:  pkgconfig 
BuildRequires:  shared-mime-info
#BuildRequires:  update-desktop-files
BuildRequires:  zip
#BuildRequires:  pkgconfig(duktape)
#BuildRequires:  pkgconfig(fontconfig)
#BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(icu-uc) >= 59.0
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libpng16)
BuildRequires:  pkgconfig(openssl) >= 1.0.0
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(zlib)
Recommends:     (kdialog or zenity)
# For patching
BuildRequires:  chrpath

%description
An open source clone of RollerCoaster Tycoon 2
that depends on the original game assets. On first
game start it will create a ~/.config/OpenRCT2/config.ini file
where the game_path = "" setting has to be set to a directory
into which the original game has been installed to.

%prep
%autosetup -n OpenRCT2-%{version} 
#-a 1 -a 2
#%patch0 -p1

# Remove build time references so build-compare can do its work
sed -i "s/__DATE__/\"openSUSE\"/" src/openrct2/Version.h
sed -i "s/__TIME__/\"Build Service\"/" src/openrct2/Version.h

%build
# %%cmake -DDOWNLOAD_TITLE_SEQUENCES=OFF -DDOWNLOAD_OBJECTS=OFF -DENABLE_SCRIPTING=OFF \
	#-DENABLE_DOWNLOAD_MISSING_LIBS=ON -DDISABLE_OPENGL=ON

%cmake -DENABLE_SCRIPTING=OFF -DENABLE_DOWNLOAD_MISSING_LIBS=ON -DDISABLE_OPENGL=ON \
	-DCMAKE_INSTALL_RPATH=%{_datadir}/%{name}/lib -DORCT2_RESOURCE_DIR="%{_datadir}/%{name}"
%make_build all
# libopenrct2 is not installed when openrct2 is called by make, so set the LD_LIBRARY_PATH
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$(dirname $(find . -name libopenrct2.so))"
%make_build g2
# %%cmake changes directory into "build"
strip openrct2
strip libopenrct2.so
cd ..



%install
%make_install

# Correct desktop files
sed -i "s|Exec=openrct2|Exec=env LD_LIBRARY_PATH=/usr/share/harbour-openrct2/lib harbour-openrct2 --openrct2-data-path=/usr/share/harbour-openrct2|" %{buildroot}%{_datadir}/applications/*.desktop
sed -i "s/Icon=openrct2/Icon=harbour-openrct2/" %{buildroot}%{_datadir}/applications/*.desktop

# find '%%{buildroot}%%{_datadir}/%{name}' -type f -exec chmod 644 \{\} \;

# We do that in the correct docdir in the files section.
rm -rf %{buildroot}%{_datadir}/doc
rm -rf %{buildroot}%{_datadir}/man

# %%fdupes %{buildroot}%{_datadir}/%{name}

# Move files to correct locations
mkdir -p %{buildroot}/%{_datadir}/%{name}/bin
mkdir -p %{buildroot}/%{_datadir}/%{name}/lib
mv %{buildroot}%{_datadir}/openrct2/* %{buildroot}%{_datadir}/%{name}/
mv %{buildroot}%{_libdir}/libopenrct2.so %{buildroot}/%{_datadir}/%{name}/lib/libopenrct2.so
mv %{buildroot}%{_bindir}/openrct2-cli %{buildroot}%{_datadir}/%{name}/bin/openrct2-cli
mv %{buildroot}%{_bindir}/openrct2 %{buildroot}%{_bindir}/harbour-openrct2

# Rename icons
pushd %{buildroot}%{_datadir}/icons/hicolor
for dir in *; do
	pushd $dir/apps
	mv openrct2.png harbour-openrct2.png || true
	mv openrct2.svg harbour-openrct2.svg || true
	popd
done
popd

# Move desktop files
mv %{buildroot}%{_datadir}/applications/openrct2.desktop %{buildroot}%{_datadir}/applications/harbour-openrct2.desktop
mv %{buildroot}%{_datadir}/applications/openrct2-savegame.desktop %{buildroot}%{_datadir}/applications/harbour-openrct2-savegame.desktop
mv %{buildroot}%{_datadir}/applications/openrct2-scenario.desktop %{buildroot}%{_datadir}/applications/harbour-openrct2-scenario.desktop
mv %{buildroot}%{_datadir}/applications/openrct2-uri.desktop %{buildroot}%{_datadir}/applications/harbour-openrct2-uri.desktop

%files
%{_bindir}/harbour-openrct2
%{_datadir}/%{name}/bin/openrct2-cli
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*.desktop
%dir %{_datadir}/metainfo/
%{_datadir}/metainfo/openrct2.appdata.xml
%{_datadir}/mime/packages/openrct2.xml

%changelog
