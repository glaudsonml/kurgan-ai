<?php
if(isset($_REQUEST['auth'])){
	$auth = $_REQUEST['auth'];
	if($auth == -1){
        	print "<script>alert(\"Authentication Failed.\")</script>";
	}
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
		</ul>

			<div id="content" class="container_16 clearfix" align="center">
				<div class="grid_17">
					<div class="box">
						<h2>Login:</h2>
						<form action="../controller/ctl_login.php" method="post">
							<p>
								<label for="post">Username:</label>
								<input type="text" name="username" autofocus/>
							</p>

							<p>
                                                                <label for="post">Password:</label>
                                                                <input type="password" name="password" />
                                                        </p>

							<p>
							<center>	<input type="submit" value="Send" /></center>
							</p>
						</form>
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
