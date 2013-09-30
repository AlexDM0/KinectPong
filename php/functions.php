<?php

function getTime() {
    $timer = explode( ' ', microtime() );
    $timer = $timer[1] + $timer[0];
    return $timer;
}


function sizeinput($input, $len){
	(int)$len;
	(string)$input;
	$n = substr($input, 0,$len);
	$ret = trim($n);
	$out = htmlentities($ret, ENT_QUOTES);
	return $out;
}

function rewriteInputForDisplay($input) {
	return str_replace("_"," ",ucfirst($input));
}

/**
* Get the dimensions of a video file
*
* @param unknown_type $video
* @return array(width,height)
* @author Jamie Scott
*/
function getVideoDimensions($video = false) {
	if (file_exists ( $video )) {
		$command = 'ffmpeg -i ' . $video . ' -vstats 2>&1';
		$output = shell_exec ( $command );
		preg_match("/, ?[0-9]{2,4}x?[0-9]{2,4},/",$output,$matches);
		$result = str_replace(" ","",str_replace(",","",$matches[0]));
		return $result;
	} 
	else {
		return false;
	}
}

function cleanText($text) {
	$text = str_replace("'","&prime;",$text);
	$text = str_replace('"',"&Prime;",$text);
	$text = stripslashes($text);
	$text = str_replace(">","> ",$text);
	$text = strip_tags($text,'<p><ul><li><span><em><strong><ol>');
	$text = str_replace("\r"," \r",$text);
	return $text;
}

function convertLinks($text) {
	$text = cleanText($text);
	$word_array = explode(" ",$text." ");
	$string = "";
	foreach ($word_array as $word) {
		$word = str_replace(" ","",$word);
		if (strpos($word,"@") !== false) 
			$new_word = '<a href="mailto:'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,"http://") !== false) 
			$new_word = '<a href="'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'www.') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.com') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.nl') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.net') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.org') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.co.uk') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		elseif (strpos($word,'.be') !== false) 
			$new_word = '<a href="http://'.strip_tags($word).'" target="_blank">'.strip_tags($word).'</a>';
		else 
			$new_word = $word;
		
		$string = $string.$new_word.' ';
	}
	$string = str_replace(" \r","\r",$string);
	return $string;
}

function rewriteDateForStorage($date) {
	$date_array = explode("-",$date); #dd-mm-yyyy
	if (strlen($date_array[0]) < 2)
		$date_array[0] = "0".$date_array[0];
	if (strlen($date_array[1]) < 2)
		$date_array[1] = "0".$date_array[1];
	if (strlen($date_array[2]) < 2)
		$date_array[2] = "0".$date_array[2];
	return $date_array[2]."-".$date_array[1]."-".$date_array[0]; #yyyy-mm-dd
}

function rewriteDateForDisplay($date) {
	$date_array = explode("-",$date); #yyyy-mm-dd
	if (strlen($date_array[0]) < 2)
		$date_array[0] = "0".$date_array[0];
	if (strlen($date_array[1]) < 2)
		$date_array[1] = "0".$date_array[1];
	if (strlen($date_array[2]) < 2)
		$date_array[2] = "0".$date_array[2];
	return $date_array[2]."-".$date_array[1]."-".$date_array[0]; #dd-mm-yyyy
}

function MySecurityLevel() {
	$user = new user($_SESSION['uid']);
	return $user->securitylevel;
}

function checkfile($input){
	$ext = array('mpg', 'wma', 'mov', 'flv', 'mp4', 'avi', 'qt', 'wmv', 'rm');
	$ext_array = explode('.',$input);
	$good = array();
	$extension = $ext_array[count($ext_array)-1];
	if(in_array($extension, $ext)){
		$good['safe'] = true;
		$good['ext'] = $extension;
	}
	else{
		$good['safe'] = false;
	}
	return $good;
}

function getThumbnail($path) {
	$path_array = explode(".",$path);
	$path = str_replace(".".end($path_array),"_tmb.".end($path_array),$path);
	return $path;
}
		
function checkImage($input){
	$ext = array('jpeg', 'jpg', 'bmp', 'gif', 'png', 'zip');
	$ext_array = explode('.',$input);
	$good = array();
	$extension = $ext_array[count($ext_array)-1];
	if(in_array($extension, $ext)){
		$good['safe'] = true;
		$good['ext'] = $extension;
	}
	else{
		$good['safe'] = false;
	}
	return $good;
}

