#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	haskell-src-meta
Summary:	Parse source to template-haskell abstract syntax
Summary(pl.UTF-8):	Przetwarzanie źródeł do abstrakcyjnej składni biblioteki template-haskell
Name:		ghc-%{pkgname}
Version:	0.6.0.5
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/haskell-src-meta
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	e59e0fedf6985494e82220477c54795c
URL:		http://hackage.haskell.org/package/haskell-src-meta
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4.2
BuildRequires:	ghc-base < 4.8
BuildRequires:	ghc-haskell-src-exts >= 1.14
BuildRequires:	ghc-haskell-src-exts < 1.15
BuildRequires:	ghc-pretty >= 1.0
BuildRequires:	ghc-pretty < 1.2
BuildRequires:	ghc-syb >= 0.1
BuildRequires:	ghc-syb < 0.5
BuildRequires:	ghc-template-haskell >= 2.4
BuildRequires:	ghc-template-haskell < 2.10
BuildRequires:	ghc-th-orphans >= 0.5
BuildRequires:	ghc-th-orphans < 0.9
BuildRequires:	ghc-uniplate >= 1.3
BuildRequires:	ghc-uniplate < 1.7
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4.2
BuildRequires:	ghc-base-prof < 4.8
BuildRequires:	ghc-haskell-src-exts-prof >= 1.14
BuildRequires:	ghc-haskell-src-exts-prof < 1.15
BuildRequires:	ghc-pretty-prof >= 1.0
BuildRequires:	ghc-pretty-prof < 1.2
BuildRequires:	ghc-syb-prof >= 0.1
BuildRequires:	ghc-syb-prof < 0.5
BuildRequires:	ghc-template-haskell-prof >= 2.4
BuildRequires:	ghc-template-haskell-prof < 2.10
BuildRequires:	ghc-th-orphans-prof >= 0.5
BuildRequires:	ghc-th-orphans-prof < 0.9
BuildRequires:	ghc-uniplate-prof >= 1.3
BuildRequires:	ghc-uniplate-prof < 1.7
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_releq	ghc
Requires:	ghc >= 6.12.3
Requires:	ghc-base >= 4.2
Requires:	ghc-base < 4.8
Requires:	ghc-haskell-src-exts >= 1.14
Requires:	ghc-haskell-src-exts < 1.15
Requires:	ghc-pretty >= 1.0
Requires:	ghc-pretty < 1.2
Requires:	ghc-syb >= 0.1
Requires:	ghc-syb < 0.5
Requires:	ghc-template-haskell >= 2.4
Requires:	ghc-template-haskell < 2.10
Requires:	ghc-th-orphans >= 0.5
Requires:	ghc-th-orphans < 0.9
Requires:	ghc-uniplate >= 1.3
Requires:	ghc-uniplate < 1.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Parse source to template-haskell abstract syntax.

%description -l pl.UTF-8
Przetwarzanie źródeł do abstrakcyjnej składni biblioteki
template-haskell.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4.2
Requires:	ghc-base-prof < 4.8
Requires:	ghc-haskell-src-exts-prof >= 1.14
Requires:	ghc-haskell-src-exts-prof < 1.15
Requires:	ghc-pretty-prof >= 1.0
Requires:	ghc-pretty-prof < 1.2
Requires:	ghc-syb-prof >= 0.1
Requires:	ghc-syb-prof < 0.5
Requires:	ghc-template-haskell-prof >= 2.4
Requires:	ghc-template-haskell-prof < 2.10
Requires:	ghc-th-orphans-prof >= 0.5
Requires:	ghc-th-orphans-prof < 0.9
Requires:	ghc-uniplate-prof >= 1.3
Requires:	ghc-uniplate-prof < 1.7

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
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
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README examples %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HShaskell-src-meta-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-meta-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Parse
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Parse/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHShaskell-src-meta-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Parse/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/Meta/Syntax/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Language/Haskell/TH/Instances/*.p_hi
%endif
