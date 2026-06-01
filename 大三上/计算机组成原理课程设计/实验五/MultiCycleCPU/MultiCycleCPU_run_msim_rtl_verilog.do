transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/MultiCycleCPU.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/div_20.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/SignZeroExtend.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/show.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/RegisterFile.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/PCAddr.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/PC.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/InstructionCut.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/ControlUnit.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/ALU.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/CLKmode.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/IO.v}
vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU {D:/MultiCycleCPU/totalmem.v}

vlog -vlog01compat -work work +incdir+D:/MultiCycleCPU/simulation/modelsim0 {D:/MultiCycleCPU/simulation/modelsim0/MultiCycleCPU.vt}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cycloneive_ver -L rtl_work -L work -voptargs="+acc"  MultiCycleCPU_vlg_tst

add wave *
view structure
view signals
run 2000 ps
