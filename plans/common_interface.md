# Common Interface for Providers

## VM

| Field       | Type             | Description                                    |
| ----------- | ---------------- | ---------------------------------------------- |
| name        | string           | The name of Virtual Machine                    |
| image       | blob             | The file to use as the virtual machine's OS    |
| network     | string           | The virtual network this VM belongs to         |
| firewall    | firewall_rules   | The firewall rules for this VM                 |

## Network

| Field       | Type             | Description                                    |
| ----------- | ---------------- | ---------------------------------------------- |
| name        | string           | The name of the network                        |
| firewall    | firewall_rules   | The firewall rules for this network


