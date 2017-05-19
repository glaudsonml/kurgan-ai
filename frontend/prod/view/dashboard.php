<?php
	namespace VortexAI\Kurgan;
	session_start();
	if($_SESSION['authenticated'] != 1){
		session_destroy();
		header("Location: ../index.php");
		exit;
	}
	else {
		require_once("../controller/ctl_utils.php");
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
			<li><span class="active">Dashboard</span></li>
			<li><a href="users.php">Users</a></li>
			<li><a href="configurations.php">Configurations</a></li>
			<li><a href="statistics.php">Statistics</a></li>
			<li><a href="reports.php">Reports</a></li>
			<li><a href="agents.php">Agents</a></li>
			<li><a href="help.php">Help</a></li>
			<li><a href="logout.php">Logout</a></li>
		</ul>
<?php

?>
			<div id="content" class="container_16 clearfix">
				<div class="grid_5">
					<div class="box">
						<h2><?php print($_SESSION['login']); ?></h2>
						<div class="utils">
							<a href="#">View More</a>
						</div>
						<p><strong>Last Signed In : </strong> <?php print($_SESSION['last_login']); ?><br /><strong>IP Address : </strong> <?php print($_SESSION['last_ip']); ?></p>
					</div>
					<div class="box">
						<h2>System</h2>
						<table>
							<tbody>
								<tr>
									<td align="left"><img src="images/cpu2.jpeg"></img></td>
									<td>CPU Usage</td>
									<td><?php echo getCpuUsage(); ?>%</td>
								</tr>

								<tr>
									<td align="left"><img src="images/hd.jpeg"></img></td>
									<td>Disk Usage</td>
									<td><?php echo getDiskUsage(); ?>%</td>
								</tr>

								<tr>
									<td align="left"><img src="images/network.jpeg"></img></td>
									<td>Memory Usage</td>
									<td><?php echo getMemoryUsage(); ?>%</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="box">
						<h2>Kurgan Updates</h2>
						<div class="utils">
							<a href="upgrade.php">Check</a>
						</div>
						<p class="center">You are running the latest free version.</p>
						<p class="center"><a href="upgrade.php">Upgrade Now.</a></p>
					</div>
				</div>
				<div class="grid_6">
					<div class="box">
						<h2>Vulnerabilities</h2>
						<div class="utils">
							<a href="#">View More</a>
						</div>
						<table>
							<tbody>
								<tr>
									<td>1 SQL Injection</td>
									<td><a href="#">More Information</a></td>
								</tr>
								<tr>
									<td>1 XSRF</td>
									<td><a href="#">View More</a></td>
								</tr>
								<tr>
									<td>1 XSS</td>
									<td>0 Pending</td>
								</tr>
								<tr>
									<td>0 LFI/RFI</td>
									<td>0 Pending</td>
                                                                </tr>
								 <tr>
                                                                        <td>1 Others</td>
                                                                        <td><a href="#">View More</a></td>
								</tr>


							</tbody>
						</table>
					</div>

<?php
        require_once(__DIR__ . "/" . "../controller/ctl_scan.php");
        $scan = new K_Scan();
        $my_last_scan = $scan->get_db_last_scan();
	if ($my_last_scan == NULL){
	        $id_scan = 0;
        	$url_scan = "http://www.kurgan.com.br/";
	}
	else {
        	$id_scan = $my_last_scan[0]['id'];
        	$url_scan = $my_last_scan[0]['url'];
	}
?>


					  <div class="box">
						 <h2>Latest Scan</h2>
                                                <div class="utils">
                                                        <a href="last_scan.php?id=<?php echo $id_scan; ?>">More Info.</a>
                                                </div>

                                                        <p><b><?php echo $url_scan; ?></b></p>
                                          </div>



					<div class="box">
						<h2>Quick Scan</h2>
						<div class="utils">
							<a href="#">Advanced</a>
						</div>
						<form action="agents_pomdp.php" method="post">
							<p>
								<label for="post">Host Target <small>(Domain ,IP or URL.)</small> </label>
								<input type="text" name="target" />
							</p>
							<p>
							<center>	<input type="submit" value="Scan" /></center>
							</p>
						</form>
					</div>
				</div>
				<div class="grid_5">
					<div class="box">
						<h2>Statistics</h2>
						 <div class="utils">
                                                        <a href="#">View More</a>
                                                </div>

						<table>
							<tbody>
								<tr>
									<td>Critical</td>
									<td>+ 120%</td>
								</tr>
								<tr>
									<td>Warning</td>
									<td>+ 220%</td>
								</tr>
								<tr>
									<td>Low</td>
									<td>- 10%</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="box">
						<h2>Agents Info</h2>
						<div class="utils">
							<a href="agents.php">View More</a>
						</div>
						<table class="date">
							<thead>
								<tr>
							 <p align="center">Messages from Multi-Agents</p>
								
								</tr>
							</thead>
							<tbody>
								<tr>
								<p>
								<b>16:10</b> - MasterAgent ready to receive url.<BR>
								<b>16:09</b> - Finished Analysis of www.vortex-ai.com.br.<BR>
								</p>

								</tr>
								<tr>
								<p>16:09 - Finished Analysis of www.vortex-ai.com.br.</p>
								</tr>
							</tbody>
						</table>
						<ol>
							<li>16:09 - Finished Analysis of www.vortex-ai.com.br.</li>
							<li>14:45 - Running Crawling against www.vortex-ai.com.br.</li>
							<li>14:40 - Running Brute Force Login against www.vortex-ai.com.br.</li>
						</ol>
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
