<?php

$prefGroups['language'] = array(
    'column' => _("Your Information"),
    'label' => _("Locale and Time"),
    'desc' => _("Set your preferred language, timezone and date options."),
    'members' => array('language', 'timezone', 'twentyFour', 'date_format', 'date_input_format', 'first_week_day')
);

// date input format
// $_prefs['date_input_format'] = array(
//     'value' => 'year-month-day',
//     'locked' => false,
//     'shared' => true,
//     'type' => 'enum',
//     'enum' => array(
//         'day-month-year' => strftime('%d %b %Y'),
//         'month-day-year' => strftime('%b %d %Y'),
//         'year-day-month' => strftime('%Y %d %b'),
//         'year-month-day' => strftime('%Y %b %d'),
//     ),
//     'desc' => _("Choose order how to enter dates:"),
// );

// user full name for From: line
// If you lock this preference, you must specify a value or a hook for it in
// horde/config/hooks.php.
$_prefs['fullname'] = array(
    'value' => '',
    'locked' => false,
    'hook' => true,
    'type' => 'text',
    'desc' => _("Your full name:")
);

// user preferred email address for From: line
// If you lock this preference, you must specify a value or a hook for it in
// horde/config/hooks.php.
$_prefs['from_addr'] = array(
    'value' => '',
    'locked' => false,
    'hook' => true,
    'type' => 'text',
    'desc' =>  _("Your From: address:")
);

// UI theme
$_prefs['theme'] = array(
    'value' => 'silver',
    'locked' => false,
    'type' => 'select',
    'desc' => _("Select your color scheme.")
);

// what application should we go to after login?
// Application list is dynamically built when prefs screen is displayed
$_prefs['initial_application'] = array(
    'value' => 'imp',
    'type' => 'enum',
    'desc' => sprintf(_("What application should %s display after login?"), $GLOBALS['registry']->get('name'))
);
