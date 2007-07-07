%define	plevel p5

%define	major 0
%define libname	%mklibname spf %{major}

Summary:	A portable ANSI C implementation of the Sender Policy Framework library
Name:		libspf
Version:	1.0.0
Release:	%mkrel 4
License:	BSD
Group:		System/Libraries
URL:		http://libspf.org/
Source0:	http://libspf.org/files/src/%{name}-%{version}-%{plevel}.tar.bz2
Patch0:		libspf-autofoo_fixes.diff
Patch1:		libspf-1.0.0-p5-double-free_bug.diff
BuildRequires:	chrpath
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
libspf - Sender Permitted From library

ANSI C implementation of draft-mengwong-spf-02.9.7.txt

%package -n	%{libname}
Summary:	A portable ANSI C implementation of the Sender Policy Framework library
Group:		System/Libraries

%description -n	%{libname}
libspf - Sender Permitted From library

ANSI C implementation of draft-mengwong-spf-02.9.7.txt

%package -n	%{libname}-devel
Summary:	Development files for the %{name} library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
libspf - Sender Permitted From library

ANSI C implementation of draft-mengwong-spf-02.9.7.txt

This package contains the development library and its header files
for the libspf library.

%package	utils
Summary:	Sender Permitted From (SPF) command line utilities
Group:		System/Servers
Obsoletes:	spfquery

%description	utils
Sender Permitted From (SPF) command line query tool

%prep

%setup -q -n %{name}-%{version}-%{plevel}
%patch0 -p1
%patch1 -p0

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;
find . -type f -perm 0744 -exec chmod 644 {} \;
find . -type f -perm 0544 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done
    	
%build

%configure2_5x \
    --enable-pthreads \
    --enable-full-optimizations

make

make test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

rm -f %{buildroot}%{_bindir}/*_static
rm -f %{buildroot}%{_sbindir}/*_static

# nuke rpath
chrpath -d %{buildroot}%{_bindir}/*

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%doc CHANGELOG FAQ LICENSE README TODO docs examples
%{_libdir}/*.so.*

%files utils
%defattr(-,root,root)
%doc src/spfqtool/INSTALL src/spfqtool/test.pl src/spfqtool/test.txt
%{_bindir}/spfqtool

%files -n %{libname}-devel
%defattr(-,root,root)
%doc patches
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
