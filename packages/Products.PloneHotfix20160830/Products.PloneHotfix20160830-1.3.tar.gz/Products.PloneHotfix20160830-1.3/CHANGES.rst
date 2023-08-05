Changelog
=========


1.3 (2016-09-08)
----------------

- Added ``allow_prefill_from_GET_request`` attribute check.  With this
  hotfix, we only use data from the request when the request method
  matches the form method.  If you have a z3c.form where this
  protection is not wanted, you can add an attribute
  ``allow_prefill_from_GET_request`` on the form and set it to a True
  value.  If you want, you can import this attribute name from
  ``Products.PloneHotfix20160830.z3c_form.ALLOW_PREFILL``.  You only
  need to update to this version of the hotfix if you have forms where
  this is needed.


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
