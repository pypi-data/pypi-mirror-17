# Created by pyp2rpm-3.1.3
%global pypi_name isholiday

Name:           python-%{pypi_name}
Version:        0.2
Release:        1%{?dist}
Summary:        Finds Czech holiday for given year

License:        Public Domain
URL:            https://gist.github.com/oskar456/e91ef3ff77476b0dbc4ac19875d0555e
Source0:        
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description


%package -n     python3-%{pypi_name}
Summary:        Finds Czech holiday for given year
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}



%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install


%files -n python3-%{pypi_name}
%doc 
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Wed Sep 21 2016 Michal Cyprian <mcyprian@redhat.com> - 0.2-1
- Initial package.