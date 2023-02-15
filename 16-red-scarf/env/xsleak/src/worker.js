const puppeteer = require("puppeteer");
const crypto = require("crypto");
const FLAG = process.env.FLAG ?? "flag{this_is_a_test_flag}";

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
    
    var idx = Math.floor(Math.random() * FLAG.length);
    var k = FLAG.charCodeAt(idx);
    for (let i = 0; i < k; i++) {
        await page.goto(`http://example.com/${crypto.randomBytes(20).toString('hex')}`, {waitUntil: "networkidle0"});
    }
    await page.goto(url, {waitUntil: "networkidle2"});
    await new Promise(r => setTimeout(r, 20000));
    await page.close();
    await browser.close();
    return idx;
}

module.exports = { visit };