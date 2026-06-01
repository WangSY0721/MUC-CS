transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/MultiCycleCPU.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/div_20.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/SignZeroExtend.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/show.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/RegisterFile.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/PCAddr.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/PC.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/InstructionCut.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/DataMEM.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/ControlUnit.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/ALU.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/CLKmode.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/IO.v}
vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU {D:/altera/15.0/MultiCycleCPU/InsMEM.v}

vlog -vlog01compat -work work +incdir+D:/altera/15.0/MultiCycleCPU/simulation/modelsim {D:/altera/15.0/MultiCycleCPU/simulation/modelsim/MultiCycleCPU.vt}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cycloneive_ver -L rtl_work -L work -voptargs="+acc"  MultiCycleCPU_vlg_tst

add wave *
view structure
view signals
run 2000 ps
