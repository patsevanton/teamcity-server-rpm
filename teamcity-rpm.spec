Name:    teamcity
Version: 2020.1
Release: 1
Summary: The best long-term remote storage for Prometheus

Group:   Development Tools
License: ASL 2.0
URL: https://download-cf.jetbrains.com/teamcity/TeamCity-%{version}.tar.gz
Source0: %{name}.service
Source1: teamcity.conf
Requires(pre): /usr/sbin/useradd, /usr/bin/getent, /usr/bin/echo, /usr/bin/chown
Requires(postun): /usr/sbin/userdel

# Use systemd for fedora >= 18, rhel >=7, SUSE >= 12 SP1 and openSUSE >= 42.1
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (!0%{?is_opensuse} && 0%{?suse_version} >=1210) || (0%{?is_opensuse} && 0%{?sle_version} >= 120100)

%description
teamcity - Powerful Continuous Integration and Continuous Delivery out of the box.

%prep
curl -L %{url} > TeamCity.tar.gz
tar -zxf TeamCity.tar.gz

%install
%{__install} -m 0755 -d %{buildroot}%{_bindir}
%{__install} -m 0755 -d %{buildroot}/etc/default/
cp %{SOURCE1} %{buildroot}/etc/default/
cp victoria-metrics-prod %{buildroot}%{_bindir}/victoria-metrics-prod
%{__install} -m 0755 -d %{buildroot}/var/lib/victoria-metrics-data
%if %{use_systemd}
%{__mkdir} -p %{buildroot}%{_unitdir}
%{__install} -m644 %{SOURCE0} \
    %{buildroot}%{_unitdir}/%{name}.service
%endif

%pre
/usr/bin/getent group teamcity > /dev/null || /usr/sbin/groupadd -r teamcity
/usr/bin/getent passwd teamcity > /dev/null || /usr/sbin/useradd -r -d /var/lib/victoria-metrics-data -s /bin/bash -g teamcity teamcity
%{__mkdir} /var/lib/victoria-metrics-data
/usr/bin/echo "WARINING: chown -R teamcity:teamcity /var/lib/victoria-metrics-data"
/usr/bin/echo "THIS MAY TAKE SOME TIME"
/usr/bin/chown -R teamcity:teamcity /var/lib/victoria-metrics-data

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
/etc/default/teamcity.conf
%{_bindir}/victoria-metrics-prod
%dir %attr(0775, teamcity, teamcity) /var/lib/victoria-metrics-data
%if %{use_systemd}
%{_unitdir}/%{name}.service
%endif
