# Huya Auto Barrage

An automation tool for sending barrages on [Huya](https://www.huya.com/) website.

Note: barrage, also called danmu, bullet comments, bullet screen, etc, is a live commenting system often existing in Chinese video live streaming website.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Supported Python Versions
- Python 3.4+

Before proceeding further, you should have created your own Huya credentials. Create a pass.json file under ./conf folder using following format.

```JSON
{
  "username": "xxxxxxxxxx",
  "password": "xxxxxxxxxx"
}
```

### Installing

If you have pip on your system, you can simply install or upgrade the Python bindings:

```
pip install -U selenium
```

Note: You may want to consider using virtualenv to create isolated Python environments.

### Drivers

Selenium requires a driver to interface with the chosen browser. Chrome is the chosen browser in this project. Download the correct Chrome driver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). The driver version should match with the Chrome version on your computer. Place the downloaded driver in the ./driver folder.

## Main Features
- Auto Login
- Send barrage in user defined rate
- User configured barrage in file
- Barrage captured
- Machine populated barrage set

## Demo

## Built With

* [Selenium Python Binding](https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver) - Python language bindings for Selenium WebDriver - Browser-based automation tool

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
