<Tool to automatically generate microbechmarks for latency,
throughput and port usage on modern RISC architecture>
Copyright (C) <2023>  <Marvin Bossow>


This project is made for the bachelor thesis at the technical university Dortmund, faculty of inforamtics, ls12 embedded systems group.

Title:  Automatic generation of ISA microbenchmarks for RISC microarchitectures port usage
Author: Marvin Bossow

The micro benchmarks are made on and for the test system: raspberry pi 400, but should be able to run on all compatible armv8 aarch64 processors with the correct performance monitoring extension (FEAT_PMUv3).

Manual:

1. Load kernel module to unlock el0 / user mode access to the pmu cycle counter:
    this can be done using "insmod":
        build the file to load into the kernel module: in the folder "kernel_module" call: "make"
        load the kernel module into the kernel:        in the folder "kernel_module" call: "sudo insmod activate_el0_access_to_pmu_cycle_counters.ko"
    or "modprobe":
        build the file to load into the kernel module: in the folder "kernel_module" call: "sudo make install"
        load the kernel module into the kernel:        in the folder "kernel_module" call: "sudo modprobe activate_el0_access_to_pmu_cycle_counters"

2. Generate benchmarks:
    Depending on which type of benchmarks you want to generate, run latency_automated.py, throughput_automated.py or port_usage_automated.py. (be aware that the creation of your benchmarks might take some time, depending on your system)

3. Execute the benchmarks:
    Execute the corresponding python script to your created benchmarks (run_*_tests.py).
    The results will be saved in a CSV file, of which the name will be printed in to the console.

4. Extension of benchmarked instructions:
    Create a new object for your instruction in the folder library, which has to use the attributes of instruction.py. (In case of unusual instruction, in terms of syntax, implementation of generate_instruction_block might be needed for your object).
    Use your newly created instruction in generator.py, as shown for all the other instructions.


Have fun micro benchmarking your armv8 aarch64 system.
If you have questions feel free to read my bachelor thesis, which will explain this work in more detail.