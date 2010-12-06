# Variables
<?php if (in_array($package->getName(), array('horde', 'imp'))): ?>
%define         V_package <?php if ($package->getName() == 'Role') {echo $package->getName() . "\n";} else {echo $package->getName() . "-H4\n";} ?>
<?php else: ?>
%define         V_package Horde_<?php if ($package->getName() == 'Role') {echo $package->getName() . "\n";} else {echo $package->getName() . "-H4\n";} ?>
<?php endif; ?>

%define         V_pear_package <?php echo $package->getName() . "\n"; ?>
%define         V_package_url http://pear.horde.org/<?php echo $package->getName() . "\n"; ?>
%define         V_version <?php echo $version . "\n"; ?>
%define         V_release 1
%define         V_sourceurl http://files.kolab.org/incoming/wrobel/Horde4
%define         V_php_lib_loc <?php if ($package->getName() == 'Role') {echo "php\n";} else {echo "php-h4\n";} ?>
%define         V_www_loc var/kolab/www/client4
%define         V_summary <?php echo $package->getSummary() . "\n"; ?>
%define         V_license <?php echo $package->getLicense() . "\n"; ?>

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
<?php if ($package->getName() == 'horde'): ?>
Source1:        webclient4-config_conf.php.template
Source2:        webclient4-config_hooks.php.template
Source3:        webclient4-config_mime_drivers.php.template
Source4:        webclient4-config_motd.php.template
Source5:        webclient4-config_nls.php.template
Source6:        webclient4-config_prefs.php.template
Source7:        webclient4-config_registry.php.template
Source8:        10-kolab_hooks_base.php
Source9:        10-kolab_prefs_base.php
Source10:       10-kolab_conf_base.php
Source11:       horde.local.php
Source12:       hook-delete_webmail4_user.php
<?php endif; ?>
<?php if ($package->getName() == 'imp'): ?>
Source1:        webclient4-imp_backends.php.template
Source2:        webclient4-imp_conf.php.template
Source3:        webclient4-imp_header.php.template
Source4:        webclient4-imp_hooks.php.template
Source5:        webclient4-imp_menu.php.template
Source6:        webclient4-imp_mime_drivers.php.template
Source7:        webclient4-imp_portal.php.template
Source8:        webclient4-imp_prefs.php.template
Source9:        conf.php
Source10:       10-kolab_backends_base.php
Source11:       10-kolab_conf_base.php
Source12:       10-kolab_hooks_base.php
<?php endif; ?>

# List of patches
Patch0:    package.patch

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
<?php
$horde_deps = $package->getDependencyHelper()->listAllHordeDependencies();
foreach ($horde_deps as $dep) {
    if ($dep->isRequired() && !in_array($dep->name(), array('Core', 'DataTree', 'Kolab_Storage'))) {
        echo 'PreReq: Horde_' . $dep->name() . '-H4';
        echo "\n";
    } else if (in_array($dep->name(), array('Test'))) {
        echo 'PreReq: Horde_' . $dep->name() . '-H4';
        echo "\n";
    } else if (!$dep->isRequired()) {
        switch ($package->getName()) {
        case 'Core':
            if (in_array($dep->name(), array('Db', 'Kolab_Session', 'Kolab_Server', 'Tree', 'Http'))) {
                echo 'PreReq: Horde_' . $dep->name() . '-H4';
                echo "\n";
            } else {
                echo '#(Optional) PreReq: Horde_' . $dep->name() . '-H4';
                echo "\n";
            }
            break;
        case 'horde':
            if (in_array($dep->name(), array('Feed'))) {
                echo 'PreReq: Horde_' . $dep->name() . '-H4';
                echo "\n";
            } else {
                echo '#(Optional) PreReq: Horde_' . $dep->name() . '-H4';
                echo "\n";
            }
            break;
        }
    }
}
$ext_deps = $package->getDependencyHelper()->listAllExternalDependencies();
foreach ($ext_deps as $dep) {
    if ($dep->isRequired() || in_array($dep->name(), array('Log', 'Net_Socket', 'Net_SMTP', 'Auth_SASL', 'Crypt_Blowfish', 'DB'))) {
        if ($dep->name() == 'PEAR') {
            continue;
        }
        if ($dep->channel() == 'pecl.php.net') {
            # No pecl for OpenPKG now.
            continue;
        }
        echo 'PreReq: ';
        switch ($dep->channel()) {
        case 'pear.php.net':
            echo 'PEAR-';
            break;
        case 'pecl.php.net':
            echo 'pecl-';
            break;
        default:
            break;
        }
        echo $dep->name();
        echo "-H4\n";
    }
}
?>

# Package options
%option       with_chroot              no

%description 
<?php echo $package->getDescription() . "\n"; ?>

