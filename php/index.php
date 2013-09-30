<?php
include "functions.php";
include "classes/MyDB.class.php";
function my_autoloader($class) {
    include 'classes/' . strtolower($class) . '.class.php';
}

spl_autoload_register('my_autoloader');

	  
$sql = new mysql("[mydb]");
	
$sql->query("DELETE FROM ips WHERE last_seen_alive < '".date("Y-m-d H:i:s",strtotime("-10 seconds"))."'");

if ($_REQUEST['ip'] != "") {
	$ip_array = explode(":",$_REQUEST['ip']);
	$sql->query("INSERT INTO ips (ip_global,ip_local,ip_full,last_seen_alive,is_server) VALUES ('".$ip_array[0]."','".$ip_array[1]."','".$_REQUEST['ip']."','".date("Y-m-d H:i:s")."',0);");
	echo "inserted.";
	queries::printQueries();
}	
elseif ($_REQUEST['reset'] == '1') {
	$sql->query("DELETE FROM ips WHERE id >= 0;");
	echo "all entrees deleted.";
}
elseif ($_REQUEST['quit'] != "") {
	$sql->query("DELETE FROM ips WHERE ip_full = '".$_REQUEST['quit']."'");
	echo "quit received.";
}
elseif ($_REQUEST['alive'] != "") {
	$sql->query("UPDATE ips SET last_seen_alive = '".date("Y-m-d H:i:s")."' WHERE ip_full = '".$_REQUEST['alive']."'");
	echo "alive received.";
}
elseif ($_REQUEST['getServer'] == "1") {	
	$sql->query("SELECT ip_full FROM ips WHERE is_server = '1';");
	$data = $sql->fetchArray();
	
	if ($data === False) {
		$sql->query("SELECT * FROM ips WHERE is_server = '0'");
		$data2 = $sql->fetchArray();
		$sql->query("UPDATE ips SET is_server = 1 WHERE id = '".$data2[0]['id']."'");
		echo $data2[0]['ip_full'];		
	}
	else {
		echo $data[0]['ip_full'];
	}
}
else {
	echo '<html>
	<head>
		<script type="text/JavaScript">
			<!--
			function timedRefresh(timeoutPeriod) {
				setTimeout("location.reload(true);",timeoutPeriod);
			}
			//   -->
		</script>
		</head>
	<body onload="JavaScript:timedRefresh(2000);">';

	$sql->query("SELECT * FROM ips ORDER BY id DESC;");
	$data = $sql->fetchArray();

	if ($data === False) {
		echo "No entrees in database";
	}
	else {
		echo "<table border='1'>
				<tr>
					<td width='200px'>Global IP:</td>
					<td width='200px'>Local IP:</td>
					<td width='400px'>IP tag:</td>
					<td>last_seen_alive:</td>
					<td width='100px'>is_server:</td>
				</tr>";
		foreach($data as $row) {
			echo "<tr>
					<td>".$row['ip_global']."</td>
					<td>".$row['ip_local']."</td>
					<td>".$row['ip_full']."</td>
					<td>".$row['last_seen_alive']."</td>
					<td>".$row['is_server']."</td>
				</tr>";
		}
		echo  "</table>";
	}
	echo "<br /> <br />";
	queries::printQueries();
	
	echo "</body>
	</html>";
}
?>
