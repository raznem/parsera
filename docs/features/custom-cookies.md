## Custom cookies usage
To manage sessions more effectively, you can supply your session cookies directly to Parsera.

### Cookies format and known issues
Please provide cookies to Parsera in JSON format, as shown in the example below.

To retrieve session cookies from your browser, you can use various browser plugins. However, be aware that some plugins may export cookies in an incorrect format, which can lead to issues.

**Note:** Pay special attention to the SameSite attribute. Valid values for SameSite are Strict, Lax, or None. Some plugins may incorrectly set this attribute to other values, which could cause parsing issues in Parsera.

Example:
```python
    file_with_cookeis = "cookies.json"
    with open(file_with_cookeis, "r") as file:
        cookies = json.load(file)

    parsera = Parsera(model=model, custom_cookies=cookies)
    return await parsera.arun(
        url="https://www.reddit.com/settings/",
        elements={
            "email address": "value",
        },
    )

```
[Try out full example](https://github.com/raznem/parsera/tree/main/examples/cookie_usage.py)