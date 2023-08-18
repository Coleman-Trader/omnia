Adding new nodes
+++++++++++++++++

**Provisioning the new node**

While adding a new node to the cluster, users can modify the following:

    - The operating system
    - CUDA
    - OFED

A new node can be added using the following ways:

1. When the discovery mechanism is ``switch-based``:

    * Edit or append JSON list stored in ``switch-based-details`` in ``input/provision_config.yml``.

    .. note::
        * All ports residing on the same switch should be listed in the same JSON list element.
        * Ports configured via Omnia should be not be removed from ``switch-based-details`` in ``input/provision_config.yml``.


    * Run ``provision.yml``.

2. When the discovery mechanism is ``mapping``:

    * Update the existing mapping file by appending the new entry (without the disrupting the older entries) or provide a new mapping file by pointing ``pxe_mapping_file_path`` in ``provision_config.yml`` to the new location.

    * Run ``provision.yml``.

3. When the discovery mechanism is ``snmpwalk``:

    * Run ``provision.yml`` once the switch has discovered the potential new node.

4. When the discovery mechanism is ``bmc``:

    * Run ``provision.yml`` once the node has joined the cluster using an IP that exists within the provided range.


Alternatively, if a new node is to be added with no change in configuration, run the following commands: ::

            cd provision
            ansible-playbook discovery_provision.yml


**Adding the new node to the cluster**

1. Insert the new IPs in the existing inventory file following the below example.

*Existing inventory*

::

    [manager]
    10.5.0.101

    [compute]
    10.5.0.102
    10.5.0.103

    [login]
    10.5.0.104

*Updated inventory with the new node information*

::

    [manager]
    10.5.0.101

    [compute]
    10.5.0.102
    10.5.0.103
    10.5.0.105
    10.5.0.106

    [login]
    10.5.0.104

In the above example, nodes 10.5.0.105 and 10.5.0.106 have been added to the cluster as a compute nodes.

.. note::
    * Do not change the manager node in the existing inventory. Simply add the new node information in the compute group.
    * Only the ``scheduler_type`` in ``input/omnia_config.yml`` and the variables in ``input/storage_config.yml`` can be updated while re-running ``omnia.yml`` to add the new node. All other variables in the files ``input/omnia_config.yml`` and ``input/security_config.yml`` must be unedited.

3. To install `security <BuildingClusters/Authentication.html>`_, `job scheduler <BuildingClusters/installscheduler.html>`_ and storage tools (`NFS <BuildingClusters/NFS.html>`_, `BeeGFS <BuildingClusters/BeeGFS.html>`_) on the node, run ``omnia.yml``: ::

    ansible-playbook omnia.yml -i inventory



