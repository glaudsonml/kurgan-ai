<?php
	namespace VortexAI\Kurgan;

	require_once(__DIR__ . "/" . "../config.php");
	require_once(__DIR__ . "/" . "ctl_utils.php");

	function agent_request_all_loaded(){
		$server = $GLOBALS['stomp_proto'] . '://' . $GLOBALS['stomp_host'] . ':' . $GLOBALS['stomp_port'];
		$user = $GLOBALS['stomp_user'];
		$password = $GLOBALS['stomp_pass'];
		$channel = $GLOBALS['stomp_channel'];

		$con = new \Stomp($server, $user, $password);
		if (!$con) {
		   die('Connection failed: ' . stomp_connect_error());
		}

		$connectionid = RandomInt(4);
		$reply_with = RandomString(5);

		$msg = "(request\n\t:sender KurganFrontend\n\t:receiver All\n\t:reply-with $reply_with\n\t:conversation-id $connectionid\n\t:content Request Information (= (agents-available) (*))\n\n)\n";
		$con->send($channel, $msg);
		$con->subscribe($channel);

		$content = '';

		while ($con->hasFrame()){
       			$frame = $con->readFrame();
			if ($frame->body === $msg) {
				$con->ack($frame);
			}
			else {
				$content = $frame->body . "\n";
	                        //file_put_contents("/tmp/stomp.log",$content,FILE_APPEND);
        	                //print "$content";
                	        $con->ack($frame);
			}
		}

		$con->unsubscribe($channel);

		/* handle content */

		$pattern = '/\(available-agent\).\((.*)\)\)/';
		preg_match($pattern, $content, $matches, PREG_OFFSET_CAPTURE, 3);
		return $matches[1];
	}

?>

