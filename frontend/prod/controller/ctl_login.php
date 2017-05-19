<?php

namespace VortexAI\Kurgan;

require_once(__DIR__ . '/' . 'ctl_user.php');

$username = $_REQUEST['username'];
$password = $_REQUEST['password'];

$user = new K_User();
$authenticated = $user->login($username, $password);

session_start();

if($authenticated == 1){
  $_SESSION['authenticated']=1;
  $user->set_login($username);
  $last_ip = $_SERVER['REMOTE_ADDR']; //todo get proxy
  $user_agent = $_SERVER['HTTP_USER_AGENT'];
  $user->set_db_last_login($last_ip, $user_agent);
  $_SESSION['login']=$username;
  $_SESSION['last_ip']=$last_ip;
  $last_login = $user->get_db_last_login($username);
  $_SESSION['last_login']=$last_login;

}
else {
  $_SESSION['authenticated']=-1;
}

header("Location: ../index.php");

?>
