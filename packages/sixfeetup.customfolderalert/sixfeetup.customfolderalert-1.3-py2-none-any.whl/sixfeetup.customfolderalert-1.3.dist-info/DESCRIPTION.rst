Introduction
============

This product will let you know if there are some files in the custom folder of your Plone site by displaying a red message at the top of the page. You can disable it by using the variable DISABLE_CUSTOMFOLDER_ALERT.

It is recommended to use this product only in debug mode.

Changelog
=========

1.1 (2011-07-19)
----------------

- Added an uninstall profile so that this product can be cleanly removed
  [clayton]
- Report the number of items in the custom folder
  [clayton]
- Clean up the javascript a bit so it is more readable
  [clayton]
- Convert variable names to lowercase as they are not globals
  [clayton]
- Only alert on custom folder paths in the active skin
  [clayton]
- Move everything to the `alert_view` view class
  [clayton]
- Make sure the alert is always visible and does not take up any space
  [clayton]

1.0 (2011-02-15)
----------------

- Remove ``paster_plugins`` and ``setup_requires`` so that install does
  not fail on Windows
  [clayton]
- Bump version to 1.0 as this has proven stable
  [clayton]

0.2 (2010-08-23)
----------------
- added a version.txt file so it is read by portal_quickinstaller,
  [lucie]
- updated setup.py to read this new version.txt file,
  [lucie]
- updated configure.zcml so the egg is considered as a package,
  [lucie]
- removed old code from init.py
  [lucie]
- added a view class so we can test if the alert has been disabled by an
  environment variable
  [lucie]

0.1 (2010-08-04)
----------------

- Initial release
  [lucielejard]


