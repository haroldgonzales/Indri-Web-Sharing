<?php
  session_start();

  // If the session vars aren't set, try to set them with a cookie
  #if (!isset($_SESSION['user_id'])) {
   # if (isset($_COOKIE['user_id']) && isset($_COOKIE['username'])) {
    
#  $_SESSION['user_id'] = $_COOKIE['user_id'];
 #     $_SESSION['username'] = $_COOKIE['username'];
  #  }
  #}
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />
    <title>PEG: Semantic Filesharing for the Enterprise</title>
    <link type="text/css" rel="stylesheet" href="peg.css" media="screen" />
  </head>
  <body>

<?php
  require_once('appvars.php');
  require_once('connectvars.php');
  // Connect to the database 
  $dbc = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
  // Generate the navigation menu
  if (isset($_SESSION['username'])) {
        echo '<h1>PEG: Search and Share</h1>';

    	echo '<p id="stored_queries">';
        echo 'Stored queries<br/>';
    	echo '</p>';
	$stored_queries_query = "SELECT * FROM stored_queries WHERE username="."'".mysqli_real_escape_string($dbc, $_SESSION['username'])."'";
	$stored_queries = mysqli_query($dbc, $stored_queries_query);
	if (!$stored_queries) {
    		die('Invalid query: ' . mysql_error());
	}
	while ($row = mysqli_fetch_array($stored_queries)){
		echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
    		echo '<input type="submit" value="'.$row['query'].'" name="change-corpus" />';
  		echo '</form>';
	}
	mysqli_free_result($stored_queries);
	echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
    	echo '<input type="submit" value="reset corpus" name="reset-corpus" />';
  	echo '</form>';
	echo $_SESSION['default_corpus']."</br>";
        echo 'Shared queries<br/>';
        echo 'here too<br/>';
    	echo '</p>';
	echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
        echo '<fieldset>';
      	echo '<legend>Search Current Corpus</legend>';
      	echo '<label for="search">Search:</label>';
      	echo '<input type="text" name="search" /><br />';
    	echo '</fieldset>';
    	echo '<input type="submit" value="new search" name="submit" />';
  	echo '</form>';
	echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
    	echo '<input type="submit" value="Store Current Query" name="store" />';
  	echo '</form>';
	echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
    	echo '<input type="submit" value="Store Current Query as Privacy Query" name="store-private" />';
  	echo '</form>';
	
	if(isset($_POST['reset-corpus'])){
		unset($_SESSION['corpus']);
		unset($_SESSION['corpus_query']);
		unset($_SESSION['query']);
	}
	if(isset($_POST['change-corpus'])){
	#set current corpus to the session var	
	$stored_queries = mysqli_query($dbc, $stored_queries_query);
	while ($myrow = mysqli_fetch_array($stored_queries)){
		echo $myrow['query']."</br>";
		if($myrow['query']==$_POST['change-corpus']){
			$_SESSION['corpus_query']=$myrow['query'];
			$_SESSION['corpus']=$myrow['index_path'];
			break;
		}
	}
	}
	if(isset($_SESSION['corpus_query'])){
		echo "<h2>Current Search Corpus: ".$_SESSION['corpus_query']."</h2>";
		echo "<h2>Current Search Index: ".$_SESSION['corpus']."</h2>";
	}
	
	if (isset($_POST['store'])||isset($_POST['store-private'])) {
		$_SESSION['query'] = mysqli_real_escape_string($dbc, trim($_SESSION['query']));
		if(isset($_POST['store'])){
			$lastline=system("/home/gonzales/enron/make_stored_query.py ".$_SESSION['username']." \"".$_SESSION['query']."\" 0",$retval);
		}
		if(isset($_POST['store-private'])){
			$lastline=system("/home/gonzales/enron/make_stored_query.py ".$_SESSION['username']." \"".$_SESSION['query']."\" 1",$retval);
		}
		if($retval==0){
#			$query = " peg_user WHERE username = '$user_username' AND password = SHA('$user_password')";
			if(isset($_POST['store'])){
			$query = "INSERT INTO stored_queries (username,index_path,query,private) VALUES ( '".$_SESSION['username']."', '$lastline', '".$_SESSION['query']."', 0)";
			}
			if(isset($_POST['store-private'])){
			$query = "INSERT INTO stored_queries (username,index_path,query,private) VALUES ( '".$_SESSION['username']."', '$lastline', '".$_SESSION['query']."', 1)";
        		}
			$data = mysqli_query($dbc, $query);
			//check for query failure here handle attempt to re store a query gracefully.
			echo '<p>\n';
			echo "Your stored query ".$_SESSION['query']." has been stored!\n";
			echo '</p>\n';
			unset($_SESSION['query']);
			echo '<form method="post" action="'. $_SERVER['PHP_SELF'] .'">';
    			echo '<input type="submit" value="Continue" name="reload" />';
  			echo '</form>';

		}
		
		
		
	}
	if (isset($_POST['submit'])) {
		$search = mysqli_real_escape_string($dbc, trim($_POST['search']));
		echo '<h2>Search Results</h2>';
#Need to add corpus selection from session variables here
		if(!isset($_SESSION['corpus'])){
			$command ='IndriRunQuery -baseline=tfidf -index='.$_SESSION['default_corpus'].' -query="' . $search.'" 2>&1';
		}
		else{
			$command ='IndriRunQuery -baseline=tfidf -index='.$_SESSION['corpus'].' -query="' . $search.'" 2>&1';
		}
		echo $command;
		$handle = popen($command,'r');
		echo '<p>';
		$count=1;
		$results=array();
		while(($line=fgets($handle,4096))!==false){
#include logic to parse out file and maybe score only here, also put in stuff for file download link
			$split=preg_split('/\s/',$line,4);
			$results[$count]='/'.$split[1];
			echo '/'.$results[$count] . '<br/>';
			$count=$count+1;
		}
		echo '</p>';
		fclose($handle);
		$_SESSION['query']=$search;
	}
  }
  else {
    echo '<a href="login.php">Log In</a><br />';
  }


?>

</body> 
</html>
