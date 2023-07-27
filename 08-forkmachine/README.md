Sample Challenge
===

## Description

I wrote a simple testbed for the JSON processor `jq`!

The flag is written in the file `/flag`.

Web: {CHAL_URL_LINK}

Attachment: {ATTACHMENT_LINK}

```
{CHAL_NC_LINK}
```

## Remark

Remark for deployment, or anything for internal can be written here. For example, the link to a very large file is: http://drive.google.com/abcd

The template `{...LINK}` will be replaced with actual values after we determined the port numbers.

If files are put into the `public/` folder, they will be zipped automatically. If a `zip` is put into the `public/` folder, it will not be zipped again.

## Developing challenge

Check out the challenges last year for sample on writing a chal with Docker:

- [C](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/59-easyheap)
- [Python](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/04-pyjail1)
- [PHP](https://github.com/samueltangz/hkcert-ctf-2021-internal/tree/master/70-jqplayground)


The main points are:

- Do clean up after `apt install` using `rm -rf /var/lib/apt/lists/* /var/cache/apt/*`
- Make sure the challenge files and the flag is owned by `root`, have restrictive permission `444` or lower and the directory with `555` or lower
- Make sure a non-root user is executing the challenges
