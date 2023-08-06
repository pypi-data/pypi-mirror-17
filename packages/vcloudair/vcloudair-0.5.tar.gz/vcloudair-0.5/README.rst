README
======

vCloud Air lightweight Python SDK
---------------------------------

This is far from a complete vCloud Air (vCA) SDK. However, it does
provide easier access to the newer API features, specifically ANS and
Metrics. It also utilizes the newer and proper login process for vCA
rather than vCD.

There is no guarantee of functionality and/or updates. This is updated
and enhanced as I need the functionality. If there is something I never
use within the API, it's unlikely that it will make its way into this
SDK.

Documentation: http://vcloudair.readthedocs.io/en/latest/

Requirements
------------

- Python 3.4+
- Requests 2.10+

Installation
------------

Run ``pip install vcloudair`` to download and install the package.

Modules
-------

ANS (Advanced Network Services)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module works with the Advanced Network Services API. Current
classes include:

- ``ANSFirewall``
- ``ANSNat``
- ``ANSIPSec``

These allow retrieving, modifying, adding, and saving configurations for
the Firewall and NAT sections, respectively.

Use the ``config_data`` property to access the raw JSON/Dict containing
all information for the ANS section, including the global config
properties.

DR (Disaster Recovery)
~~~~~~~~~~~~~~~~~~~~~~

This module is for Disaster Recovery 2.x (DRaaS) within vCloud Air.
Current classes include:

- ``DisasterRecovery``

The module allows for retrieving a list of DR replications and
initiating test failovers, test recoveries, and actual failovers.

**Note: Use with the On-Demand session class**

Metrics
~~~~~~~

This module works with the newer Metrics API for vCloud Air VPCs and
DCs. A link to the metrics documentation is below in the metrics usage
example.

- ``Metrics``

Query
~~~~~

The classic vCD API has a query system that allows users to query
records for a number of types within the system. These records can be
traversed as resources. However, this library does not include traversal
of resource HREF records.

Queries can be helpful to find out name<->UUID matches, as well a
general count of resources and some basic information (using the fields
parameter).

Current canned query classes include:

- ``VMQuery``
- ``EdgeGatewayQueury``
- ``VAppQuery``
- ``VAppTemplateQuery``
- ``OrgVdcQuery``

Session
~~~~~~~

This module handles the basic login process for vCA and vCD. OAUTH
tokens are generated for vCloud Air and for any Org a user wants to log
into.

- ``VCASession``
- ``VCAODSession``

The VCA session refers to the login session used with VPC and Dedicated
clouds.

The VCA OD session refers to the On-Demand platform and its related
login session and protocols.

Usage Examples
--------------

Logging Into vCloud Air
~~~~~~~~~~~~~~~~~~~~~~~

This is using the VPC/Dedicated login session. **NOT On-Demand!**

.. code-block:: python

    from vcloudair import VCASession

    sess = VCASession('5.6', <username>, <password>)
    sess.login()

    #To show a list of available Orgs you can use the property vdc_names
    print(sess.vdc_names)

    #Membership testing also works
    'orgname' in sess.vdc_names #True / False

    #Alternatively, login() can be called with an org name and return the
    #org data

    sess.login('orgname1')

    #The difference between login() and login_to_vdc() is that the latter
    #will not generate a new VCA token. Only a new/additional vCD token for
    #the org specified.

    sess.login_to_vdc('orgname2')
    org_info = sess.login_to_vdc('orgname3') #Assigns the org data immediately

    #To retrieve the org data from the session later, use the name of the org
    org_info = sess['orgname3']

Organization info stores five pieces of data in a dictionary. The keys
are as follows:

- vcdurl -- The base VCD URL for the instance
- token -- The vCD authorization token
- org\_uuid -- The UUID of the vDC itself
- auth-header -- The name of the authorization header that should be
  used with the token: 'x-vcloud-authorization' in all cases so far.
- version -- The version of the API called

Gathering Metrics
~~~~~~~~~~~~~~~~~

All metrics show up in ~60-second intervals. So, pulling the last 10
minutes worth of metrics will give you ~10 records/timestamps.

