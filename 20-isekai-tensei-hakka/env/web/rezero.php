<?php
set_time_limit(0);
require "/usr/local/apache2/htdocs/forum_support/config/config.php";
$conn = new mysqli($servername, $dbusername, $dbpassword);
$conn->query("SET NAMES utf8;");
$conn->query("SET CHARACTER_SET_CLIENT=utf8;");
$conn->query("SET CHARACTER_SET_RESULTS=utf8;");
$conn->query("CREATE DATABASE IF NOT EXISTS test123");
$conn->select_db("test123");
$lines = file("wog3_sql_utf8.sql", FILE_SKIP_EMPTY_LINES|FILE_IGNORE_NEW_LINES);
$sqls = "";
foreach($lines as $line) {
    if(substr($line,0,1)!="#"){
    	$sqls .= $line;
    }
}
$sqls = str_replace("TYPE=MyISAM", "Engine=MyISAM", $sqls);
$sqla = explode(";",$sqls);
foreach($sqla as $sql){
	$conn->query($sql.";");
}
$conn->close();
exec("rm -rf /tmp/*");
?>