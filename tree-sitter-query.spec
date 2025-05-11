Summary:	A tree-sitter parser for tree-sitter query files
Name:		tree-sitter-query
Version:	0.5.1
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-query/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	03a4e0e559587ab4e2af245fa44c7a35
URL:		https://github.com/tree-sitter-grammars/tree-sitter-query
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_query_soname	libtree-sitter-query.so.14.0

%description
A tree-sitter query file parser for tree-sitter.

%package devel
Summary:	Header files for tree-sitter-query
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-query.

%package static
Summary:	Static tree-sitter-query library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-query library.

%package -n neovim-parser-query
Summary:	tree-sitter query file parser for Neovim
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-query
tree-sitter query file parser for Neovim.

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

%{__ln_s} -f %{_libdir}/%{ts_query_soname} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-query.so

%{__ln_s} %{_libdir}/%{ts_query_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/query.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_libdir}/%{ts_query_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-query.so
%{_includedir}/tree_sitter/tree-sitter-query.h
%{_pkgconfigdir}/tree-sitter-query.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-query.a

%files -n neovim-parser-query
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/query.so
