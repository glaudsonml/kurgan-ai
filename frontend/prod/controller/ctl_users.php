<?php
	namespace VortexAI\Kurgan;

	require_once(__DIR__ . '/' . '../model/mdl_db.php');
	require_once(__DIR__ . '/' . 'ctl_user.php');

	Class K_Users {
		private $user = '';

		function __construct(){
			$this->user = new K_User();
		}

        	public function get_all_users(){
			$data = '';
			$db = new K_Database();
                        $table = "users";
                        $fields = "id,login,level,enabled";
			$where = NULL;
			$orderby = "id";
			$limit = NULL;
                        $data = $db->get_data($table,$fields,$where,$orderby,$limit);
			/*
			for($i = 0; $i < count($data); $i++){
	                        $log = new K_log();
        	                $msg = sprintf("Login: %s", $data[$i]['login']);
                	        $log->log($msg);
			}
			*/
			$db->disconnect();
			return $data;
                }

               public function get_last_login($idlogin){
                        $data = '';
                        $db = new K_Database();
                        $table = "last_login";
                        $fields = "last_login";
                        $where = "idlogin=$idlogin";
			$orderby = "id DESC";
                        $limit = "1,1";
                        $data = $db->get_data($table,$fields,$where,$orderby,$limit);
                        /*
                        for($i = 0; $i < count($data); $i++){
                                $log = new K_log();
                                $msg = sprintf("Login: %s", $data[$i]['login']);
                                $log->log($msg);
                        }
                        */
                        $db->disconnect();
                        return $data[0]['last_login'];
                }

              public function get_last_ip($idlogin){
                        $data = '';
                        $db = new K_Database();
                        $table = "last_login";
                        $fields = "last_ip";
                        $where = "idlogin=$idlogin";
                        $orderby = "id DESC";
                        $limit = "1,1";
                        $data = $db->get_data($table,$fields,$where,$orderby,$limit);
                       $db->disconnect();
                        return $data[0]['last_ip'];
                }



	}
?>
