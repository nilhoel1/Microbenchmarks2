cmd_/home/bossow/benchmark/kernel_module/modules.order := {   echo /home/bossow/benchmark/kernel_module/activate_el0_access_to_pmu_cycle_counters.ko; :; } | awk '!x[$$0]++' - > /home/bossow/benchmark/kernel_module/modules.order