%global debug_package %{nil}
%global dkms_name xpadneo

Name:       dkms-%{dkms_name}
Version:    0.9.1
Release:    2%{?dist}
Summary:    Advanced Linux Driver for Xbox One Wireless Gamepad
License:    GPLv3
URL:        https://atar-axis.github.io/%{dkms_name}
BuildArch:  noarch

Source0:    https://github.com/atar-axis/%{dkms_name}/archive/refs/tags/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
Source1:    %{name}.conf
Source2:    dkms-no-weak-modules.conf
Patch0:     xpadneo-git.patch

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
Advanced Linux Driver for Xbox One Wireless Gamepad.

%prep
%autosetup -p1 -n %{dkms_name}-%{version}

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
* Mon Aug 30 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-2
- Add upstream patches.

* Mon Aug 16 2021 Simone Caronni <negativo17@gmail.com> - 0.9.1-1
- First build.
