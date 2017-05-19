<?php
namespace VortexAI\Kurgan;

	require_once(__DIR__ . "/" . "../config.php");
	require_once(__DIR__ . "/" . "ctl_utils.php");


	function agent_request_pomdp($url_target){

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
	$msg1 = "(inform\n\t:sender KurganFrontend\n\t:receiver AgentTarget\n\t:reply-with $reply_with\n\t:conversation-id $conversationid\n\t:content Request Information (= (base-url-target) ($url_target))\n\n)\n";
	
	stomp_begin($link, 't1');
	stomp_send($link, $channel, $msg1, array('transaction' => 't1'));
	stomp_commit($link, 't1');
	stomp_subscribe($link, $channel);
	$frame = stomp_read_frame($link);
	if ($frame['body'] === $msg1) {
		stomp_ack($link, $frame['headers']['message-id']);
                        }
                        else {
                             $content = $frame['body'] . "\n";
                                //print "$content";
                        }

	stomp_close($link);

	$content = '';
        $link = stomp_connect($server, $user, $password);
        if (!$link) {
            die('Connection failed: ' . stomp_connect_error());
        }

        $conversationid = RandomInt(4);
        $reply_with = RandomString(5);
	$msg2 = "(request\n\t:sender KurganFrontend\n\t:receiver MasterAgent\n\t:reply-with $reply_with\n\t:conversation-id $conversationid\n\t:content Request Information (= (run-pomdp) (*))\n\n)\n";

        stomp_begin($link, 't2');
        stomp_send($link, $channel, $msg2, array('transaction' => 't2'));
        stomp_commit($link, 't2');
        stomp_subscribe($link, $channel);
	while($frame = stomp_read_frame($link)){
        if ($frame['body'] === $msg2) {
                stomp_ack($link, $frame['headers']['message-id']);
                        }
                        else {
				//all content below
                             //$content.= $frame['body'] . "\n";
                             $content = $frame['body'];
 //                               print "$content";
                        }
	sleep(1);
	}

	stomp_close($link);
	$content = trim(preg_replace('/~[\n]+~/',' ', $content));
        $pattern = '/Best-Action:.(.*)+/';
        preg_match($pattern, $content, $matches, PREG_OFFSET_CAPTURE, 3);
	$response1 = preg_replace('/[0-9]+/','', $matches[0][0]);

        $pattern2 = '/Data Returned:.(.*)+/';
        preg_match($pattern2, $content, $matches, PREG_OFFSET_CAPTURE, 3);
        $response2 = $matches[0][0];

	$response = $response1 . "|" . $response2;
        return $response;


}
/*



	try {
		$server = $GLOBALS['stomp_proto'] . '://' . $GLOBALS['stomp_host'] . ':' . $GLOBALS['stomp_port'];
		$user = $GLOBALS['stomp_user'];
		$password = $GLOBALS['stomp_pass'];
		$channel = $GLOBALS['stomp_channel'];

		$con = new \Stomp($server, $user, $password);
		if (!$con) {
		   die('Connection failed: ' . stomp_connect_error());
		}

                $conversationid = RandomInt(4);
                $reply_with = RandomString(5);


		$msg1 = "(inform\n\t:sender KurganFrontend\n\t:receiver AgentTarget\n\t:reply-with $reply_with\n\t:conversation-id $conversationid\n\t:content Request Information (= (base-url-target) ($url_target))\n\n)\n";
                $con->send($channel, $msg1);
                $con->subscribe($channel);

               if ($con->hasFrame()){
                        $frame = $con->readFrame();
                        if ($frame->body === $msg1) {
                                $con->ack($frame);
                        }
                        else {
                                $content = $frame->body . "\n";
                                file_put_contents("/tmp/stomp.log",$content,FILE_APPEND);
                                print "$content";
                               $con->ack($frame);
                        }
                }

		$con->unsubscribe($channel);
	}
	catch (Exception $e)
    	{
		$msg_error = $e->getMessage();
		file_put_contents("/tmp/stomp_error.log", $msg_error, FILE_APPEND);
	}

	try {
                $con2 = new \Stomp($server, $user, $password);
                if (!$con2) {
                   die('Connection failed: ' . stomp_connect_error());
                }

                $conversationid = RandomInt(4);
                $reply_with = RandomString(5);

		$msg = "(request\n\t:sender KurganFrontend\n\t:receiver MasterAgent\n\t:reply-with $reply_with\n\t:conversation-id $conversationid\n\t:content Request Information (= (run-pomdp) (*))\n\n)\n";
		$con2->send($channel, $msg);
		$con2->subscribe($channel);

		$content = '';

//		if ($con2->hasFrame()){
		while ($con2->hasFrame()){
       			$frame = $con2->readFrame();
			if ($frame->body === $msg) {
				$con2->ack($frame);
			}
			else {
				$content = $frame->body . "\n";
	                        //file_put_contents("/tmp/stomp.log",$content,FILE_APPEND);
        	                print "$content";
                	        $con2->ack($frame);
			}
			sleep(3);
		}

		$con2->unsubscribe($channel);
		unset($con2);
       		}
        catch (Exception $e)
        {
                $msg_error = $e->getMessage();
                file_put_contents("/tmp/stomp_error.log", $msg_error, FILE_APPEND);
        }


                $pattern = '/\(run-pomdp\).\((.*)\)\)/';
                preg_match($pattern, $content, $matches, PREG_OFFSET_CAPTURE, 3);
                return $matches[1];

	}
*/
?>

