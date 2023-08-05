# httpstat

curl statistics made simple.

![screenshot](screenshot.png)


httpstat is a **single file🌟** Python script that has **no dependency👏** and is compatible with **Python 3🍻**.


## Usage

Just pass a url with it:

```bash
python httpstat.py httpbin.org/get
```

By default it will write response body in a tempfile, but you can let it print out by setting `HTTPSTAT_SHOW_BODY=true`:

```bash
HTTPSTAT_SHOW_BODY=true python httpstat.py httpbin.org/get
```

You can pass any curl supported arguments after the url (except for `-w`, `-D`, `-o`, `-s`, `-S` which are already used by httpstat):

```bash
HTTPSTAT_SHOW_BODY=true python httpstat.py httpbin.org/post -X POST --data-urlencode "a=中文" -v
```


