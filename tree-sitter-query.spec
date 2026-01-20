Summary:	A tree-sitter parser for tree-sitter query files
Summary(pl.UTF-8):	Analizator składniowy tree-sittera do plików zapytań tree-sittera
Name:		tree-sitter-query
Version:	0.8.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/tree-sitter-grammars/tree-sitter-query/releases
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-query/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1b85950e4496d5e349c71f055ad247c6
URL:		https://github.com/tree-sitter-grammars/tree-sitter-query
# c11
BuildRequires:	gcc >= 6:4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	15.0

%description
A tree-sitter query file parser for tree-sitter.

%description -l pl.UTF-8
Analizator składniowy tree-sittera do plików zapytań tree-sittera.

%package devel
Summary:	Header files for tree-sitter-query
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-query
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-query.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-query.

%package static
Summary:	Static tree-sitter-query library
Summary(pl.UTF-8):	Statyczna biblioteka tree-sitter-query
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-query library.

%description static -l pl.UTF-8
Statyczna biblioteka tree-sitter-query.

%package -n neovim-parser-query
Summary:	tree-sitter query file parser for Neovim
Summary(pl.UTF-8):	Analizator składniowy plików zapytań tree-sittera dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-query
tree-sitter query file parser for Neovim.

%description -n neovim-parser-query -l pl.UTF-8
Analizator składniowy plików zapytań tree-sittera dla Neovima.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} -f libtree-sitter-query.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-query.so

%{__ln_s} -f ../../libtree-sitter-query.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/query.so

# redundant symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-query.so.15

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libtree-sitter-query.so.%{soname_ver}
# XXX: who should own top dirs?
%dir %{_datadir}/tree-sitter
%dir %{_datadir}/tree-sitter/queries
%{_datadir}/tree-sitter/queries/query

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-query.so
%{_includedir}/tree_sitter/tree-sitter-query.h
%{_pkgconfigdir}/tree-sitter-query.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-query.a

%files -n neovim-parser-query
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/query.so
