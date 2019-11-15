Name:		  flatbuffers
Summary:	cross platform serialization library
Version:	1.11.0
Release:	1%{?dist}
Group:		Development/Libraries
Packager:	Parichay Kapoor <pk.kapoor@samsung.com>
License:	Apache-2.0
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.manifest

BuildRequires:	cmake
BuildRequires:	gcc-c++

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

%prep
%setup -q
cp %{SOURCE1} .

%build
%{cmake} \
    -DFLATBUFFERS_INSTALL=ON \
    -DFLATBUFFERS_BUILD_SHAREDLIB=ON \
    -DCMAKE_POSITION_INDEPENDENT_CODE=TRUE \
    -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_BINDIR=%{_bindir} \
    -DFB_CMAKE_DIR=%{_libdir}/cmake \
    -DCMAKE_BUILD_TYPE=Release .
%{__make} %{?_smp_mflags}

%check
make test

%install
%{__make} DESTDIR=%{?buildroot:%{buildroot}} install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.txt
%{_libdir}/libflatbuffers.so*

%files devel
%{_bindir}/flatc
%{_includedir}/flatbuffers
%{_libdir}/libflatbuffers.a
%{_libdir}/cmake/flatbuffers/*

%changelog
* Fri Nov 15 2019 Parichay kapoor <pk.kapoor@samsung.com>
- Release of 1.11.0
