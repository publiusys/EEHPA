# Linux perf

### Install
```
hand32@node1:~$ perf stat
Command 'perf' not found, but can be installed with:
apt install linux-intel-iotg-tools-common        # version 5.15.0-1066.72, or
apt install linux-nvidia-6.2-tools-common        # version 6.2.0-1003.3~22.04.1
apt install linux-nvidia-tegra-igx-tools-common  # version 5.15.0-1018.18
apt install linux-nvidia-tools-common            # version 5.15.0-1066.67
apt install linux-tools-common                   # version 5.15.0-124.134
apt install linux-nvidia-5.19-tools-common       # version 5.19.0-1014.14
apt install linux-nvidia-tegra-tools-common      # version 5.15.0-1028.28
apt install linux-xilinx-zynqmp-tools-common     # version 5.15.0-1037.41
Ask your administrator to install one of them.

hand32@node1:~$ sudo apt install -y linux-tools-common

hand32@node1:~$ perf stat
WARNING: perf not found for kernel 5.15.0-131

  You may need to install the following packages for this specific kernel:
    linux-tools-5.15.0-131-generic
    linux-cloud-tools-5.15.0-131-generic

  You may also want to install one of the following packages to keep up to date:
    linux-tools-generic
    linux-cloud-tools-generic

hand32@node1:~$ sudo apt install -y linux-tools-5.15.0-131-generic

hand32@node1:~$ perf stat
Error:
Access to performance monitoring and observability operations is limited.
Consider adjusting /proc/sys/kernel/perf_event_paranoid setting to open
access to performance monitoring and observability operations for processes
without CAP_PERFMON, CAP_SYS_PTRACE or CAP_SYS_ADMIN Linux capability.
More information can be found at 'Perf events and tool security' document:
https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html
perf_event_paranoid setting is 4:
  -1: Allow use of (almost) all events by all users
      Ignore mlock limit after perf_event_mlock_kb without CAP_IPC_LOCK
>= 0: Disallow raw and ftrace function tracepoint access
>= 1: Disallow CPU event access
>= 2: Disallow kernel profiling
To make the adjusted perf_event_paranoid setting permanent preserve it
in /etc/sysctl.conf (e.g. kernel.perf_event_paranoid = <setting>)

hand32@node1:~$ sudo sysctl kernel.perf_event_paranoid=-1
kernel.perf_event_paranoid = -1

hand32@node1:~$ perf stat
^C
 Performance counter stats for 'system wide':

         26,545.95 msec cpu-clock                 #   39.963 CPUs utilized
               237      context-switches          #    8.928 /sec
                40      cpu-migrations            #    1.507 /sec
                 0      page-faults               #    0.000 /sec
        22,466,992      cycles                    #    0.001 GHz
         5,646,054      instructions              #    0.25  insn per cycle
         1,137,695      branches                  #   42.858 K/sec
            88,397      branch-misses             #    7.77% of all branches

       0.664265588 seconds time elapsed

hand32@node0:~/EEHPA/perfstatpower$ perf stat -a -e power/energy-pkg/ -x, -I 1000
     1.001078602,9.93,Joules,power/energy-pkg/,2002451247,100.00,,
     2.002387877,9.76,Joules,power/energy-pkg/,2002592581,100.00,,
     3.003655992,10.02,Joules,power/energy-pkg/,2002563684,100.00,,
     4.004907665,10.41,Joules,power/energy-pkg/,2002350930,100.00,,
     4.318790534,3.50,Joules,power/energy-pkg/,627845304,100.00,,
```