obj-m = activate_el0_access_to_pmu_cycle_counters.o

KERNEL_DIRECTORY = /lib/modules/$(shell uname -r)/build/
WORKING_DIRECTORY = $(shell pwd)

all:
	make -C $(KERNEL_DIRECTORY) M=$(WORKING_DIRECTORY) modules

install:
	make -C $(KERNEL_DIRECTORY) M=$(WORKING_DIRECTORY) modules_install		# needed for install with "modprobe <name>"		|	else: install with "insmod <name>.ko"

clean:
	make -C $(KERNEL_DIRECTORY) M=$(WORKING_DIRECTORY) clean

