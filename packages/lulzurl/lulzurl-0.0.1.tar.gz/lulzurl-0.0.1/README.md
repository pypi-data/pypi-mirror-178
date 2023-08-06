# lulzurl

## easyurl

Contains class EasyUrl which allows you to do somthing like this:

```
e = EasyUrl("https://exampleurl.com", lambda url: url)
print(e()) # outputs "https://exampleurl.com"
print(e.main.other.coolthing()) # outputs "https://exampleurl.com/main/other/coolthing"
```

You can substitute any handler you wish.