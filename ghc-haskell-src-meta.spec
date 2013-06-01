%define		pkgname	haskell-src-meta
Summary:	Parse source to template-haskell abstract syntax
Name:		ghc-%{pkgname}
Version:	0.6.0.2
Release:	3
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d3b9c3dfbc9bb9466e0a002ed195c352
URL:		http://hackage.haskell.org/package/haskell-src-meta/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-haskell-platform
BuildRequires:	ghc-haskell-platform-prof
BuildRequires:	ghc-haskell-src-exts
BuildRequires:	ghc-haskell-src-exts-prof
BuildRequires:	ghc-th-lift
BuildRequires:	ghc-th-lift-prof
BuildRequires:	ghc-th-orphans
BuildRequires:	ghc-th-orphans-prof
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires:	ghc-haskell-platform
Requires:	ghc-haskell-src-exts
Requires:	ghc-th-lift
Requires:	ghc-th-orphans
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
Parse source to template-haskell abstract syntax.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-haskell-platform-prof
Requires:	ghc-haskell-src-exts-prof
Requires:	ghc-th-lift-prof
Requires:	ghc-th-orphans-prof

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README examples
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances/*.p_hi
