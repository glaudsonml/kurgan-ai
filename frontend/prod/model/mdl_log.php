<?php
	namespace VortexAI\Kurgan;

	require_once(__DIR__ . "/" . "../config.php"); 

	Class K_Log {
		private $file = '';

		function __construct(){
			$this->file = $GLOBALS['log_file'];
		}
		
		public function log($msg){
			openlog($this->file, LOG_PID | LOG_PERROR, LOG_LOCAL0);
			syslog(LOG_ERR, $msg);
			closelog();
		}
	}
?>
