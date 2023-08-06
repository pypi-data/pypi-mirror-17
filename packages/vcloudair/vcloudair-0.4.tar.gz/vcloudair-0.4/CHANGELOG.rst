.. :changelog:

Changelog
=========

Version 0.4 (2016-09-22)
------------------------

**Improvements**

- ``DisasterRecovery`` class methods ``do_failover``, ``do_test_failover``, and
  ``do_test_cleanup`` now support multiple UUIDs being submitted to the calls.
  E.g.: ``DisasterRecovery.do_failover('uuid1', 'uuid2', 'uuid3')``.
- Switched to a threaded model for failover and recovery tasks. Failover and
  recovery tasks use the same task queue for the threads. So the total number of
  concurrent operations is a combined total of both failover and recovery. Any
  additional operations are simply added to the queue. The queue is processed
  in a First-In-First-Out fashion.
- Switched to a threaded model when retrieving replications. This does not use
  the same queue as the DR operations above. Currently it is unbounded as it
  happens once during the login process. Will determine if this should be moved
  to a pool model instead.

**New Features**

- ``DisasterRecovery`` method ``dump_replication_details`` will allow output of
  all DR replications for a particular instance to be saved to a file. This is
  to help with the creation of automation tasks by showing a match between VM
  name and UUID.

**Bugfixes**

- Added a timeout to the task monitoring (10min default) so the blocking call
  for failovers and recovery won't hang indefinitely if a task is hung in vCD.

Version 0.3 (2016-09-12)
------------------------

- Published to PyPI

**Improvements**

- Cleaned up the On-Demand instance display table by adding friendly names and
  region information

**Misc**

- Converted MD files to RST format

Version 0.2 (2016-09-09)
------------------------

**New Features**

- Added a new session class for logging into On-Demand instances. This
  includes DR 2.x (DRaaS)
- Added a new module for Disaster Recovery and a new class
  ``DisasterRecovery``

Version 0.1
-----------

- Initial Release
