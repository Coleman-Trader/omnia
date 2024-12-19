Prerequisites
=================

1. Choose a server outside of your intended cluster with the mentioned `storage requirements <RHELSpace.html>`_ to function as your Omnia Infrastructure Manager (OIM).

2. Ensure that the OIM has a full-featured RHEL operating system (OS) installed. For a complete list of supported OS versions, check out the `Support Matrix <../../Overview/SupportMatrix/OperatingSystems/index.html>`_.

3. Enable the **AppStream** and **BaseOS** repositories via the RHEL subscription manager.

4. Ensure that the OIM needs is internet-capable with Git installed. If Git is not installed, use the below commands to install it. ::

    dnf install git -y

.. note:: If the OIM server has an Infiniband NIC installed, run the below command to install the hardware drivers and Infiniband-related packages:
    ::
        yum groupinstall "Infiniband Support" -y

5. Clone the Omnia repository from GitHub on to the OIM server using the following command: ::

    git clone https://github.com/dell/omnia.git

6. [Optional] `Set up a proxy server for the OIM <Setup_CP_proxy.html>`_.

