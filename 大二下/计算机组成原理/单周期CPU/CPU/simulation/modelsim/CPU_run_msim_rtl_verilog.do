transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/result.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/regfile.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/control.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/instructionslice.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/insmem.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/pc.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/mux.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/alu.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/inmediateextend.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/add.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/left.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/mux4.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/inputextend.v}
vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU {D:/altera/Compute/lab6/CPU/inputdata.v}

vlog -vlog01compat -work work +incdir+D:/altera/Compute/lab6/CPU/simulation/modelsim {D:/altera/Compute/lab6/CPU/simulation/modelsim/CPU.vt}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cycloneive_ver -L rtl_work -L work -voptargs="+acc"  CPU_vlg_tst

add wave *
view structure
view signals
run 200 ns
