const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
const worker = require("./worker");

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

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
    if (!(/^https?:\/\/.*\//).test(url)) {
        return res.render('visit', {
            challenge: CHAL,
            msg: "URL must match ^https?:\/\/.*\/"
        });
    }
    else {
        console.log(`[!] ${new Date().toLocaleString()} attempt to visit ${url}`);
        try {
            let idx = await worker.visit(url);
            console.log(`[+] ${new Date().toLocaleString()} success`);
            return res.render('visit', {
                challenge: CHAL,
                msg: `The admin has visited your URL based on Rule ${idx}.`
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