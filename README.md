# EEHPA: Energy Efficient Horizontal Pod Autoscaler

## Hardware Info
| Name          | Link                                                                  | Threads |
| :-------------| :------                                                               | :------ |
| c220g1        |   https://www.wisc.cloudlab.us/portal/show-hardware.php?type=c220g1   | 32      |
| sm220u        |   https://www.wisc.cloudlab.us/portal/show-hardware.php?type=sm220u   | 64      |

## Experimental Setup

### Baselines
System          | DVFS           | Config     |
| :-------------| :------------- | :------    |
| HPA           | ondemand       | 2 x sm220u |
| Cilantro      | ondemand       | 2 x sm220u |
| Ax            | ondemand       | 2 x sm220u |
| HPA           | performance    | 2 x sm220u |
| Cilantro      | performance    | 2 x sm220u |
| Ax            | performance    | 2 x sm220u |

System          | DVFS           | Config     |
| :-------------| :------------- | :------    |
| HPA           | ondemand       | 4 x c220g1 |
| Cilantro      | ondemand       | 4 x c220g1 |
| Ax            | ondemand       | 4 x c220g1 |
| HPA           | performance    | 4 x c220g1 |
| Cilantro      | performance    | 4 x c220g1 |
| Ax            | performance    | 4 x c220g1 |

### Mix old and new hardware
System          | DVFS           | Config                 |
| :-------------| :------------- | :------                |
| HPA           | ondemand       | 2 x c220g1, 1 x sm220u |
| Cilantro      | ondemand       | 2 x c220g1, 1 x sm220u |
| Ax            | ondemand       | 2 x c220g1, 1 x sm220u |
| HPA           | performance    | 2 x c220g1, 1 x sm220u |
| Cilantro      | performance    | 2 x c220g1, 1 x sm220u |
| Ax            | performance    | 2 x c220g1, 1 x sm220u |

### Ax Multi-Objective
System          | DVFS           | Config                 |
| :-------------| :------------- | :------                |
| Ax            | ondemand       | 4 x c220g1, 2 x sm220u |
| Ax            | performance    | 4 x c220g1, 2 x sm220u |