%prep
	%setup -n %{V_pear_package}-%{V_version}

	cat ../package.xml | sed -e 's/md5sum="[^"]*"//' > package.xml

        if [ -n "`cat %{PATCH0}`" ]; then
	    %patch -p1 -P 0
	fi

<?php if ($package->getName() == 'horde'): ?>
        sed -i -e 's#/usr/bin/env php#%{l_prefix}/bin/php#' bin/*
<?php endif; ?>

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

<?php if ($package->getName() == 'horde'): ?>
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/var/kolab/hooks/delete
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/storage
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/log
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/tmp
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/sessions
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates	
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/conf.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/hooks.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/mime_drivers.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/motd.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/nls.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/prefs.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/registry.d

	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} %{S:7} \
	  $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates
	sed -i -e 's#@@@horde_confdir@@@#%{l_prefix}/%{V_www_loc}/config#' $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates/*.php.template

	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:8} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/hooks.d/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:9} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/prefs.d/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:10} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/conf.d/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:11} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/
	sed -i -e 's#@@@prefix@@@#%{l_prefix}#' $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/horde.local.php
	sed -i -e 's#@@@lib_loc@@@#%{V_php_lib_loc}#' $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/horde.local.php

	%{l_shtool} install -c -m 755 %{l_value -s -a} %{S:12} $RPM_BUILD_ROOT%{l_prefix}/var/kolab/hooks/delete
	sed -i -e 's#@@@prefix@@@#%{l_prefix}#' $RPM_BUILD_ROOT%{l_prefix}/var/kolab/hooks/delete/hook-*
	sed -i -e 's#@@@php_bin@@@#%{l_prefix}/bin/php#' $RPM_BUILD_ROOT%{l_prefix}/var/kolab/hooks/delete/hook-*


        %{l_prefix}/bin/sqlite3 $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/storage/horde.db < scripts/sql/horde_alarms.sql
        %{l_prefix}/bin/sqlite3 $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/storage/horde.db < scripts/sql/horde_datatree.sql
        sed -i -e 's/AUTO_INCREMENT//' scripts/sql/horde_perms.sql
        %{l_prefix}/bin/sqlite3 $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/storage/horde.db < scripts/sql/horde_perms.sql
        %{l_prefix}/bin/sqlite3 $RPM_BUILD_ROOT%{l_prefix}/var/kolab/webclient4_data/storage/horde.db < scripts/sql/horde_syncml.sql

	for fl in $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/config/*.dist;do cp $fl ${fl/.dist/}; done
<?php endif; ?>
<?php if ($package->getName() == 'imp'): ?>
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates	
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/backends.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/conf.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/header.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/hooks.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/menu.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/mime_drivers.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/portal.d
	%{l_shtool} install -d $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/prefs.d

	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:1} %{S:2} %{S:3} %{S:4} %{S:5} %{S:6} %{S:7} %{S:8}\
	  $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates
	sed -i -e 's#@@@imp_confdir@@@#%{l_prefix}/%{V_www_loc}/imp/config#' $RPM_BUILD_ROOT%{l_prefix}/etc/kolab/templates/*.php.template

	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:9} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:10} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/backends.d/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:11} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/conf.d/
	%{l_shtool} install -c -m 644 %{l_value -s -a} %{S:12} $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/hooks.d/

	for fl in $RPM_BUILD_ROOT%{l_prefix}/%{V_www_loc}/imp/config/*.dist;do cp $fl ${fl/.dist/}; done
<?php endif; ?>

        %{l_rpmtool} files -v -ofiles -r$RPM_BUILD_ROOT %{l_files_std} \
<?php if ($package->getName() == 'horde'): ?>
	    '%config %{l_prefix}/etc/kolab/templates/webclient4-config_conf.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_hooks.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_mime_drivers.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_motd.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_nls.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_prefs.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-config_registry.php.template' \
            '%config(noreplace) %{l_prefix}/var/kolab/webclient4_data/storage/horde.db' \
            %dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/webclient4_data/log \
            %dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/webclient4_data/storage \
            %dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/webclient4_data/storage/horde.db \
            %dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/webclient4_data/tmp \
            %dir '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/webclient4_data/sessions \
	    '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/www/client4/config/conf.php
<?php endif; ?>
<?php if ($package->getName() == 'imp'): ?>
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_backends.php.template' \
	    '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_conf.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_header.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_hooks.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_menu.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_mime_drivers.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_portal.php.template' \
            '%config %{l_prefix}/etc/kolab/templates/webclient4-imp_prefs.php.template' \
	    '%defattr(-,%{l_nusr},%{l_ngrp})' %{l_prefix}/var/kolab/www/client4/imp/config/conf.php
<?php endif; ?>

%clean
	rm -rf $RPM_BUILD_ROOT

%files -f files
