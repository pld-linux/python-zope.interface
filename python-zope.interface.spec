#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-zope.interface.spec)
%bcond_without	tests	# unit tests

%define		module	zope.interface
Summary:	Python 'interface' concept implementation
Summary(pl.UTF-8):	Implementacja interfejsów dla języka Python
Name:		python-%{module}
# keep 5.x here for python2 support
Version:	5.5.2
Release:	4
License:	ZPL v2.1
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/zope.interface/
Source0:	https://files.pythonhosted.org/packages/source/z/zope.interface/zope.interface-%{version}.tar.gz
# Source0-md5:	5a383d71156ce6f89f59a86d957a8d65
URL:		https://zopeinterface.readthedocs.io/
%if %{with python2}
BuildRequires:	python >= 1:2.7
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-coverage >= 5.0.3
BuildRequires:	python-zope.event
BuildRequires:	python-zope.testing
%endif
%endif
%if %{with python3}
BuildRequires:	python3 >= 1:3.5
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-coverage >= 5.0.3
BuildRequires:	python3-zope.event
BuildRequires:	python3-zope.testing
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-repoze.sphinx.autointerface
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
Requires:	python-zope-base
Provides:	ZopeInterface
Provides:	Zope-Interface
Obsoletes:	ZopeInterface < 3.4.0
Obsoletes:	Zope-Interface < 4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python 'interface' concept implementation.

%description -l pl.UTF-8
Implementacja interfejsów (abstrakcyjnych reprezentacji klas) dla
języka Python.

%package -n python3-%{module}
Summary:	Python 'interface' concept implementation
Summary(pl.UTF-8):	Implementacja interfejsów dla języka Python
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
Requires:	python3-zope-base

%description -n python3-%{module}
Python 'interface' concept implementation.

%description -n python3-%{module} -l pl.UTF-8
Implementacja interfejsów (abstrakcyjnych reprezentacji klas) dla
języka Python.

%package apidocs
Summary:	API documentation for Python zope.interface module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona zope.interface
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Python zope.interface module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona zope.interface.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/zope/interface/*.c

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/zope/interface/*.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt README.rst
%dir %{py_sitedir}/zope/interface
%{py_sitedir}/zope/interface/*.py[co]
%attr(755,root,root) %{py_sitedir}/zope/interface/_zope_interface_coptimizations.so
%{py_sitedir}/zope/interface/common
%{py_sitedir}/zope/interface/tests
%{py_sitedir}/zope.interface-%{version}-py*.egg-info
%{py_sitedir}/zope.interface-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst COPYRIGHT.txt README.rst
%dir %{py3_sitedir}/zope/interface
%{py3_sitedir}/zope/interface/*.py
%{py3_sitedir}/zope/interface/__pycache__
%attr(755,root,root) %{py3_sitedir}/zope/interface/_zope_interface_coptimizations*.so
%{py3_sitedir}/zope/interface/common
%{py3_sitedir}/zope/interface/tests
%{py3_sitedir}/zope.interface-%{version}-py*.egg-info
%{py3_sitedir}/zope.interface-%{version}-py*-nspkg.pth
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
