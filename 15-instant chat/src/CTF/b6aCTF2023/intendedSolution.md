Assuming reverse engineered the application, obtained the firebase config and noticed the collection structure by observing the decompiled code

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

There are 3 collection

```
messages
users
chatrooms
```

by reverse engineering the APK and you can test access control manually. I used https://github.com/iosiro/baserunner

The following is the firebase security rule. Should share this rule? However, the vulnerability is quite easy to spot.

```
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
      ".write" : "auth != null",
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

You will see only message has some sort of access control enforced.

Use this config

```
{
  "apiKey": "AIzaSyAS4ptyTHqvFh0tviMbWV9gzIr7bMo0eCY",
  "authDomain": "instantchat-66091-default-rtdb.firebaseio.com",
  "databaseURL": "https://instantchat-66091-default-rtdb.firebaseio.com",
  "projectId": "instantchat-66091",
  "storageBucket": "instantchat-66091.appspot.com",
  "appId": "1:204796949431:android:8b3f79c75f2559c452ee32"
}
```

Add yourself to the participant of the chatroom as such

![43c5a6fadaa0ceae8e0aa8d7c3df8649.png](../../_resources/43c5a6fadaa0ceae8e0aa8d7c3df8649.png)

Read the chatroom as such

![a95457ec96932e58c665c2a07df21636.png](../../_resources/a95457ec96932e58c665c2a07df21636.png)