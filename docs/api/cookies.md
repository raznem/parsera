## How to use cookies with the API
You can provide cookie from the target website to the API. (for example to access User session).

To retrieve session cookies from your browser, you can use various browser plugins. However, be aware that some plugins may export cookies in an incorrect format, which can lead to issues.

**Note:** Pay special attention to the SameSite attribute. Valid values for SameSite are Strict, Lax, or None. Some plugins may incorrectly set this attribute to other values, which could cause parsing issues in Parsera.

```bash
curl https://api.parsera.org/v1/extract \
--header 'Content-Type: application/json' \
--header 'X-API-KEY: <YOUR_API_KEY>' \
--data '{
    "url": "https://www.reddit.com/settings/",
    "attributes": [
        {
            "name": "email",
            "description": "email value"
        }
    ],
        "cookies": [
    {
		"your cookie 0" : "have a great day!",
		"sameSite" : "None"
    },
    {
		"your cookie 1" : "have a great day!",
		"sameSite" : "Lax"
    },
    {
		"your cookie 2" : "have a great day!",
		"sameSite" : "Strict"
    },
]
}
```