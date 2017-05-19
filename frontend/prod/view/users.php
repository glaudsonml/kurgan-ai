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
                        <li><span class="active">Users</span></li>
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
						<h2>Users</h2>
						 <div class="utils">
                                                        <a href="user_add.php">+</a>
                                                </div>

						<table>
							<tbody>

								<tr>
									<td align="center"><h2>Login</h2></td>
									<td align="center"><h2>Last Access</h2></td>
									<td align="center"><h2>Remote IP</h2></td>
								</tr>

<?php
        require_once(__DIR__ . "/" . "../controller/ctl_users.php");
        $users = new K_Users();
        $all_users = $users->get_all_users();
	for($i = 0; $i < count($all_users); $i++){
		$idlogin = $all_users[$i]['id'];
		$last_login = $users->get_last_login($idlogin);
		$last_ip = $users->get_last_ip($idlogin);
?>


								<tr>
									<td align="center"><a href="/view/user_edit.php?id=<?php print $all_users[$i]['id']; ?>"><?php print $all_users[$i]['login']; ?></a></td>
									<td align="center"><?php print $last_login; ?></td>
									<td align="center"><?php print $last_ip; ?></td>
								</tr>

<?php
	}
?>

							</tbody>
						</table>
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
