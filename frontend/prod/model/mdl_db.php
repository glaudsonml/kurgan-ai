<?php
	namespace VortexAI\Kurgan;

	require_once(__DIR__ . '/' . "../config.php");
	require_once(__DIR__ . '/' . 'mdl_log.php');

	class K_Database {

                private $hostname = '';
                private $username = '';
                private $password = '';
                private $database = '';
                public $connection = NULL;

		function __construct(){
	        	$this->hostname = $GLOBALS['db_host'];
        	        $this->username = $GLOBALS['db_user'];
                	$this->password = $GLOBALS['db_pass'];
                	$this->database = $GLOBALS['db_name'];
		}


		public function connect(){
			$this->connection = mysql_connect($this->hostname, $this->username, $this->password);
			if($this->connection === false){
				$log = new K_log();
				$msg = sprintf("Database Connection Error: %s", mysql_error());
				$log->log($msg);
				return NULL;
			}
			$d = mysql_select_db($this->database, $this->connection);
			if($d === false){
                                $log = new K_log();
                                $msg = sprintf("Database Connection Error: %s", mysql_error());
                                $log->log($msg);
                                return NULL;
			}

			return $this->connection;
		}

		public function disconnect(){
			$d = mysql_close($this->connection);
			if($d === false){
				$log = new K_log();
                                $log->log('Database Disconnection Error!');
                                return false;
			}
		}


		public function get_dbname(){
			$c = $this->connect();
			if($c != NULL){
				$query = "SELECT DATABASE()";
				$result = mysql_query($query, $c);
				if($result === false){
					$log = new K_log();
					$msg = sprintf("Database Query Error: %s", mysql_error());
                                	$log->log($msg);
					return false;
				}	

				$row = mysql_fetch_row($result);
			        //print $row[0];
				return $row[0];
			}
		}

		public function send($query){
			$c = $this->connect();
			$val = '';
			if($this->connection != NULL){
				$result = mysql_query($query, $this->connection);
                                if(!$result){
                                        $log = new K_log();
                                        $msg = sprintf("Database Query Error: %s", mysql_error($this->connection));
                                        $log->log($msg);
                                        return false;
                                } else {
					$lines = mysql_num_rows($result);
					$columns = mysql_num_fields($result);

					for($i=0; $i < $columns; $i++){
						$col = mysql_fetch_field($result, $i);
						for($j=0; $j < $lines; $j++){
		                                	$row = mysql_result($result,$j,$i);
							$val[$j][$col->name] = $row;
						}
					}
				}
				//this->disconnect();

			}
			return $val;
		}


                public function get_data($table,$fields,$where,$orderby,$limit){
			$v = '';
			if($this->connection == NULL){
				$c = $this->connect();
			}
                        if($this->connection != NULL){
                                $query = "SELECT $fields FROM $table";
                                if(is_null($where) == FALSE){
                                        $query = $query . " WHERE $where";
                                }
				if(is_null($orderby) == FALSE){
					$query = $query . " ORDER BY $orderby";
				}
                                if(is_null($limit) == FALSE){
                                        $query = $query . " LIMIT $limit";
                                }
                                $v = $this->send($query);
			}
			return $v;
                }



                public function insert_data($table,$fields,$values){
                        $v = '';
                        $c = $this->connect();
                        if($this->connection != NULL){
                                $query = "INSERT INTO $table ($fields) VALUES($values)";
				$result = mysql_query($query, $this->connection);
                                if(!$result){
                                        $log = new K_log();
                                        $msg = sprintf("Database Query Error: %s", mysql_error($this->connection));
                                        $log->log($msg);
                                        return false;
				}
//                                $v = $this->send($query);
                        }
                        return $v;
                }



                public function auth($user, $pass){
                        $c = $this->connect();
                        if($c != NULL){
				// make satement anti sql injection
                                $query = "SELECT login FROM users WHERE login=\"$user\" AND pass=SHA1(\"$pass\") LIMIT 1";
                                $result = mysql_query($query, $c);
                                if($result === false){
                                        $log = new K_log();
                                        $msg = sprintf("Database Query Error: %s", mysql_error);
                                        $log->log($msg);
                                        return false;
                                } 
				$lines = mysql_num_rows($result);
                                $row = mysql_fetch_row($result);
				if("$row[0]" == "$user") {
	                                return true;
				}
				else {
					syslog(LOG_ERR,"Authentication Failure!");
					return false;
				}

                        }
                }




	}

?>
