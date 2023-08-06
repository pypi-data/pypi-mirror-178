# InstaReset - _Forgot Instagram Password_ using Python !

<br>

## What is this?
This script was made to send a Instagram reset password request using Python **without asking for reCAPTCHA** as Instagram does if we used a browser, It supports username and email methods.

<br>

## How it works ?
This script works by using a faked mobile user agent like `Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440)` and send a POST request to `https://i.instagram.com/api/v1/accounts/send_password_reset/` _with a random generated CSRF token of 32 chars_ in the request data.

<br>

## Features
- Faster ⚡
- No reCAPTCHA 🤖
- Nice looking CLI 🎨
- Works on mobile 📱

<br>

## Requirements
- [Python 3.6.3 or higher](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/) module `pip install requests`
- [Rich](https://pypi.org/project/rich/) module `pip install rich`

<br>

## Installation

The source code is now available on [PyPi](https://pypi.org/project/instareset/) so you can install it using `pip`:

```bash
pip install instareset
```

<br>

## Module version usage (New in v2.0.0)

```python
from instareset import InstaReset

# Create an instance of InstaReset
ir = InstaReset()

# Send a reset password request
ir.send_request('username or email')
```

`send_request` might raise `InvalidUsernameException`, `RateLimitedException`, or `UsernameNotFoundException` which can be imported from `instareset.exceptions`.

<br>

## Changelog

**v2.0.0**

What's new?
- Added module support, script mode still available if you run the script directly.
- Uploaded source code to [PyPi](https://pypi.org/project/instareset/)
- Removed `main.exe` file
- New ASCII art and changed in console style
- Changed `README.md` file (added **installation** and **usage** sections)
- Changed coloring module to [Rich](https://pypi.org/project/rich/)

Coming soon...
- **Auto reset password** feature (available with temporary email that the script will generate)

**v1.1**
- Auto detect target's method (email/username)
- More clean code
- Fixed bug in email method

**v1.0**
- Initial release

<br><br><hr>

_Liked the project? Leave a star ⭐ to show your support!_
