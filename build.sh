#!/bin/bash

list_dependencies=(rpm-build rpmdevtools)

for i in ${list_dependencies[*]}
do
    if ! rpm -qa | grep -qw $i; then
        echo "__________Dont installed '$i'__________"
        #yum -y install $i
    fi
done

mkdir -p ./{RPMS,SRPMS,BUILD,SOURCES,SPECS}
cp teamcity-server.service ./SOURCES
spectool -g -R teamcity-server-rpm.spec
sudo yum-builddep -y teamcity-server-rpm.spec
rpmbuild --quiet --define "_topdir `pwd`" -bb teamcity-server-rpm.spec