function resize_image($path,$saveas_path,$width_n,$height_n,$force,$shrink_only) {
	$failed = 0;
	list($width, $height) = getimagesize($path);
	if ($width < $width_n && $height < $height_n && $shrink_only == True) {
		rename($path,$saveas_path);
	}
	else {
		if ($width > $height)
			$percent = ($width_n/$width);
		else
			$percent = ($height_n/$height);
		if ($force == "no") {
			$new_width = $width * $percent;
			$new_height = $height * $percent;
		}
		if ($force == "yes" || $force == "") {
			$new_width = $width_n;
			$new_height = $height_n;
		}

		// Resample
		$image_p = imagecreatetruecolor($new_width, $new_height);
		$extentionarray = explode(".",$path);
		$extention = end($extentionarray);
		$extention = strtolower($extention);
		if ($extention == "jpg")
		{
			if (!@imagecreatefromjpeg($path))
			{
				echo "$path is een invalid image file, probeer een andere";
				unlink($path);
				$failed = 1;
			}
			$image = @imagecreatefromjpeg($path);
		}
		elseif ($extention == "gif")
		{
			if (!@imagecreatefromgif($path))
			{
				echo "$path is een invalid image file, probeer een andere";
				unlink($path);
				$failed = 1;
			}
			$image = imagecreatefromgif($path);
		}
		elseif ($extention == "bmp")
		{
			if (!@imagecreatefrombmp($path))
			{
				echo "$path is een invalid image file, probeer een andere ($extention)";
				unlink($path);
				$failed = 1;
			}
			$image = imagecreatefrombmp($path);
		}
		elseif ($extention == "png")
		{
			if (!@imagecreatefrompng($path))
			{
				echo "$path is een invalid image file, probeer een andere";
				unlink($path);
				$failed = 1;
			}
			$image = @imagecreatefrompng($path);
		}
		elseif ($extention == "jpeg")
		{
			if (!@imagecreatefromjpeg($path))
			{
				echo "$path is een invalid image file, probeer een andere";
				unlink($path);
				$failed = 1;
			}
			$image = @imagecreatefromjpeg($path);
		}
		else
		{
			echo "NOT A VALID IMAGE FILE, ondersteunde formats: jpg, jpeg, gif, png en bmp";
			echo "<br><br>$path";
			unlink($path);
			$failed = 1;
		}

		@imagecopyresampled($image_p, $image, 0, 0, 0, 0, $new_width, $new_height, $width, $height);

		// Output
		imagejpeg($image_p, $saveas_path, 95);
		if ($failed == 1)
			return false;
		else
			return true;
	}
}
/*
 *------------------------------------------------------------
*                    ImageCreateFromBmp
*------------------------------------------------------------
*            - Reads image from a BMP file
*
*         Parameters:  $file - Target file to load
*
*            Returns: Image ID
*/

