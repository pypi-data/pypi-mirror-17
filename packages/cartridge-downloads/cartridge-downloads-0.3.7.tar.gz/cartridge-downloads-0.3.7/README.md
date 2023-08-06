Digital product support for the [Django](https://github.com/django/django)/[Mezzanine](https://github.com/stephenmcd/mezzanine)/[Cartridge](https://github.com/stephenmcd/cartridge) stack, with support for large files with [django_downloadview](https://github.com/benoitbryon/django-downloadview).

[![Build Status](https://travis-ci.org/ryneeverett/cartridge-downloads.svg?branch=master)](https://travis-ci.org/ryneeverett/cartridge-downloads)

# Features

- Adds download fields to the `Product` admin.
- Adds download fields to the `Form` admin.
- Download files are available upon order/form completion and if there is a confirmation email a link is added to the files.

## Download Only Variations *(optional)*

Often times a download is bundled with a physical product -- mp3's may come with a cd or an epub might come with a book. In this case it often makes sense to have one variation for just the download and another for the physical good *and* the download.

### Product Page
- When all variations of a product are "download only", it's quantity field is hidden.

### Cart Page

- The quantity field of "download only" variations is forced to "1" and hidden.

### Orders

When orders consist solely of "download only" products, they get:

  - marked as processed automatically
  - free shipping

To enable this feature:

1. Add a "Downloads" type to the setting `SHOP_OPTION_TYPE_CHOICES`.
2. Add a `ProductOption` named "Download Only" to the "Download" type.

# Installation

```console
pip install cartridge-downloads
python manage.py migrate
```

## settings.py

```py
# OPTIONALLY, if you're using the "download only" feature and want free shipping for transactions consisting of only those products.
SHOP_HANDLER_BILLING_SHIPPING = "cartridge_downloads.checkout.billship_handler"

# Alternately, you could call this handler method from your own handler.
SHOP_HANDLER_ORDER = 'cartridge_downloads.checkout.order_handler'
...
# OPTIONALLY, specify allowed file formats here. Defaults to allowing all.
FILEBROWSER_SELECT_FORMATS = {
    ...
    'Download': ['Document'],
}
...
INSTALLED_APPS = (
...
    'cartridge_downloads',  # Before cartridge.shop
    ...
    'cartridge.shop',
    ...
...
)
```

## urls.py

```py
from cartridge_downloads.views import override_filebrowser
...
urlpatterns = [
...
    # Cartridge-Downloads' URLs (before cartridge urls).
    url("^downloads/", include('cartridge_downloads.urls')),
    url("^shop/(?=(product|cart))",
        include('cartridge_downloads.cartridge_override_urls')),
    url(r'^delete/$', override_filebrowser.delete, name="fb_delete"),
...
]
```

# Webserver Configuration

## Protecting Files in Production

In development, static assets are served by the development server and as such can be masked by django views. In production, your static assets are served more efficiently by circumventing the wsgi process. As such, you'll need to take action specific to your deployment setup to ensure your downloads are only available to authorized clients.

Here's an example nginx snippet that takes advantage of the fact that nginx directs to the [location](http://nginx.org/en/docs/http/ngx_http_core_module.html#location) block with the longest matching "prefix string" to ensure downloads are only served via django views:

```nginx
# The longest matching "prefix string" is selected.
location /static/media/uploads/downloads {
    proxy_pass http://.example.com;
}

location /static {
    alias /path/to/static;
}
```

## Download Optimization

Even though they aren't publicly available you probably still want to serve downloads with your webserver for performance. See [the django-downloadview docs](http://django-downloadview.readthedocs.io/en/latest/optimizations/) for details.

# How it works

There's quite a bit more going on than this, but it's mostly UI hacks. Here's a summary of the mechanics:

1. Monkey patch an inline to our `Download` model onto cartridge/mezzanine's `ProductAdmin`/`FormAdmin`.
2. When a user successfully submits an order/form, create a `Transaction` and an `Acquisition` referencing the `Download`s, add transaction credentials to their session and as query params in a link in the confirmation email, and direct them to the `/downloads/` view.
3. The `/downloads/` view links to `Download`s associated with `Acquisition`s associated with the `Transaction`.

# Development

```console
cd cartridge-downloads
pip install -e . -c constraints.txt

# If python2:
pip install mock

python test
```

Running the Tests
-----------------

- To run browser tests, install python dependencies with `pip install -r dev-requirements.txt`.
- To run browser tests headless, [install phantomjs](http://phantomjs.org/download.html) on your system. A `ghostdriver.log` file is created (and deleted after every TestCase) which may be useful for debugging these, though running them again with firefox is generally easier.

```sh
python test [--debug] [<webdriver>]
```

- *--debug* Write verbose output to ghostdriver.log.
- *\<webdriver\>* [phantomjs|firefox|chrome] If ommitted the browser tests will default to phantomjs and fall back to firefox if unavailable.
