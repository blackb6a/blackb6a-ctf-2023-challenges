from flask import Flask, request
from urllib.parse import urlencode
from urllib.request import urlopen
import subprocess
import os

G_SITEKEY = os.getenv("G_SITEKEY", '"><script>document.write("reCAPTCHA is broken")</script>')
G_SECRET = os.getenv("G_SECRET", "Victoria's Secret")
app = Flask(__name__)

def escapeshellcmd(cmd):
	bad = "&#;`|*?~<>^()[]}{$\\,\n\xff'\""
	mad = ["\\"+c for c in bad]
	return cmd.translate(str.maketrans(dict(zip(bad,mad))))

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if "g-recaptcha-response" not in request.form or request.form["g-recaptcha-response"] == "":
			return "Bad reCAPTCHA"
		data = urlencode({"secret": G_SECRET, "response": request.form["g-recaptcha-response"]}).encode('ascii')
		try:
			fetch = urlopen("https://www.google.com/recaptcha/api/siteverify", data).read().decode("utf-8")
		except Exception as e:
			return str(e)
		if '"success": true' not in fetch:
			return "reCAPTCHA is broken"
		argv = escapeshellcmd(request.form["argv"])
		if "-eval" in argv:
			payload = argv[argv.find("-eval")+6:].split()[0]
			return "<script>for(;;){try{eval(prompt('eval','%s'))}catch(e){}}</script>" % payload
		if "-alert" in argv:
			payload = argv[argv.find("-alert")+7:].split()[0]
			return "<script>for(;;){alert('%s')}</script>" % payload
		command = "python sqlmap.py %s" % argv
		print(request.remote_addr + ": " + command, flush=True)
		try:
			out = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=30, cwd="/sqlmap-dev")
		except subprocess.CalledProcessError as e:
			out = e.output
		return "<code>%s</code><hr /><plaintext>%s" % (command, out.decode("utf-8"))
	else:
		return """<html>
<head>
<title>Sqlmap as a Service</title>
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
</head>
<body>
<h2>Sqlmap as a Service</h2>
<form method="post">
<p style="font-family:Courier New;background:#CCCCCC;font-size:16pt;padding:0.25em">
python sqlmap.py 
<input style="font-family:Courier New;background:#CCCCCC;font-size:16pt;border:0;width:80%%" name="argv" placeholder="http://menazon.ozetta.net/search.php --answers=Y --data=search=Y">
</p>
<div class="g-recaptcha" data-sitekey="%s"></div>
<p><input type="submit"></p>
</form>
<p>Remarks: 
<ul>
<li style="color:red">Do not scan others without permission. Your IP will be reported if we receive abuse complains. </li>
<li>Timeout in 30 seconds </li>
<li>Reborn every 30 minutes </li>
<li>To prevent hackers like you hacking the service, the keywords <code style="color:red">-eval</code> and <code style="color:red">-alert</code> are blocked. </li>
</ul>
</p>
</body>
</html>""" % G_SITEKEY


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=3306)