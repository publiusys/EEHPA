# ipmitool - utility for controlling IPMI-enabled devices

### Install
```
sudo apt install ipmitool
```

### Example
```
hand32@node1:~$ sudo ipmitool sdr type
Sensor Types:
	Temperature               (0x01)   Voltage                   (0x02)
	Current                   (0x03)   Fan                       (0x04)
	Physical Security         (0x05)   Platform Security         (0x06)
	Processor                 (0x07)   Power Supply              (0x08)
	Power Unit                (0x09)   Cooling Device            (0x0a)
	Other                     (0x0b)   Memory                    (0x0c)
	Drive Slot / Bay          (0x0d)   POST Memory Resize        (0x0e)
	System Firmwares          (0x0f)   Event Logging Disabled    (0x10)
	Watchdog1                 (0x11)   System Event              (0x12)
	Critical Interrupt        (0x13)   Button                    (0x14)
	Module / Board            (0x15)   Microcontroller           (0x16)
	Add-in Card               (0x17)   Chassis                   (0x18)
	Chip Set                  (0x19)   Other FRU                 (0x1a)
	Cable / Interconnect      (0x1b)   Terminator                (0x1c)
	System Boot Initiated     (0x1d)   Boot Error                (0x1e)
	OS Boot                   (0x1f)   OS Critical Stop          (0x20)
	Slot / Connector          (0x21)   System ACPI Power State   (0x22)
	Watchdog2                 (0x23)   Platform Alert            (0x24)
	Entity Presence           (0x25)   Monitor ASIC              (0x26)
	LAN                       (0x27)   Management Subsys Health  (0x28)
	Battery                   (0x29)   Session Audit             (0x2a)
	Version Change            (0x2b)   FRU State                 (0x2c)

hand32@node1:~$ sudo ipmitool sdr type 0x08
PSU1_STATUS      | 26h | ok  | 10.1 | Presence detected
PSU1_PWRGD       | 28h | ok  | 10.1 | State Asserted
PSU1_POUT        | 2Bh | ok  | 10.1 | 120 Watts
PSU2_STATUS      | 2Ch | ok  | 10.2 |
PSU2_PWRGD       | 2Eh | ns  | 10.2 | No Reading
PSU2_POUT        | 31h | ns  | 10.2 | No Reading
PS_RDNDNT_MODE   | ADh | ok  | 20.0 | Non-Redundant: Sufficient from Redundant
POWER_USAGE      | AEh | ok  |  7.0 | 128 Watts
PSU1_PIN         | AFh | ok  | 10.1 | 128 Watts
PSU2_PIN         | B0h | ns  | 10.2 | No Reading

hand32@node1:~$ sudo ipmitool sdr get POWER_USAGE
Sensor ID              : POWER_USAGE (0xae)
 Entity ID             : 7.0 (System Board)
 Sensor Type (Threshold)  : Power Supply (0x08)
 Sensor Reading        : 120 (+/- 4) Watts
 Status                : ok
 Upper non-recoverable : 1552.000
 Upper critical        : 1400.000
 Positive Hysteresis   : Unspecified
 Negative Hysteresis   : Unspecified
 Minimum sensor range  : Unspecified
 Maximum sensor range  : Unspecified
 Event Message Control : Per-threshold
 Readable Thresholds   : ucr unr
 Settable Thresholds   : ucr unr
 Threshold Read Mask   : ucr unr
 Assertion Events      :
 Assertions Enabled    : ucr+ unr+
 Deassertions Enabled  : ucr+ unr+
```