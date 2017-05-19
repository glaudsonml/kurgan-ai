<?php
function RandomString($length) {
    $keys = array_merge(range(0,9), range('A', 'Z'));

    $key = "";
    for($i=0; $i < $length; $i++) {
        $key .= $keys[mt_rand(0, count($keys) - 1)];
    }
    return $key;
}

function RandomInt($length) {
    $keys = array_merge(range(0,9));

    $key = "";
    for($i=0; $i < $length; $i++) {
        $key .= $keys[mt_rand(0, count($keys) - 1)];
    }
    return $key;
}


function getMemoryUsage(){
	$fh = fopen('/proc/meminfo','r');
	$mem_total = 0;
	$mem_free = 0;
	while ($line = fgets($fh)) {
		$pieces = array();
		if (preg_match('/^MemTotal:\s+(\d+)\skB$/', $line, $pieces)) {
		$mem_total = $pieces[1];
		}
		if (preg_match('/^MemFree:\s+(\d+)\skB$/', $line, $pieces)) {
		$mem_free = $pieces[1];
		}
	}
	fclose($fh);

	$mem_used = $mem_total - $mem_free;
	$mf = ceil(($mem_used * 100) / $mem_total);
	return $mf;
}

function getDiskUsage(){
	$df_total = disk_total_space("/");
	$df_free = disk_free_space("/");

	$df_used = $df_total - $df_free;
	$df_perc = ceil(($df_used * 100) / $df_total);
	return $df_perc;
}

function getCpuUsage(){
	$cpu_load = sys_getloadavg();
	$cpu_used = $cpu_load[1];
	return $cpu_used;
}

?>

