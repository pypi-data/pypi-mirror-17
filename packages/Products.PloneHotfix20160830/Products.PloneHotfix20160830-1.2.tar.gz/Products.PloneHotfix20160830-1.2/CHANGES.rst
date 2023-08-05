Changelog
=========

1.2 (2016-09-06)
----------------

- Fix plone.app.discussion patch to still work for deleting comments on
  versions older than 2.3.3

1.1 (2016-09-01)
----------------

- Fixed z3c.form patch for Plone 3.  Plone 3 does not use z3c.form by
  default.  If you have an add-on that *does* use it, you should
  upgrade, otherwise you get errors when showing such a form.  Plone 4
  and higher work fine with the previous version of the patch.

- Updated plone.app.users patch to work on Plone 4.x even though it is
  not vulnerable.  On standard Plone 4 there should be no reason to
  upgrade to this version.  If you have custom code that changes
  ``UserDataPanel`` you may need this update though.  There is a
  simple check: if on Plone 4 as Manager when you visit
  ``@@user-information?userid=non-existing-user`` you get an error,
  then you are safe.


1.0 (2016-08-30)
----------------

- Initial release
