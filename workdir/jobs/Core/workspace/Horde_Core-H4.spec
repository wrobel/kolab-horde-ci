# Variables
%define         V_package Horde_Core-H4

%define         V_pear_package Horde_Core
%define         V_package_url http://pear.horde.org/Horde_Core
%define         V_version 0.1.0dev201102221423
%define         V_release 1
%define         V_sourceurl http://files.kolab.org/incoming/wrobel/Horde4
%define         V_php_lib_loc php-h4
%define         V_www_loc var/kolab/www/client4
%define         V_summary Horde Core Framework libraries
%define         V_license LGPL

# Package Information
Name:	   %{V_package}
Summary:   %{V_summary}
URL:       {%V_package_url}%{V_pear_package}
Packager:  Gunnar Wrobel <wrobel@pardus.de> (p@rdus)
Version:   %{V_version}
Release:   %{V_release}
License:   %{V_license}
Group:     Development/Libraries
Distribution:	OpenPKG

# List of Sources
Source:    %{V_sourceurl}/%{V_pear_package}-%{V_version}.tgz

# Build Info
Prefix:	   %{l_prefix}
BuildRoot: %{l_buildroot}

#Pre requisites
BuildPreReq:  OpenPKG, openpkg >= 20070603
BuildPreReq:  php, php::with_pear = yes
BuildPreReq:  PEAR-Horde-Channel
PreReq:       OpenPKG, openpkg >= 20070603
PreReq:       php, php::with_pear = yes
PreReq:       PEAR-Horde-Channel
PreReq: Horde_ActiveSync-H4
PreReq: Horde_Alarm-H4
PreReq: Horde_Auth-H4
PreReq: Horde_Autoloader-H4
#(Optional) PreReq: Horde_Browser-H4
PreReq: Horde_Cache-H4
PreReq: Horde_Cli-H4
PreReq: Horde_Exception-H4
PreReq: Horde_History-H4
PreReq: Horde_Injector-H4
PreReq: Horde_Lock-H4
PreReq: Horde_Log-H4
PreReq: Horde_LoginTasks-H4
PreReq: Horde_Mime-H4
PreReq: Horde_Mime_Viewer-H4
PreReq: Horde_Notification-H4
PreReq: Horde_Perms-H4
PreReq: Horde_Prefs-H4
PreReq: Horde_Secret-H4
PreReq: Horde_SessionHandler-H4
PreReq: Horde_Share-H4
PreReq: Horde_Support-H4
PreReq: Horde_Translation-H4
PreReq: Horde_Url-H4
PreReq: Horde_Util-H4
#(Optional) PreReq: Horde_Crypt-H4
PreReq: Horde_Db-H4
#(Optional) PreReq: Horde_Editor-H4
#(Optional) PreReq: Horde_Form-H4
PreReq: Horde_Http-H4
#(Optional) PreReq: Horde_Icalendar-H4
PreReq: Horde_Kolab_Server-H4
PreReq: Horde_Kolab_Session-H4
PreReq: Horde_Kolab_Storage-H4
#(Optional) PreReq: Horde_Nls-H4
#(Optional) PreReq: Horde_Service_Twitter-H4
#(Optional) PreReq: Horde_Text_Filter-H4
PreReq: Horde_Tree-H4
#(Optional) PreReq: Horde_VFS-H4
PreReq: PEAR-DB-H4

# Package options
%option       with_chroot              no

%description 
These classes provide the core functionality of the Horde
Application Framework.

%prep
	%setup -n %{V_pear_package}-%{V_version}

	cat ../package.xml | sed -e 's/md5sum="[^"]*"//' > package.xml

        if [ -e bin ]; then
          find bin -type f | xargs sed -i -e 's#/usr/bin/env php#%{l_prefix}/bin/php#'
        fi

%build

%install
	if [ -d scripts ]; then
          find scripts -type f | xargs sed -i -e "s#/bin/sh#%{l_prefix}/lib/openpkg/bash#"
	fi
        if [ "%{V_php_lib_loc}" == "php-h4" ]; then
          PHP_BIN_DIR="bin-h4"
        else
          PHP_BIN_DIR="bin"
        fi
        env PHP_PEAR_PHP_BIN="%{l_prefix}/bin/php -d safe_mode=off -d memory_limit=40M"\
            PHP_PEAR_CACHE_DIR="/tmp/pear/cache"                                       \
	    %{l_prefix}/bin/pear -d horde_dir="%{l_prefix}/%{V_www_loc}"               \
	                         -d bin_dir="%{l_prefix}/$PHP_BIN_DIR"                 \
	                         -d php_dir="%{l_prefix}/lib/%{V_php_lib_loc}"         \
	                         -d doc_dir="%{l_prefix}/lib/%{V_php_lib_loc}/doc"     \
	                         -d data_dir="%{l_prefix}/lib/%{V_php_lib_loc}/data"   \
	                         -d test_dir="%{l_prefix}/lib/%{V_php_lib_loc}/test"   \
                                 install --offline --force --nodeps -P $RPM_BUILD_ROOT \
                                 package.xml

	rm -rf $RPM_BUILD_ROOT/%{l_prefix}/lib/%{V_php_lib_loc}/{.filemap,.lock,.channels,.depdb,.depdblock}

        # With chroot
        %if "%{with_chroot}" == "yes"
                %{l_shtool} mkdir -f -p -m 755 $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/%{l_prefix}/lib
                cp -a $RPM_BUILD_ROOT/%{l_prefix}/lib/%{V_php_lib_loc} $RPM_BUILD_ROOT%{l_prefix}/var/kolab/www/%{l_prefix}/lib/
        %endif


        %{l_rpmtool} files -v -ofiles -r$RPM_BUILD_ROOT %{l_files_std} \

%clean
	rm -rf $RPM_BUILD_ROOT

%files -f files