function imagecreatefrombmp($file) {
	global  $CurrentBit, $echoMode;

	$f=fopen($file,"r");
	$header=fread($f,2);

	if($header=="BM")
	{
	 $Size=freaddword($f);
	 $Reserved1=freadword($f);
	 $Reserved2=freadword($f);
	 $FirstByteOfImage=freaddword($f);

	 $SizeBITMAPINFOheader=freaddword($f);
	 $Width=freaddword($f);
	 $Height=freaddword($f);
	 $biPlanes=freadword($f);
	 $biBitCount=freadword($f);
	 $RLECompression=freaddword($f);
	 $WidthxHeight=freaddword($f);
	 $biXPelsPerMeter=freaddword($f);
	 $biYPelsPerMeter=freaddword($f);
	 $NumberOfPalettesUsed=freaddword($f);
	 $NumberOfImportantColors=freaddword($f);

	 if($biBitCount<24)
	 {
	  $img=imagecreate($Width,$Height);
	  $Colors=pow(2,$biBitCount);
	  for($p=0;$p<$Colors;$p++)
	  {
	  $B=freadbyte($f);
	  $G=freadbyte($f);
	  $R=freadbyte($f);
	  $Reserved=freadbyte($f);
	  $Palette[]=imagecolorallocate($img,$R,$G,$B);
	  };




	  if($RLECompression==0)
	  {
	   $Zbytek=(4-ceil(($Width/(8/$biBitCount)))%4)%4;

	   for($y=$Height-1;$y>=0;$y--)
	   {
	   	$CurrentBit=0;
	   	for($x=0;$x<$Width;$x++)
	   	{
	   	$C=freadbits($f,$biBitCount);
		   imagesetpixel($img,$x,$y,$Palette[$C]);
		  };
		  if($CurrentBit!=0) {
		  freadbyte($f);
	   };
	   for($g=0;$g<$Zbytek;$g++)
	   	freadbyte($f);
	};
	
	};
	};
	
	
	if($RLECompression==1) //$BI_RLE8
	{
	$y=$Height;
	
	$pocetb=0;
	
	while(true)
	{
	$y--;
	$prefix=freadbyte($f);
	$suffix=freadbyte($f);
	$pocetb+=2;
	
	$echoit=false;
	
	if($echoit)echo "Prefix: $prefix Suffix: $suffix<BR>";
	if(($prefix==0)and($suffix==1)) break;
	if(feof($f)) break;
	
	while(!(($prefix==0)and($suffix==0)))
	{
		if($prefix==0)
		{
			$pocet=$suffix;
			$Data.=fread($f,$pocet);
			$pocetb+=$pocet;
			if($pocetb%2==1) {
				freadbyte($f); $pocetb++;
			};
		};
		if($prefix>0)
		{
			$pocet=$prefix;
			for($r=0;$r<$pocet;$r++)
				$Data.=chr($suffix);
		};
		$prefix=freadbyte($f);
		$suffix=freadbyte($f);
		$pocetb+=2;
		if($echoit) echo "Prefix: $prefix Suffix: $suffix<BR>";
	};
	
	for($x=0;$x<strlen($Data);$x++)
	{
	imagesetpixel($img,$x,$y,$Palette[ord($Data[$x])]);
	};
	$Data="";
	
	};
	
	};
	
	
	if($RLECompression==2) //$BI_RLE4
	{
	$y=$Height;
	$pocetb=0;
	
	/*while(!feof($f))
	echo freadbyte($f)."_".freadbyte($f)."<BR>";*/
	while(true)
	{
	//break;
	$y--;
	$prefix=freadbyte($f);
	$suffix=freadbyte($f);
	$pocetb+=2;
	
	$echoit=false;
	
	if($echoit)echo "Prefix: $prefix Suffix: $suffix<BR>";
	if(($prefix==0)and($suffix==1)) break;
	if(feof($f)) break;
	
	while(!(($prefix==0)and($suffix==0)))
	{
	if($prefix==0)
	{
	$pocet=$suffix;
	
		$CurrentBit=0;
		for($h=0;$h<$pocet;$h++)
			$Data.=chr(freadbits($f,4));
			if($CurrentBit!=0) freadbits($f,4);
			$pocetb+=ceil(($pocet/2));
			if($pocetb%2==1) {
			freadbyte($f); $pocetb++;
	};
	};
	if($prefix>0)
		{
		$pocet=$prefix;
		$i=0;
		for($r=0;$r<$pocet;$r++)
		{
			if($i%2==0)
			{
			$Data.=chr($suffix%16);
		}
		else
		{
		$Data.=chr(floor($suffix/16));
		};
		$i++;
		};
		};
		$prefix=freadbyte($f);
		$suffix=freadbyte($f);
		$pocetb+=2;
		if($echoit) echo "Prefix: $prefix Suffix: $suffix<BR>";
	};
	
	for($x=0;$x<strlen($Data);$x++)
	{
	imagesetpixel($img,$x,$y,$Palette[ord($Data[$x])]);
	};
	$Data="";
	
	};
	
	};
	
	
	if($biBitCount==24)
	{
	$img=imagecreatetruecolor($Width,$Height);
	$Zbytek=$Width%4;
	
	for($y=$Height-1;$y>=0;$y--)
		{
		for($x=0;$x<$Width;$x++)
		{
		$B=freadbyte($f);
		$G=freadbyte($f);
		$R=freadbyte($f);
		$color=imagecolorexact($img,$R,$G,$B);
		if($color==-1) $color=imagecolorallocate($img,$R,$G,$B);
		imagesetpixel($img,$x,$y,$color);
		}
		for($z=0;$z<$Zbytek;$z++)
			freadbyte($f);
		};
		};
		return $img;
	
		};
	
	
		fclose($f);


};





	/*
	* Helping functions:
	*-------------------------
	*
	* freadbyte($file) - reads 1 byte from $file
	* freadword($file) - reads 2 bytes (1 word) from $file
	* freaddword($file) - reads 4 bytes (1 dword) from $file
	* freadlngint($file) - same as freaddword($file)
	* decbin8($d) - returns binary string of d zero filled to 8
	* RetBits($byte,$start,$len) - returns bits $start->$start+$len from $byte
	* freadbits($file,$count) - reads next $count bits from $file
	* RGBToHex($R,$G,$B) - convert $R, $G, $B to hex
	* int_to_dword($n) - returns 4 byte representation of $n
	* int_to_word($n) - returns 2 byte representation of $n
	*/

function freadbyte($f){
	return ord(fread($f,1));
};

function freadword($f){
	$b1=freadbyte($f);
	$b2=freadbyte($f);
	return $b2*256+$b1;
};


function freadlngint($f){
	return freaddword($f);
};

