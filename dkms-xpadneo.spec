%global commit0 70ef8ee276354eb82bd1de224fcc9c0f8a6390c9
%global date 20240923
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%global dkms_name xpadneo

Name:       dkms-%{dkms_name}
Version:    0.9.6%{!?tag:^%{date}git%{shortcommit0}}
Release:    3%{?dist}
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
* Tue Sep 24 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6^20240923git70ef8ee-3
- Use new packaging guidelines for snapshots.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6-2.20240423git73be2eb
- Update to latest snapshot.

* Sat Feb 17 2024 Simone Caronni <negativo17@gmail.com> - 0.9.6-1
- Update to final 0.9.6.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 0.9.5-4.20240130gitbce97bd
- Update to latest snapshot.

* Wed Jun 21 2023 Simone Caronni <negativo17@gmail.com> - 0.9.5-3.20230617git5970c4c
- Update to latest snapshot.

* Sun Jun 04 2023 Simone Caronni <negativo17@gmail.com> - 0.9.5-2.2023050330503git13dd267
- Update to latest snapshot.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 0.9.5-1
- Update to 0.9.5.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 0.9.4-1
- Update to 0.9.4.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 0.9.3-1
- Update to release 0.9.3.

* Sun May 01 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-5.20220430git74ea7c1
- Update to latest snapshot, supports firmware 5.13.

* Sun Mar 20 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-4.20220306git4fd620c
- Update to latest snapshot, adds support for BLE firmware.

* Sun Jan 23 2022 Simone Caronni <negativo17@gmail.com> - 0.9.1-3.20211203gitcf392a7
- Update to latest snapshot.

* Mon Aug 30 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-2
- Add upstream patches.

* Mon Aug 16 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-1
- First build.
