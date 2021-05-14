Name:		flatbuffers
Summary:	cross platform serialization library
Version:	2.0.0
Release:	1%{?dist}
Group:		Development/Libraries
Packager:	Parichay Kapoor <pk.kapoor@samsung.com>
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.manifest

BuildRequires:	cmake
BuildRequires:	gcc-c++
BuildRequires:	sed
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
FlatBuffers is a cross platform serialization library architected for maximum
memory efficiency. It allows you to directly access serialized data without
parsing/unpacking it first, while still having great forwards/backwards
compatibility.

%package devel
Summary:	Development package to use flatbuffers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%description devel
This package provides headers and other miscellaneous files required to use flatbuffers.

%package python
Summary:	Python subpackage to use flatbuffers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:   python3-devel
%description python
This package provides flatbuffers python API.

%prep
%setup -q
cp %{SOURCE1} .

%build
export CFLAGS+=" -fno-lto"
export CXXFLAGS+=" -fno-lto"
pushd python
export VERSION="2.0.0"
%{_bindir}/python3 setup.py build
popd

# flatbuffers build occasionally fails when using -j${BUILD_THREADS} with an error similar to:
# /mnt/source/flatbuffers/flatbuffers-1.6.0/samples/sample_binary.cpp:19:17: error: 'MyGame' has not been declared
# /mnt/source/flatbuffers/flatbuffers-1.6.0/samples/sample_binary.cpp:19:25: error: 'Sample' is not a namespace-name
# ...
# Disabling build tests gets rid of this flakiness and makes the compilation faster.
%{cmake} \
    -DFLATBUFFERS_INSTALL=ON \
    -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
    -DCMAKE_POSITION_INDEPENDENT_CODE=TRUE \
    -DFLATBUFFERS_BUILD_TESTS=OFF \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DFB_CMAKE_DIR=%{_libdir}/cmake \
    -DCMAKE_BUILD_TYPE=Release .
%{__make} %{?_smp_mflags}

%install
%{__make} DESTDIR=%{?buildroot:%{buildroot}} install
install -D -m 644 packaging/%{name}.pc.in %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i 's#@version@#%{version}#g' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i 's#@libdir@#%{_libdir}#g' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
sed -i 's#@includedir@#%{_includedir}#g' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
mkdir -p %{buildroot}/%{python3_sitelib}/flatbuffers
pushd python
export VERSION="2.0.0"
%{_bindir}/python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
rm -r %{buildroot}/%{python3_sitelib}/*.egg-info
rm -r %{buildroot}/%{python3_sitelib}/flatbuffers/__pycache__
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.txt
%{_libdir}/libflatbuffers.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/flatc
%{_includedir}/flatbuffers
%{_libdir}/libflatbuffers.a
%{_libdir}/cmake/flatbuffers/*
%{_libdir}/libflatbuffers.so
%{_libdir}/pkgconfig/flatbuffers.pc

%files python
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.txt
%{python3_sitelib}/flatbuffers/

%changelog
* Thu May 13 2021 Gichan Jang <gichan2.jang@samsung.com>
- Release of 2.0.0

* Tue Sep 15 2020 Wook Song <wook16.song@samsung.com>
- Add the pkg-config file to the dev-kit package

* Mon Aug 03 2020 Geunsik Lim <geunsik.lim@samsung.com>
- Release of 1.12.0 to support Tensorflow-Lite 2.x

* Fri Nov 15 2019 Parichay kapoor <pk.kapoor@samsung.com>
- Release of 1.11.0
