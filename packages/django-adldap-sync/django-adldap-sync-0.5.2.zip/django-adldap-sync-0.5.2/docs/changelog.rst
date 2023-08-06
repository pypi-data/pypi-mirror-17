.. _changelog:

Changelog
=========

These are the notable changes for each django-ldap-sync release. For
additional detail, read the complete `commit history`_.

**django-adldap-sync 0.5.0**
   * Complete overhaul of the system. Renamed to django-adldap-sync
   * Added Group Membership Synchronization
   * Added Incremental Synchronization
   * Added support for failover ldap servers
   * Added a simple way to populate User Profiles
   * Support for importing thumbnailPhoto to ImageField
   * Added support for ignoring users on import
   * Created a model for storing last update time, and statistics

**django-ldap-sync 0.4.0**
   * Fix error when synchronizing groups
   * Add setting to retrieve additional LDAP attributes
   * Pass attributes to user callback functions
   * Add example callback for disabling users with AD userAccountControl

**django-ldap-sync 0.3.2**
   * Fix packaging errors

**django-ldap-sync 0.3.0**
   * Add a setting to override the username field
   * Add handling of removed users
   * Implement callbacks for added/changed and removed users

**django-ldap-sync 0.2.0**
   * Handle DataError exception when syncing long names (thanks @tomrenn!)
   * Change Celery task to use @shared_task decorator

**django-ldap-sync 0.1.1**
   * Fix exception with AD internal referrals

**django-ldap-sync 0.1.0**
   * Initial release

.. _commit history: https://github.com/marchete/django-adldap-sync/commits/
