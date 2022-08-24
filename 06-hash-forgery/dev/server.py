import random
import hashlib
# from secret import start_seed
start_seed = "this_is_a_secret_seed_lol?"
flag = "flag{}"


def f(h, c):
    return hashlib.md5((h + c).encode()).hexdigest()


def shit_hash(s):
    h = start_seed
    for c in str(s):
        h = f(h, c)
    return int(h, 16)


def verify_signature(s, h):
    if len(s) > 64:
        s = s[-64:]

    return shit_hash(s) == h


users = ['mystiz', 'grhkm']
perms = [1000, 1000]
hashes = [shit_hash(name) for name in users]


def add_user(user):
    global users, perms, hashes
    if user in users:
        print(f"User {user} already in database! Exiting!")
        exit(1)

    users.append(user)
    perms.append(-1)

    user_hash = shit_hash(user)
    hashes.append(user_hash)

    return user_hash


def login_user(user_hash):
    global users, perms, hashes
    for _user, _perm, _hash in zip(users, perms, hashes):
        if user_hash == _hash:
            print(f"Authenticated as {_user}!")
            print("Here is your flag:", flag)
            return 0
        else:
            print("Failed authentication!")
            return 1


def challenge():
    # add name
    print("What's your name?")
    name = input("> ")

    user_hash = add_user(name)
    print("Your hash is:", user_hash)

    # ask name
    print("Now try logging in with your hash!")
    user_hash = int(input("> "))

    exit_code = login(user_hash)
    return exit_code


if __name__ == '__main__':
    challenge()