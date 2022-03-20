%global commit0 4fd620cd6cb80fb0c1490dc1c864108679d91ab1
%global date 20220306
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%global dkms_name xpadneo

Name:       dkms-%{dkms_name}
Version:    0.9.1
Release:    4%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:    Advanced Linux Driver for Xbox One Wireless Gamepad
License:    GPLv3
URL:        https://atar-axis.github.io/%{dkms_name}
BuildArch:  noarch

%if 0%{?tag:1}
Source0:    https://github.com/atar-axis/%{dkms_name}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
%else
Source0:    https://github.com/atar-axis/%{dkms_name}/archive/%{commit0}.tar.gz#/%{dkms_name}-%{shortcommit0}.tar.gz
%endif

Source1:    %{name}.conf
Source2:    dkms-no-weak-modules.conf

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
Advanced Linux Driver for Xbox One Wireless Gamepad.

%prep
%if 0%{?tag:1}
%autosetup -p1 -n %{dkms_name}-%{version}
%else
%autosetup -p1 -n %{dkms_name}-%{commit0}
%endif

cp -f %{SOURCE1} hid-xpadneo/src/dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' hid-xpadneo/src/dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr hid-xpadneo/src/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Sun Mar 20 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-4.20220306git4fd620c
- Update to latest snapshot, adds support for BLE firmware.

* Sun Jan 23 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-3.20211203gitcf392a7
- Update to latest snapshot.

* Mon Aug 30 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-2
- Add upstream patches.

* Mon Aug 16 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-1
- First build.
