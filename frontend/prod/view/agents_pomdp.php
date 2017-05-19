<?php
	namespace VortexAI\Kurgan;
	session_start();
	if($_SESSION['authenticated'] != 1){
		session_destroy();
		header("Location: ../index.php");
		exit;
	}

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
		<title>Kurgan AI - Web Application Security Framework</title>
		<link rel="stylesheet" href="css/960.css" type="text/css" media="screen" charset="utf-8" />
		<link rel="stylesheet" href="css/template.css" type="text/css" media="screen" charset="utf-8" />
		<link rel="stylesheet" href="css/colour.css" type="text/css" media="screen" charset="utf-8" />
		<!--[if IE]><![if gte IE 6]><![endif]-->
		<script src="js/glow/1.7.0/core/core.js" type="text/javascript"></script>
		<script src="js/glow/1.7.0/widgets/widgets.js" type="text/javascript"></script>
		<script src="js/jquery.js" type="text/javascript"></script>
		<link href="js/glow/1.7.0/widgets/widgets.css" type="text/css" rel="stylesheet" />
		<script type="text/javascript">
			glow.ready(function(){
				new glow.widgets.Sortable(
					'#content .grid_5, #content .grid_6',
					{
						draggableOptions : {
							handle : 'h2'
						}
					}
				);
			});
		</script>
		<!--[if IE]><![endif]><![endif]-->
	</head>
	<body>

		<h1 id="head">
			<div class="areaImagem">
			    <img class="img" src="images/logo2.png" />
		</div>
			<div class="areaTexto">
				&nbsp;&nbsp;Kurgan AI - Web Application Security Framework
			</div>
		</h1>
			
		
		<ul id="navigation">
			<li>&nbsp;&nbsp;</li>
			<li><a href="dashboard.php">Dashboard</a></li>
			<li><a href="users.php">Users</a></li>
			<li><a href="configurations.php">Configurations</a></li>
			<li><a href="statistics.php">Statistics</a></li>
			<li><a href="reports.php">Reports</a></li>
			<li><a href="agents.php">Agents</a></li>
			<li><a href="help.php">Help</a></li>
			<li><a href="logout.php">Logout</a></li>
		</ul>

			<div id="content" class="container_16 clearfix" align="center">
				<div class="grid_18">
					<div class="box">
						<h2>Agent POMDP</h2>
						<table>
							<tr> </tr>
       <div id=''>Response From Agent: </div>
	<div id='' align='center'><img src=images/masterAgent.png></div>
							<tr> </tr>

<?php
        require_once(__DIR__ . "/" . "../controller/ctl_agent_send_pomdp.php");
$target = $_POST['target'];
if ($target != NULL){
      	$retorno = agent_request_pomdp($target);
	//print_r($retorno);
	$pieces = explode("|",$retorno,2);
        foreach ($pieces as $key => $value) {
               echo "<div id='' align='center'><tr><b>$value</b></tr></div>\n";
	}
}
else {
        print "Without url target!";
}
?>
							<tr>
							<BR>
							</tr>


							</tbody>
						</table>

<script>
$(document).ready(function() {  

var atualizaDiv = setInterval(function(){
$('#tabela').fadeOut("slow").load('../controller/ctl_agents.php',{},function(retorno){
$('#tabela').html(retorno);
$('#tabela').fadeIn("slow")
});
       }, 2000
   );
});
</script>

<div class="box">
    <h2>Agents Communications</h2>
	<table>
		<tbody>
			<tr><div id='tabela'> </div></tr>
		</tbody>
	</table>
</div>


					</div>

				</div>
			</div>
		<div id="foot">
			<div class="container_16 clearfix">
				<div class="grid_16" align="center">
					Copyright &copy; 2017. Vortex AI
				</div>
			</div>
		</div>
	</body>
</html>
