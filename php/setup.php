<?php
include "functions.php";
function my_autoloader($class) {
    include 'classes/' . strtolower($class) . '.class.php';
}
spl_autoload_register('my_autoloader');
$sqli = new mysqli("localhost", "root", "", "[myDB]");

$sqli->query("DROP TABLE ips");
		
$query = "CREATE TABLE ips 
		(
		id int NOT NULL AUTO_INCREMENT,
		PRIMARY KEY(id),
		ip_global varchar(100),
		ip_local varchar(100),
		ip_full varchar(100),
		last_seen_alive datetime,
		is_server int(1)				
		);";

if ($sqli->query($query) === True) 
	echo'table ips created.<br>';
else
	echo $sqli->error;
	

?>
