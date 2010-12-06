<?php
/* CONFIG START. DO NOT CHANGE ANYTHING IN OR AFTER THIS LINE. */
// $Horde: imp/config/conf.xml,v 1.53.2.43 2009-07-02 06:18:15 slusarz Exp $
$conf['user']['allow_accounts'] = true;
$conf['user']['select_sentmail_folder'] = true;
$conf['user']['allow_folders'] = true;
$conf['user']['allow_resume_all'] = false;
$conf['user']['allow_view_source'] = true;
$conf['user']['select_view'] = true;
$conf['server']['server_list'] = 'none';
$conf['server']['fixed_folders'] = array();
$conf['msgsettings']['filtering']['words'] = './config/filter.txt';
$conf['msgsettings']['filtering']['replacement'] = '****';
$conf['spam']['reporting'] = false;
$conf['notspam']['reporting'] = false;
$conf['print']['add_printedby'] = true;
$conf['compose']['allow_receipts'] = true;
$conf['compose']['use_vfs'] = true;
$conf['compose']['link_all_attachments'] = false;
$conf['compose']['link_attachments_notify'] = true;
$conf['compose']['link_attachments'] = true;
$conf['compose']['attach_size_limit'] = 0;
$conf['compose']['attach_count_limit'] = 0;
$conf['compose']['convert_to_related'] = true;
$conf['compose']['reply_limit'] = 200000;
$conf['compose']['ac_browser'] = 200;
$conf['compose']['ac_threshold'] = 3;
$conf['maillog']['use_maillog'] = false;
$conf['sentmail']['driver'] = 'Null';
$conf['tasklist']['use_tasklist'] = true;
$conf['notepad']['use_notepad'] = true;
$conf['dimp']['viewport']['buffer_pages'] = 10;
$conf['dimp']['viewport']['viewport_wait'] = 10;
$conf['menu']['apps'] = array();
/* CONFIG END. DO NOT CHANGE ANYTHING IN OR BEFORE THIS LINE. */