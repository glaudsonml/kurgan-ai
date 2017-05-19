<?php
	namespace VortexAI\Kurgan;
	require_once(__DIR__ . '/' . '../model/mdl_db.php');

	Class K_Scan {
		private $id = '';
		private $idlogin = '';
		private $time_executed = '';
		private $url = '';
		private $agent_output = '';


		public function getname(){
			$db = new K_Database();
			$my_db = $db->get_dbname();
		}


		public function set_db_last_scan($idlogin, $url, $agent_output){
			$idlogin = $this->id;
			$db = new K_Database();
			$table = "last_scan";
			$fields = "idlogin,time_executed,url,agent_output";
			$values = "$idlogin,now(),\"$url\",\"$agent_output\"";
			$res = $db->insert_data($table,$fields,$values);
			return $res;
		}



               public function get_db_last_scan(){
                        $db = new K_Database();
                        $table = "last_scan";
                        $fields = "idlogin,time_executed,url,agent_output";
                        $where = "1=1";
                        $orderby = "id DESC";
                        $limit = "1";
                        $res = $db->get_data($table,$fields,$where,$orderby,$limit);
                        #$this->last_login = $res[0]['last_login'];
			return $res;
                }


               public function get_db_last_scan_by_id($id){
                        $db = new K_Database();
			$table = "last_scan";
                        $fields = "idlogin,time_executed,url,agent_output";
                        $where = "id=$id";
			$orderby = "id DESC";
                        $limit = "1";
                        $res = $db->get_data($table,$fields,$where,$orderby,$limit);
                        return $res;
                }


                public function get_id(){
                        return $this->id;
                }
                public function set_id($val){
                        $this->id = $val;
                }


	}
?>
