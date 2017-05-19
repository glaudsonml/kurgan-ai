<?php
	namespace VortexAI\Kurgan;

	require_once("./config.php");
	require_once('controller/ctl_user.php');

	session_start();

	if((isset($_SESSION['authenticated']) == FALSE) || (empty($_SESSION['authenticated']) == TRUE)){
		header('Location: view/login.php');
		exit;

	}
	else {
		$ses = $_SESSION['authenticated'];
		if ($ses == 1){
			header('Location: view/dashboard.php');
			exit;
		}
		else {
			header('Location: view/login.php?auth=-1');
			exit;
		}
	}
?>
