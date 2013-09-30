<?php

	class MyDB {
		private static $dbLink;

		private function __construct() {}
		private function __clone() {}

		public static function Get() {
			if(!self::$dbLink) {
				self::$dbLink = new mysqli("localhost", "root", "", "[myDB]");
				if(mysqli_connect_errno()) {
					throw new Exception("Database connection failed: ".mysqli_connect_error());
				}

			}
			return self::$dbLink;
		}
	}
	
?>
