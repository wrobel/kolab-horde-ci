# Variables
%define         V_package Horde_<?php if ($package->getName() == 'Role') {echo $package->getName() . "\n";} else {echo $package->getName() . "-H4\n";} ?>
%define         V_pear_package <?php echo $package->getName() . "\n"; ?>
%define         V_package_url http://pear.horde.org/<?php echo $package->getName() . "\n"; ?>
%define         V_version <?php echo $version . "\n"; ?>
%define         V_release 1
%define         V_sourceurl http://files.kolab.org/incoming/wrobel/Horde4
%define         V_php_lib_loc <?php if ($package->getName() == 'Role') {echo "php\n";} else {echo "php-h4\n";} ?>
%define         V_www_loc NONE
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
    if (!$dep->isRequired()) {
        echo 'PreReq: Horde_' . $dep->name() . '-H4';
        echo "\n";
    }
}
$ext_deps = $package->getDependencyHelper()->listAllExternalDependencies();
foreach ($ext_deps as $dep) {
    if (!$dep->isRequired()) {
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
        echo "\n";
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
	    %patch -p3 -P 0
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
	    %{l_prefix}/bin/pear -d www_dir="%{l_prefix}/var/kolab/www/%{V_www_loc}"   \
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

        %{l_rpmtool} files -v -ofiles -r$RPM_BUILD_ROOT %{l_files_std} 

%clean
	rm -rf $RPM_BUILD_ROOT

%files -f files
