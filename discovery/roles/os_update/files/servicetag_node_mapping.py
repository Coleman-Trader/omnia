#  Copyright 2024 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys
import syslog
import subprocess

role_path = sys.argv[1]
file_path = sys.argv[2]
inventory_hostname = sys.argv[3]
db_path = role_path + file_path
kernel_params = sys.argv[4]

sys.path.insert(0, db_path)

import omniadb_connection as omniadb

def service_tag_node_mapping():
    """
    outputs the node name for the service tag or admin IP 
    and runs chdef command to add the kernel parameters

    """
    try:
        # Create a database connection
        connection = omniadb.create_connection()
        cursor = connection.cursor()

        node_name = ""
        # Check if the inventory hostname(can be service tag, or admin_IP) is not empty 
        if len(inventory_hostname) > 0:

            # Query string: get host IP if service tag or node name is given
            query = "select node from cluster.nodeinfo where service_tag=%s or node=%s"
            params = (inventory_hostname.upper(), inventory_hostname)

            # Query execution
            cursor.execute(query, params)
            row = cursor.fetchone()

            if row:
                # Collect host ip if result is valid
                node_name = row[0]
                print(f"{node_name}")
            else:
                syslog.syslog(syslog.LOG_INFO,
                    f"servicetag_node_mapping:service_tag_node_mapping(): query failed to fetch node name for service tag: {inventory_hostname}")
                
                query = "select node from cluster.nodeinfo where admin_ip=%s"
                params = (inventory_hostname,)

                # Query execution
                cursor.execute(query, params)
                row = cursor.fetchone()

                if row:
                    # Collect host ip if result is valid
                    node_name = row[0]
                    print(f"{node_name}")
        
        if len(node_name) > 0:
            command = ["/opt/xcat/bin/chdef", node_name, f"addkcmdline={kernel_params}"]
            print(f"{command}")
            subprocess.run(command)

        # Close the cursor and connection
        cursor.close()
        connection.close()
    except (ValueError) as err:
        print(f'{type(err).__name__}: {err}')
    except (OSError, Exception) as err:
        print(f"servicetag_node_mapping: service_tag_node_mapping: {type(err).__name__}: {err}")


if __name__ == "__main__":
    service_tag_node_mapping()