.. code-block:: python

    from vcloudair import Metrics

    #Using org_info variable from above...
    #Specifying collection of metrics across the entire VDC (all VMs)
    new_metrics = Metrics(vcdurl=org_info['vcdurl'], token=org_info['token'],
                          org_uuid=org_info['org_uuid'])

    #OR

    new_metrics = Metrics(org_info) #Passing the org_info dict directly into the class

    #OR

    vms = ['vm-UUID1', 'vm-UUID2']
    new_metrics = Metrics(org_info, vm_uuids=vms) #Pull only 2 VM metrics.

    #Passing in VM UUIDs will override passing in an entire Org

    new_metrics.set_relative_interval('HOUR', 1) #Previous 1 hour
    new_metrics.set_metric_filters('cpu.ready.summation') #Limit the metric results to only CPU ready

    #Add 2 additional filters without clearing the previous
    new_metrics.add_metric_filters('cpu.usage.average', 'cpu.idle.summation')

    new_metrics.collect() #Makes the API call

    #Data is stored in the metric_data instance variable
    #metric_data['vmUUID']['timestamp']['metric-name']

`Full Metrics
Docs <https://pubs.vmware.com/vca/topic/com.vmware.vca.metrics.api.doc/GUID-A796113C-A7BA-441A-BD44-329A813C5BA3.html>`_

Querying Edges
~~~~~~~~~~~~~~

Standard query results for all query types include UUID and Name fields
only. The UUID is used as the dictionary key with all other fields
stored in a subsequent dictionary as the value

``results['item_uuid']['field']``

Query types also have a ``find_by_name('name')`` method which returns a
list of UUIDs that have a matching 'name' attribute to the string passed
into the method.

.. code-block:: python

    from vcloudair import EdgeGatewayQuery

    egwq = EdgeGatewayQuery(org_info)
    egwq.execute() #Run the query

    print(egwq.results) #All results are stored in the results instance variable

    egwq.set_fields('applicable', 'query', 'field', 'names') #vCD docs discuss query fields
    egwq.execute() #Execute the query again to add the fields to results

    edge_uuids = egwq.find_by_name('edge_name')

`vCD Query
Documentation <https://pubs.vmware.com/vca/topic/com.vmware.vcloud.api.doc_56/GUID-4FD71B6D-6797-4B8E-B9F0-618F4ACBEFAC.html>`_

Retrieving ANS Firewall Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NAT configuration works the same as the Firewall. Iteration and
retrieving rules is also done using slicing or index-based calls as
shown below.

.. code-block:: python

    from vcloudair import ANSFirewall

    fw = ANSFirewall('edge-UUID', org_info)
    fw.get_config()

    fw[0] #Retrieve the first rule
    del fw[2] #Delete the rule at index 2
    for rule in fw: #Iterate through the rules
        print(rule)

Adding A Rule
~~~~~~~~~~~~~

.. code-block:: python

    #The first three arguments do not have default vaules. The remaining ones do.
    fw.add_rule('Rule Name', source='external', destination='23.45.67.89', action='accept',
        protocol='tcp', source_port='any', dest_port=80)

Saving ANS Firewall Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    fw.save_config() #Pushes the config back to the server via API

Adding an IPSec VPN
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from vcloudair import ANSIPSec

    ipsec = ANSIPSec('edge-UUID', org_info)
    ipsec.get_config()
    ipsec.add_psk_tunnel('TestTunnel', local_id='23.92.255.65',
                                    local_ip='23.92.255.65',
                                    peer_id='195.177.229.88',
                                    peer_ip='195.177.229.88',
                                    local_subnets='10.0.50.0/24,10.0.51.0/24',
                                    peer_subnets=['10.0.40.0/24','10.0.41.0/24'],
                                    psk='ABcdEFghIJklMNopQRstUVwxYZ1234567890')

    # Optional, defaulted, parameters include DH Group, PFS, and encryption algorithm

    ipsec.save_config()

Initiating A Full DR Failover Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from vcloudair import VCAODSession, DisasterRecovery

    sesh = VCAODSession('5.7', 'username', 'password')
    print('Logging into On-Demand')
    sesh.login()

    #Print out the instance list and their indexes
    sesh.show_instance_list()

    print('Logging into DR Instance')
    instance_data = sesh.login_to_instance(0) #In this example, instance 0 is the DR instance

    dr = DisasterRecovery(instance_data)

    print('Retrieving Replications')
    dr.retrieve_replications()

    print('Testing Failover')
    dr.do_test_failover(power_on=True, total=True)
    #... Wait appropriate time
    dr.do_test_cleanup(total=True)
