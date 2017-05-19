<?php
        namespace VortexAI\Kurgan;
//      require_once("config.php");


        require_once(__DIR__ . '/' . 'mdl_log.php');
        require_once(__DIR__ . '/' . 'mdl_db.php');

        class K_User {
		private $db = '';
		public $db_connection = NULL;

		public __construct(){
			$db = new K_Database();	
			$db_connection = $db->connect()
		}

		public function get_data($table,$fields,$where,$limit){
			if($this->db_connection != NULL){
				$query = "SELECT $fields FROM $table";
				if(isnull($where) == FALSE){
					$query = $query . " WHERE $where";
				}
				if(isnull($limit) == FALSE){
					$query = $query . " LIMIT $limit";
				}

				$val = $this->db->send($query);
			 	$log = new K_log();
                                $msg = sprintf("Result: %s", var_dump($val));
                                $log->log($msg);

			}
		}
		
		public __destruct(){
			if(isnull(this->$db_connection) == FALSE){
				$this->db->disconnect($db_connection);
			}
		}

	}

?>
