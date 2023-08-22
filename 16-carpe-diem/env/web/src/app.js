const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
const { verify } = require("hcaptcha");
const worker = require("./worker");

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

const secret = "0x51894fEc2042F17078eC760d86d515200a60aC90";

const PORT = process.env.PORT ?? 12345;
const CHAL = process.env.CHAL ?? "Placeholder";

app.get('/', (req, res, next) => {
    res.render('index', {
        challenge: CHAL
    });
});

app.get('/visit', (req, res, next) => {
    res.render('visit', {
        challenge: CHAL,
        msg: "The admin will visit your URL."
    });
});

app.post('/visit', async (req, res, next) => {
    let url = req.body.url;
    let token = req.body["h-captcha-response"];
    if (!(/^https?:\/\/.*\//).test(url)) {
        return res.render('visit', {
            challenge: CHAL,
            msg: "URL must match ^https?:\/\/.*\/"
        });
    }
    else {
        if (req.socket.remoteAddress != "127.0.0.1") {
            verify(secret, token).then((data) => {
                if (!data.success === true) {
                    return res.render('visit', {
                        challenge: CHAL,
                        msg: "hCaptcha is broken"
                    });
                }
            });
        }
        console.log(`[!] ${new Date().toLocaleString()} attempt to visit ${url}`);
        try {
            await worker.visit(url);
            console.log(`[+] ${new Date().toLocaleString()} success`);
            return res.render('visit', {
                challenge: CHAL,
                msg: `The admin has visited your URL.`
            });
        }
        catch (e) {
            console.log(`[-] ${new Date().toLocaleString()} fail, reason: ${e}`);
            return res.render('visit', {
                challenge: CHAL,
                msg: "Error occured when the admin was trying to visit your URL."
            })
        }
    }
});

app.listen(PORT, () => {
    console.log(`web/${CHAL} listening on port ${PORT}`);
});