#include <linux/module.h>   // Needed for all Modules
#include <linux/kernel.h>   // Needed for "KERN_INFO" ("printk(...)")
#include <linux/init.h>     // Needed for the macros

#define PMUSERENR_EL0__EN   (1 << 0)    // Enables EL0 access to PMU Registers
#define PMUSERENR_EL0__CR   (1 << 2)    // Enables EL0 to read the Cycle Counters ("PMCCNTR_EL0")
// See: https://developer.arm.com/documentation/ddi0595/2021-12/AArch64-Registers/PMUSERENR-EL0--Performance-Monitors-User-Enable-Register?lang=en

#define PMCNTENSET_EL0__C   (1 << 31)   // Enables the Cycle Counter Register ("PMCCNTR_EL0")
// See: https://developer.arm.com/documentation/ddi0595/2021-12/AArch64-Registers/PMCNTENSET-EL0--Performance-Monitors-Count-Enable-Set-register?lang=en

#define PMCR_EL0__E         (1 << 0)    // Enables the PMU Counters
// See: https://developer.arm.com/documentation/ddi0595/2021-12/AArch64-Registers/PMCR-EL0--Performance-Monitors-Control-Register?lang=en

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Timo Stapel");
MODULE_DESCRIPTION("Enables EL0 (user-mode) access to PMU Cycle Counters on ARMv8 AARCH64 Processors.");

// Nice Tutorial (just for getting started, please check with ARMs documentations after understanding this): http://zhiyisun.github.io/2016/03/02/How-to-Use-Performance-Monitor-Unit-(PMU)-of-64-bit-ARMv8-A-in-Linux.html

// Insert Kernel Module:                "insmod <name>.ko"      ||      "modprobe <name>"
// See if Kernel Module is loaded:      "lsmod"
// Read "printk(...)"-log:              "dmesg"
// remove Kernel Module:                "rmmod <name>"          ||      "modprobe -r <name>"

static void activate_el0_access_to_pmu_cycle_counters(void (*vp))
{
    // Enable EL0 (User-Mode) Access to PMU Cycle Counters
    asm volatile("msr pmuserenr_el0, %0" : : "r" (PMUSERENR_EL0__EN | PMUSERENR_EL0__CR));

    // Enable the Cycle Count Register
    unsigned long long a = 0;
    asm volatile("mrs %0, pmcntenset_el0" : "=r" (a));
    //printk(KERN_INFO "PMCNTENSET_EL0: %lu\n", a);                               // Optional: to see which event counters are enabled
    asm volatile("msr pmcntenset_el0, %0" : : "r" (a | PMCNTENSET_EL0__C));     // Do not change anything else: read before and only set the one bit

    // Enable PMU Counters
    unsigned long long b = 0;
    asm volatile("mrs %0, pmcr_el0" : "=r" (b));
    //printk(KERN_INFO "PMCR_EL0: %lu\n", b);                                     // Optional: to see details of the Performance Monitors implementation (like how many event counters are implemented)
    asm volatile("msr pmcr_el0, %0" : : "r" (b | PMCR_EL0__E));                 // Do not change anything else: read before and only set the one bit
}

static int __init activate(void)
{
    printk(KERN_INFO "Activating Module and granting EL0 access to PMU Cycle Counters ...\n");

    // Activate El0 access to the PMU Cycle Counter on each CPU (Core)
    on_each_cpu(&activate_el0_access_to_pmu_cycle_counters, NULL, 0);

    printk(KERN_INFO "Module activated.\n");

    return 0;
}

static void __exit deactivate(void)
{
    printk(KERN_INFO "Removing Module ...\n");

    printk(KERN_INFO "This does NOT disable EL0 access to PMU Cycle Counters! Please restart your machine.\n");

    printk(KERN_INFO "Module removed.\n");
}

module_init(activate);
module_exit(deactivate);

