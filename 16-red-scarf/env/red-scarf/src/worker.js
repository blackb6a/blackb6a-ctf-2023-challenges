const puppeteer = require("puppeteer");
const crypto = require("crypto")
const FLAG = process.env.FLAG ?? "flag{THISISATESTFLAG}";
const flag_content = FLAG.slice(FLAG.indexOf("{") + 1, -1);

async function visit(url) {
    var browser = await puppeteer.launch({
        executablePath: "/usr/bin/google-chrome",
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--no-gpu',
            '--disable-default-apps',
            '--disable-translate',
            '--disable-device-discovery-notifications',
            '--disable-software-rasterizer',
            '--disbale-xss-auditor'
        ],
        ignoreHTTPSErrors: true
    });
    var page = await browser.newPage();
    
    var idx = Math.floor(Math.random() * flag_content.length);
    var k = flag_content.charCodeAt(idx) - 65 + 1;

    for (let i = 0; i < k; i++) {
        await page.goto(`http://example.com/${crypto.randomBytes(20).toString("hex")}`, {waitUntil: "networkidle0"});
    }

    await page.goto(url+`?z=${idx}`, {waitUntil: "networkidle2"});
    await new Promise(r => setTimeout(r, 20000));
    await page.close();
    await browser.close();
}

module.exports = { visit };