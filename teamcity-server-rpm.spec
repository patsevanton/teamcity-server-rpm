%global __os_install_post %{nil}
%global _unpackaged_files_terminate_build      0
%global _binaries_in_noarch_packages_terminate_build   0
AutoReqProv: no

Name:    teamcity
Version: 2020.1
Release: 1
Summary: The best long-term remote storage for Prometheus

Group:   Development Tools
License: ASL 2.0
URL: https://download-cf.jetbrains.com/teamcity/TeamCity-%{version}.tar.gz
Source0: teamcity-server.service
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel
BuildRequires: wget
BuildArch: noarch

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%description
teamcity - Powerful Continuous Integration and Continuous Delivery out of the box.

%prep
pwd
wget --no-clobber  %{url} -O TeamCity.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}/var
tar -xzf TeamCity.tar.gz -C %{buildroot}/var
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/%{name}.service
%endif

%pre
/usr/bin/getent group teamcity > /dev/null || /usr/sbin/groupadd -r teamcity
/usr/bin/getent passwd teamcity > /dev/null || /usr/sbin/useradd -r -d /var/TeamCity -s /bin/bash -g teamcity teamcity

%post
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%preun
%if %use_systemd
/usr/bin/systemctl stop %{name}
%endif

%postun
%if %use_systemd
/usr/bin/systemctl daemon-reload
%endif

%files
%defattr (-, teamcity, teamcity,-)
/var/TeamCity
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
