<?php

class queries {
	static $query_array = array();
	static $query_time = 0;
  
	static function Add($query) {
		self::$query_array[] = $query;
	}
	
	static function printQueries() {
		foreach(self::$query_array as $query) {
			echo $query."<br />";
		}
    echo (self::$query_time/1000)." seconds spent on a total of ".count(self::$query_array)." queries";
	}
	
  
	static function resetQueries() {
		self::$query_array = array();
	}
  
  static function addTimeToQuery($time,$index_shift=0) {
    $time = round($time*1000,5);
    self::$query_array[count(self::$query_array)-1 + $index_shift] = self::$query_array[count(self::$query_array)-1 + $index_shift]."  ".$time." ms";
    self::$query_time = self::$query_time + $time;
  }
}

?>