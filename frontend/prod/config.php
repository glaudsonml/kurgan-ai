<?php

namespace VortexAI\Kurgan;

/* Database Config */
$GLOBALS['db_user'] = "kurgan";
$GLOBALS['db_pass'] = "29kurgan29";
$GLOBALS['db_name'] = "kurgan";
$GLOBALS['db_host'] = "127.0.0.1";
$GLOBALS['db_port'] = 3306;

/* Logger Config */
$GLOBALS['log_file'] = "/var/log/apache/error.log";

/* Stomp server and credentials */

$GLOBALS['stomp_proto'] = 'tcp';
$GLOBALS['stomp_host'] = '192.168.2.33';
$GLOBALS['stomp_port'] = 61613;
$GLOBALS['stomp_user'] = 'admin';
$GLOBALS['stomp_pass'] = 'KuRg4nLives!';
$GLOBALS['stomp_channel'] = '/topic/kurgan';

?>
