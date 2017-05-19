<?php
	namespace VortexAI\Kurgan;
	require_once(__DIR__ . '/' . '../model/mdl_db.php');

	Class K_User {
		private $id = '';
		private $login = '';
		private $pass = ''; // we really need this?
		private $last_login = '';
		private $last_ip = '';
		private $level = '';
		private $enabled = '';


		public $authenticated = '';

		public function getname(){
			$db = new K_Database();
			$my_db = $db->get_dbname();
			//print "Dbname: $my_db";
		}

		public function login($username, $password){
			$this->authenticated = 0;
			$db = new K_Database();
			$res = $db->auth($username,$password);
			if($res == true){
				$this->authenticated = 1;
				$this->login = $username;
				$table = "users";
				$fields = "id";
				$where = "login=\"$this->login\"";
				$limit = "1";
				$res = $db->get_data($table,$fields,$where,NULL,$limit);
				$this->id = $res[0]['id'];
			}
			else {
				$this->authenticated = -1;
				$this->login = '';
			}
			return $this->authenticated;
		}


		public function set_db_last_login($last_ip, $user_agent){
			$idlogin = $this->id;
			$db = new K_Database();
			$table = "last_login";
			$fields = "idlogin,last_login,last_ip,user_agent";
			$values = "$idlogin,now(),\"$last_ip\",\"$user_agent\"";
			$res = $db->insert_data($table,$fields,$values);
			return $res;
		}

               public function get_db_last_login($login){
                        $idlogin = $this->id;
                        $db = new K_Database();
			$table = "last_login";
                        $fields = "last_login";
                        $where = "idlogin=$idlogin";
			$orderby = "id DESC";
                        $limit = "1,1";
                        $res = $db->get_data($table,$fields,$where,$orderby,$limit);
                        $this->last_login = $res[0]['last_login'];
                        return $this->last_login;
                }


                public function get_id(){
                        return $this->id;
                }
                public function set_id($val){
                        $this->id = $val;
                }

		public function get_login(){
			return $this->login;
		}
		public function set_login($val){
			$this->login = $val;
		}

         	public function get_last_login(){
                        return $this->last_login;
                }
                public function set_last_login($val){
                        $this->last_login = $val;
                }
                public function get_last_ip(){
                        return $this->last_ip;
                }
                public function set_last_ip($val){
                        $this->last_ip = $val;
                }

                public function get_level(){
                        return $this->level;
                }
                public function set_level($val){
                        $this->level = $val;
                }

                public function get_enabled(){
                        return $this->enabled;
                }
                public function set_enaled($val){
                        $this->enabled = $val;
                }

/*
		public function get_user(){
			$table = "user";
			$fields = "id,login,last_login,last_ip,level,enabled";
			$where = "login=\"$this->login\";
			$limit = "1";
			$data = get_data($table,$fields,$where,$limit);
			$log = new K_log();
                        $msg = sprintf("Data: %s", var_dump($data));
                        $log->log($msg);
		}

               public function get_all_users(){
                        $table = "user";
                        $fields = "id,login,last_login,last_ip,level,enabled";
                        $where = "login=\"$this->login\";
                        $limit = "1";
                        $data = get_data($table,$fields,$where,$limit);
                        $log = new K_log();
                        $msg = sprintf("Data: %s", var_dump($data));
                        $log->log($msg);
                }

*/

	}
?>
