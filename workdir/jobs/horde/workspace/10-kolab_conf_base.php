<?php

$conf['debug_level'] = E_ALL;

$conf['session']['use_only_cookies'] = true;

$conf['urls']['token_lifetime'] = 30;
$conf['urls']['hmac_lifetime'] = 30;
$conf['urls']['pretty'] = false;

$conf['tmpdir'] = dirname(__FILE__) . '/../../../../webclient4_data/tmp/';

$conf['menu']['links']['logout'] = 'authenticated';
$conf['menu']['links']['prefs'] = 'authenticated';
$conf['menu']['links']['help'] = 'authenticated';

$conf['sql']['database'] = dirname(__FILE__) . '/../../../../webclient4_data/storage/horde.db';
$conf['sql']['mode'] = '0640';
$conf['sql']['charset'] = 'utf-8';
$conf['sql']['phptype'] = 'sqlite';

$conf['auth']['driver'] = 'kolab';
$conf['auth']['admins'] = array();
$conf['auth']['checkip'] = true;
$conf['auth']['checkbrowser'] = true;
$conf['auth']['alternate_login'] = false;
$conf['auth']['redirect_on_logout'] = false;
$conf['auth']['list_users'] = 'list';
$conf['auth']['params']['login_block'] = false;

$conf['signup']['allow'] = false;

$conf['log']['priority'] = 'DEBUG';
$conf['log']['ident'] = 'HORDE';
$conf['log']['params'] = array();
$conf['log']['name'] = dirname(__FILE__) . '/../../../../webclient4_data/log/horde.log';
$conf['log']['params']['append'] = true;
$conf['log']['type'] = 'file';
$conf['log']['enabled'] = true;

$conf['prefs']['params']['directory'] = dirname(__FILE__) . '/../../../../webclient4_data/storage/';
$conf['prefs']['driver'] = 'file';

$conf['alarms']['params']['driverconfig'] = 'horde';
$conf['alarms']['params']['ttl'] = 300;
$conf['alarms']['driver'] = 'Sql';

$conf['group']['driver'] = 'kolab';
$conf['group']['cache'] = true;

$conf['perms']['driverconfig'] = 'horde';
$conf['perms']['driver'] = 'Sql';

$conf['share']['cache'] = true;
$conf['share']['driver'] = 'kolab';

$conf['cache']['default_lifetime'] = 1800;
$conf['cache']['params']['dir'] = $conf['tmpdir'];
$conf['cache']['params']['sub'] = 0;
$conf['cache']['driver'] = 'file';

$conf['mailer']['type'] = 'smtp';
$conf['mailer']['params']['auth'] = true;
$conf['mailer']['params']['port'] = 25;
// @todo: Reactivate for Kolab Server 2.3.*                                  //$conf['mailer']['params']['port'] = 587;                                   

$conf['token']['params']['token_dir'] = dirname(__FILE__) . '/../../../../webclient4_data/tmp';
$conf['token']['driver'] = 'file';

$conf['vfs']['params']['vfsroot'] = dirname(__FILE__) . '/../../../../webclient4_data/storage';
$conf['vfs']['type'] = 'file';

$conf['accounts']['driver'] = 'kolab';
$conf['accounts']['params']['attr'] = 'mail';
$conf['accounts']['params']['strip'] = false;

$conf['kolab']['ldap']['server'] = 'localhost';
$conf['kolab']['ldap']['port'] = 389;
$conf['kolab']['imap']['port'] = 143;
$conf['kolab']['imap']['sieveport'] = 2000;
$conf['kolab']['imap']['cache_folders'] = true;
$conf['kolab']['smtp']['server'] = 'localhost';
$conf['kolab']['smtp']['port'] = 25;
$conf['kolab']['misc']['multidomain'] = false;
$conf['kolab']['cache_folders'] = true;
$conf['kolab']['enabled'] = true;
$conf['kolab']['freebusy']['server'] = 'https://localhost/freebusy';

$conf['kolab']['session']['debug'] = true;
