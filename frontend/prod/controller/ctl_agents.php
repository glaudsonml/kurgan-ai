<?php
namespace VortexAI\Kurgan;
	require_once(__DIR__ . "/" . "../config.php");
/*
	require_once(__DIR__ . "/" . "ctl_utils.php");
	function agentPHP(){

		$server = $GLOBALS['stomp_proto'] . '://' . $GLOBALS['stomp_host'] . ':' . $GLOBALS['stomp_port'];
		 $user = $GLOBALS['stomp_user'];
                $password = $GLOBALS['stomp_pass'];
                $channel = $GLOBALS['stomp_channel'];

	$link = stomp_connect($server, $user, $password);
	if (!$link) {
	    die('Connection failed: ' . stomp_connect_error());
	}

        $conversationid = RandomInt(4);
        $reply_with = RandomString(5);
	$msg1 = "(request\n\t:sender KurganFrontend\n\t:receiver AgentTarget\n\t:reply-with $reply_with\n\t:conversation-id $conversationid\n\t:content Request Information (= (base-url-target) (*))\n\n)\n";
	
	stomp_begin($link, 't1');
	stomp_send($link, $channel, $msg1, array('transaction' => 't1'));
	stomp_commit($link, 't1');
	stomp_subscribe($link, $channel);
	while($frame = stomp_read_frame($link)){
		if ($frame['body'] === $msg1) {
			stomp_ack($link, $frame['headers']['message-id']);
                        }
                        else {
                             $content = $frame['body'] . "\n";
                             print "$content";
                        }
	}
	stomp_close($link);
}
*/

	function agentPHP(){
		$server = $GLOBALS['stomp_proto'] . '://' . $GLOBALS['stomp_host'] . ':' . $GLOBALS['stomp_port'];
		$user = $GLOBALS['stomp_user'];
		$password = $GLOBALS['stomp_pass'];
		$channel = $GLOBALS['stomp_channel'];

		$con = new \Stomp($server, $user, $password);
		if (!$con) {
		   die('Connection failed: ' . stomp_connect_error());
		}
	

		$con->subscribe($channel);
		sleep(1);
		while ($con->hasFrame()){
       			$frame = $con->readFrame();
		//	if ($frame->body === $msg) {
		//		$con->ack($frame);
		//	}
		//	else {
				$content = $frame->body . "\n";
	                        file_put_contents("/tmp/stomp.log",$content,FILE_APPEND);
        	                print "$content";
                	        $con->ack($frame);
		//	}
		}

		$con->unsubscribe($channel);
	}

agentPHP();
?>

