include settings.mk
include jenkins/jenkins.mk
include horde-packaging/make/jobs.mk

HORDE_FRAMEWORK=workdir/jobs/horde-git/workspace/framework
TOOLSDIR=workdir/jobs/php-ci-tools/workspace/pear/pear

DEPENDENCIES=PEAR-PEAR-1.9.1 \
             PEAR-Console_Getopt-1.2.3 \
             PEAR-PEAR-H4 \
             PEAR-Console_Getopt-H4 \
             PEAR-Horde-Channel \
             PEAR-Auth_SASL-H4 \
             PEAR-Crypt_Blowfish-H4 \
             PEAR-DB-H4 \
             PEAR-Log-H4 \
             PEAR-Mail-H4 \
             PEAR-Net_SMTP-H4 \
             PEAR-Net_Socket-H4 \
             PEAR-PHPUnit-Channel-H4 \
             PHPUnit-H4

.PHONY:install
install: jenkins-install kolab-dependencies

.PHONY:install-latest
install-latest: jenkins-install-latest kolab-dependencies

.PHONY:kolab-dependencies
kolab-dependencies: $(DEPENDENCIES:%=dependency-%)

.PHONY: $(DEPENDENCIES:%=dependency-%)
$(DEPENDENCIES:%=dependency-%):
	/kolab/bin/openpkg rpm --rebuild dependencies/$(@:dependency-%=%)-*.src.rpm
	-/kolab/bin/openpkg rpm -Uhv --force /kolab/RPM/PKG/$(@:dependency-%=%)-*.rpm

.PHONY:jenkins-jobs
jenkins-jobs: $(JOBS:%=job-%) $(APP_JOBS:%=job-%)

.PHONY:$(JOBS:%=job-%)
$(JOBS:%=job-%):
	mkdir -p workdir/jobs/$(@:job-%=%)
	php -d include_path=$(TOOLSDIR)/php $(TOOLSDIR)/horde-components -T php-ci-tools/workspace/pear/pear -t $(WORKDIR)/templates -c workdir/jobs/$(@:job-%=%) --pearrc=$(TOOLSDIR)/../.pearrc $(HORDE_FRAMEWORK)/$(@:job-%=%)
	if [ "$(@:job-%=%)" = "Role" ]; then \
	  NAME=Horde_Role; \
	else \
	  NAME=Horde_$(@:job-%=%)-H4; \
	fi; \
	sed -i -e "s/@NAME@/$$NAME/g" workdir/jobs/$(@:job-%=%)/config.xml
	mkdir -p workdir/jobs/$(@:job-%=%)/workspace/
	touch workdir/jobs/$(@:job-%=%)/workspace/package.patch
	cp templates/job-gitignore workdir/jobs/$(@:job-%=%)/.gitignore

.PHONY:$(APP_JOBS:%=job-%)
$(APP_JOBS:%=job-%):
	mkdir -p workdir/jobs/$(@:job-%=%)
	php -d include_path=$(TOOLSDIR)/php $(TOOLSDIR)/horde-components -T php-ci-tools/workspace/pear/pear -t $(WORKDIR)/templates -c workdir/jobs/$(@:job-%=%) --pearrc=$(TOOLSDIR)/../.pearrc $(HORDE_FRAMEWORK)/../$(@:job-%=%)
	sed -i -e 's/@NAME@/$(@:job-%=%)-H4/g' workdir/jobs/$(@:job-%=%)/config.xml
	mkdir -p workdir/jobs/$(@:job-%=%)/workspace/
	touch workdir/jobs/$(@:job-%=%)/workspace/package.patch
	cp templates/job-gitignore workdir/jobs/$(@:job-%=%)/.gitignore

PHONY:clean-all
clean-all: clean clean-jobs

PHONY:clean
clean: jenkins-clean

.PHONY:clean-jobs
clean-jobs: $(JOBS:%=clean-job-%)

.PHONY:$(JOBS:%=clean-job-%)
$(JOBS:%=clean-job-%):
	rm -rf workdir/jobs/$(@:clean-job-%=%)/builds
	rm -rf workdir/jobs/$(@:clean-job-%=%)/htmlreports
	rm -rf workdir/jobs/$(@:clean-job-%=%)/lastStable
	rm -rf workdir/jobs/$(@:clean-job-%=%)/lastSuccessful
	rm -rf workdir/jobs/$(@:clean-job-%=%)/nextBuildNumber
