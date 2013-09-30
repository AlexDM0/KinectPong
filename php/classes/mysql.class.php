<?php
	class mysql {
		private static $dbLink;
		
		protected $connection;
		protected $last_query;
		protected $db;
		protected $table;
		protected $mysqli;
		
		public $num_rows;
		public $resultset;
		
		function __construct($db){
			$this->db = $db;
			$this->mysqli = MyDB::Get();
		}
		
		
		public function setTable($table) {
			$this->table = $table;
		}
		
		
		function query($query){
			$start = getTime();
			queries::Add($query." EXECUTED FROM query");
			$this->last_query = $query;
			if(!$this->mysqli->query($query)){
				echo $query."<br />this caused: ".$this->mysqli->error;
				die;
				}
			$end = getTime();
			queries::addTimeToQuery($end-$start);
		}
		
		
		function getValue($query="",$keepopen=False){
			$start = getTime();
			if ($query != "") {
				queries::Add($query." EXECUTED FROM getValue");
				$this->last_query = $query;
				$this->resultset = $this->mysqli->query($query);
			}
			else {
				queries::Add($this->last_query." EXECUTED FROM getValue");
				$this->resultset = $this->mysqli->query($query);
			}
			$this->num_rows = $this->resultset->num_rows;
			if ($this->num_rows > 0) {
				$return = $this->resultset->fetch_row();
				if (!$keepopen)
					$this->resultset->close();
				$end = getTime();
				queries::addTimeToQuery($end-$start);
				return $return[0];
			}
			else {
				if (!$keepopen)
					$this->resultset->close();
				return false;
			}
		}
		
		function getNumRows($query){
			$this->resultset = $this->mysqli->query($query);
			return $this->resultset->num_rows;
		}
		
		function clearResults() {
			$this->resultset.close();
		}
		
		function fetchFieldArray($table) {
			$results = $this->fetchArray("SHOW COLUMNS FROM ".$table);
			return $results;
		}
		
		
		function fetchArray($query="",$keepopen=False){
			$start = getTime();
			if ($query != "") {
				queries::Add($query." EXECUTED FROM fetchArray");
				$this->last_query = $query;
				$this->resultset = $this->mysqli->query($query);
			}
			else {
				queries::Add($this->last_query." EXECUTED FROM fetchArray");
				$this->resultset = $this->mysqli->query($this->last_query);
			}
			$this->num_rows = $this->resultset->num_rows;
			if ($this->num_rows > 0) {
				while($row = $this->resultset->fetch_array(MYSQLI_ASSOC)) {
					$rows[] = $row;
				}
				if (!$keepopen)
					$this->resultset->close();
				$return = $rows;
			}
			else {
				if (!$keepopen)
					$this->resultset->close();
				$return = false;
			}
			$end = getTime();
			queries::addTimeToQuery($end-$start,-1);
			return $return;
		}
		
		
		function columnExists($table,$column) {
			if ($this->tableExists($table)) {
				$fields = $this->fetchFieldArray($table);
				$found = false;
				foreach ($fields as $field) {
					if ($field['Field'] == $column) {
						$found = true;
						break;
					}					
				}
				return $found;
			}
			else
				return false;
		}
		
		function tableExists($table) {
			$result = $this->getValue("SELECT COUNT(*) AS count FROM information_schema.tables WHERE table_schema = '".$this->db."' AND table_name = '".$table."'");
			print_r($result);
			if ($result[0] == 1)
				return true;
			else
				return false;
		}
		
		
		function appendColumn($table,$column,$type="double",$after_column="") {
			$size = "";
			if ($type == "double") 
				$size = "(12,2)";
			elseif ($type == "varchar")
				$size = "(200)";
			elseif ($type == "int")
				$size = "(12)";
				
			if ($after_column != "")
				$after_column = " AFTER ".$after_column;
			$query = "ALTER TABLE ".$table." ADD ".$column." ".$type.$size.$after_column;
			$this->query($query);
		}
		
		
		
	}