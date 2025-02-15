This repo contains the Python3 port of the ISFDB. This work is currently in progress.

Let's say the isfdb.org is down, the founders are not responding, and the wiki at isfdb.org is not available. How would one bootstrap a new version of isfdb.org? Here are the steps needed to bringup a new version of the web site.

<h1>Prerequisites</h1>
The system is a minimum configuration of Fedora Core. As such, many packages need to be installed with dnf.

* dnf install gcc
* dnf install make
* dnf install tar
* dnf install zip.x86_64
* dnf install bzip2.x86_64
* dnf install wget
* dnf install mod_dav_svn subversion
* dnf install telnet
* dnf install ImageMagick

<h1>Apache</h1>
Install and configure apache:

* dnf install httpd
* firewall-cmd --add-service=http --add-service=https --permanent
* Add to etc/httpd/httpd.conf: LoadModule dir_module modules/mod_dir.so
* Change etc/httpd/httpd.conf: DirectoryIndex /cgi-bin/index.cgi index.html index.html.var
* systemctl enable httpd
* systemctl start httpd
* Create the file /var/www/html/robots.txt with the following:
> User-agent: *
> <br>
> Disallow: /

<h1>ISFDB Database Backup</h1>
Download the latest ISFDB backup. The most recent links are stored on the Wiki
<br>
https://www.isfdb.org/wiki/index.php/ISFDB_Download_Archives
<br>
But that doesn't help you if the Wiki is down. Currently the most recent backup is at: 
<br>
https://drive.google.com/file/d/1dABQ7fIH3S-YL3P5_yLM8CHTLmOT4xog/view?usp=drive_link
<br>

<h1>MySQL</h1>
Download and install MySQL. Do the following:

* dnf update
* dnf module enable mysql:8.0
* dnf install @mysql
* systemctl enable mysqld
* systemctl start mysqld
* Issue: mysql
* While in mysql, issue the command: create database isfdb;
* While in mysql, issue the command: use isfdb;
* While in mysql, issue the command: alter database isfdb character set latin1 collate latin1_swedish_ci;
* While in mysql, issue the command: source <<backupfile>>;'
* create user isfdb1@localhost identified by 'PASSWORD';
* GRANT ALL PRIVILEGES ON isfdb.* TO 'isfdb1'@'localhost';
* SET GLOBAL sql_mode = 'NO_ENGINE_SUBSTITUTION';"
* Add the following line to the end of /etc/my.cnf.d/community-mysql-server.cnf:
> binlog-expire-logs-seconds=259200
* and restart MySQL (systemctl restart mysqld); this will ensure that MySQL's binary log files are automatically purged after 3 days as opposed to the default value (30 days)

<h1>Python 2.7.18</h1>
This github repo is supposed to support Python3, but we aren't there yet. When we are, we'll change the instructions here:

* dnf install python2
* dnf install python2-devel
* dnf install mysql-devel
* python2 -m ensurepip --no-default-pip
* pip install --upgrade pip
* pip2 install mysqlclient
* alternatives --install /usr/bin/python python /usr/bin/python3.9 2
* alternatives --install /usr/bin/python python /usr/bin/python2.7 1
* alternatives --config python
* python --version

<h1>ISFDB</h1>
These instructions will also change when the code work is complete in the github repo.

* In home directory:
> svn checkout https://svn.code.sf.net/p/isfdb/code-svn/trunk isfdb-code-svn
* Update common/localdefs.py (using your new IP address):
> COOKIEHOST = "67.225.129.86"
> <br>
> HTFAKE = "/67.225.129.86/cgi-bin"
> <br>
> HTMLHOST = "67.225.129.86"
> <br>
> HTMLLOC = "67.225.129.86"
> <br>
> PASSWORD = "PASSWORD"
> <br>
> USERNAME = "isfdb1"
> <br>
> WIKILOC = "67.225.129.86/wiki"
* make

<h1>PHP</h1>
PHP is a prerequisite for MediaWiki. To install:

* dnf module reset php
* dnf module enable php:7.4
* dnf install php php-common php-opcache php-cli php-gd php-curl php-mysqlnd
* systemctl start php-fpm
* systemctl enable php-fpm
* php -v
* systemctl stop httpd
* systemctl start httpd

<h1>Add Users</h1>
Add the necessary users to the new system. These are the users that will administer the website, so the number of users should be relatively small.
Give them sudo access by adding them to the wheel group.

<h1>MediaWiki</h1>
Install the Wiki:

* cd to /var/www/html
* Fetch the current stable long-term support release of MediaWiki:
> wget https://releases.wikimedia.org/mediawiki/1.35/mediawiki-1.35.6.zip
* unzip mediawiki-1.35.6.zip
* mv mediawiki-1.35.6 wiki
* cd wiki && place the old isfdb version of LocalSettings.php here
* Edit LocalSettings.php and make the follow changes:
> Change wgServer
> <br>
> Change wgDBuser
> <br>
> Change wgDBpassword
> <br>
> Comment out the ConfirmEdit extension
> <br>
> Comment out the SyntaxHighlight extension
> <br>
> Comment out the SVGtag extension
* mkdir wiki/images
* chown apache images
* chgrp apache images
* Copy all image subdirectory content from isfdb.org:/var/www/html/wiki/images to the new server.
* php maintenance/update.php
* Wait a very long time for the update to finish (about 3.5 hours). This will perform hundreds of thousands of revision updates, but it issues a constant stream of progress lines. There is a web-based alternative, but I recommend against that, as the long processing time will generate a 504 error from Apache.
It helps to ssh into the system with the "-o ServerAliveInterval=600" option, which will generate a null keep alive packet every 10 minutes, keeping the session alive.
* cp isfdb.gif to wiki/skins/common/images
* Add the following lines to the end of LocalSettings.php and remove the old commented out versions:
* wfLoadSkin( 'Vector' );
* wfLoadExtension( 'ConfirmEdit' );
* wfLoadExtension( 'SyntaxHighlight_GeSHi' );
* wfLoadExtension( 'WikiEditor' );
* $wgExtraSignatureNamespaces = [ NS_MAIN, NS_USER, NS_TALK, NS_PROJECT ];
* Uncomment and change to: $wgImageMagickConvertCommand = "/usr/bin/convert";
* Uncomment and change to: $wgLogo = "$wgStylePath/common/images/isfdb.gif";