function freaddword($f)	{
	$b1=freadword($f);
	$b2=freadword($f);
	return $b2*65536+$b1;
};



function RetBits($byte,$start,$len)	{
	$bin=decbin8($byte);
		$r=bindec(substr($bin,$start,$len));
		return $r;
};



	$CurrentBit=0;
function freadbits($f,$count)	{
	global $CurrentBit,$SMode;
	$Byte=freadbyte($f);
	$LastCBit=$CurrentBit;
	$CurrentBit+=$count;
	if($CurrentBit==8)		{
		$CurrentBit=0;
	}
	else {
		 fseek($f,ftell($f)-1);
	};
	return RetBits($Byte,$LastCBit,$count);
};



function RGBToHex($Red,$Green,$Blue)
	{
	$hRed=dechex($Red);if(strlen($hRed)==1) $hRed="0$hRed";
	$hGreen=dechex($Green);if(strlen($hGreen)==1) $hGreen="0$hGreen";
	$hBlue=dechex($Blue);if(strlen($hBlue)==1) $hBlue="0$hBlue";
	return($hRed.$hGreen.$hBlue);
};

function int_to_dword($n){
	return chr($n & 255).chr(($n >> 8) & 255).chr(($n >> 16) & 255).chr(($n >> 24) & 255);
}
	
function int_to_word($n)	{
	return chr($n & 255).chr(($n >> 8) & 255);
}


function decbin8($d){
	return decbinx($d,8);
};

function decbinx($d,$n)	{
	$bin=decbin($d);
	$sbin=strlen($bin);
	for($j=0;$j<$n-$sbin;$j++)
	 $bin="0$bin";
	 return $bin;
};

function inttobyte($n){
	return chr($n);
};

/**
 * Unzip the source_file in the destination dir
 *
 * @param   string      The path to the ZIP-file.
 * @param   string      The path where the zipfile should be unpacked, if false the directory of the zip-file is used
 * @param   boolean     Indicates if the files will be unpacked in a directory with the name of the zip-file (true) or not (false) (only if the destination directory is set to false!)
 * @param   boolean     Overwrite existing files (true) or not (false)
 * 
 * @return  boolean     Succesful or not
 */

function unzip($src_file, $dest_dir, $create_zip_name_dir=false, $overwrite=true)
{
      if(!is_resource(zip_open($src_file)))
      { 
          $src_file=dirname($_SERVER['SCRIPT_FILENAME'])."/".$src_file; 
      }
      
      if (is_resource($zip = zip_open($src_file)))
      {          
          $splitter = ($create_zip_name_dir === true) ? "." : "/";
          if ($dest_dir === false) $dest_dir = substr($src_file, 0, strrpos($src_file, $splitter))."/";
         
          // Create the directories to the destination dir if they don't already exist
          create_dirs($dest_dir);

          // For every file in the zip-packet
          while ($zip_entry = zip_read($zip))
          {
            // Now we're going to create the directories in the destination directories
           
            // If the file is not in the root dir
            $pos_last_slash = strrpos(zip_entry_name($zip_entry), "/");
            if ($pos_last_slash !== false)
            {
              // Create the directory where the zip-entry should be saved (with a "/" at the end)
              create_dirs($dest_dir.substr(zip_entry_name($zip_entry), 0, $pos_last_slash+1));
            }

            // Open the entry
            if (zip_entry_open($zip,$zip_entry,"r"))
            {
             
              // The name of the file to save on the disk
              $file_name = $dest_dir.zip_entry_name($zip_entry);
             
              // Check if the files should be overwritten or not
              if ($overwrite === true || $overwrite === false && !is_file($file_name))
              {
                // Get the content of the zip entry
                $fstream = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));           
                
                if(!is_dir($file_name))            
                file_put_contents($file_name, $fstream );
                // Set the rights
                if(file_exists($file_name))
                {
                    chmod($file_name, 0777);
                    //echo "<span style=\"color:#1da319;\">file saved: </span>".$file_name."<br />";
                }
                else
                {
                    //echo "<span style=\"color:red;\">file not found: </span>".$file_name."<br />";
                }
              }
             
              // Close the entry
              zip_entry_close($zip_entry);
            }      
          }
          // Close the zip-file
          zip_close($zip);
      }
      else
      {
        echo "No Zip Archive Found.";
        return false;
      }
     
      return true;
  }


function create_dirs($path)
{
  if (!is_dir($path))
  {
    $directory_path = "";
    $directories = explode("/",$path);
    array_pop($directories);
   
    foreach($directories as $directory)
    {
      $directory_path .= $directory."/";
      if (!is_dir($directory_path))
      {
        mkdir($directory_path);
        chmod($directory_path, 0777);
      }
    }
  }
}

?>