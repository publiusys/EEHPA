# EEHPA: Energy Efficient Horizontal Pod Autoscaler

## Hardware Info
| Name          | Link                                                                  | Threads |
| :-------------| :------                                                               | :------ |
| c220g1        |   https://www.wisc.cloudlab.us/portal/show-hardware.php?type=c220g1   | 32      |
| sm220u        |   https://www.wisc.cloudlab.us/portal/show-hardware.php?type=sm220u   | 64      |

## Experimental Setup

### Baselines
System          | DVFS           | Config     | Files    | Avg P99 (ms) | Power (W) |
| :-------------| :------------- | :------    | :------  | :--------    | :-------- |
| HPA           | performance    | 2 x sm220u | 242      | 1171         | 371       |
| Cilantro      | performance    | 2 x sm220u | 814      | 3169         | 334       |
| Ax            | performance    | 2 x sm220u | 414      | 237          | 345       |

System          | DVFS           | Config     | Files    | Avg P99 (ms) | Power (W) |
| :-------------| :------------- | :------    | :------  | :----------  | :-------- | 
| HPA           | performance    | 4 x c220g1 | 241      | 1305         | 274       |
| Cilantro      | performance    | 4 x c220g1 | 1313     | 5188         | 235       |
| Ax            | performance    | 4 x c220g1 | 240      | 680          | 199       |

### Mix old and new hardware
System          | DVFS           | Config                 | Files    | Avg P99 (ms) | Power (W) |
| :-------------| :------------- | :------                | :------  | :----------  | :-------- | 
| HPA           | performance    | 2 x c220g1, 1 x sm220u | 365      | 994          | 321       |
| Cilantro      | performance    | 2 x c220g1, 1 x sm220u | 959      | 1373         | 270       |
| Ax            | performance    | 2 x c220g1, 1 x sm220u | 157      | 193          | 238       |

### Ax Multi-Objective
System          | DVFS           | Config                 | Files    | Avg P99 (ms) | Power (W) |
| :-------------| :------------- | :------                | :------  | :----------  | :-------- | 
| Ax            | performance    | 3 x c220g1, 2 x sm220u | 238      | 100           | 369       |