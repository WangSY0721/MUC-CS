transcript on
if {[file exists rtl_work]} {
	vdel -lib rtl_work -all
}
vlib rtl_work
vmap work rtl_work

vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/InstructionCut.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/RegFile.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/Cpu.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/result.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/unitcontrol.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/mux2_1.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/mux2_1_5.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/extend.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/myalu.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/datamem.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/instructionmem.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/inputnumber.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/inputextend.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/pc.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/add.v}
vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu {D:/Users/Berton/Desktop/SingleCPU/AMycpu/left.v}

vlog -vlog01compat -work work +incdir+D:/Users/Berton/Desktop/SingleCPU/AMycpu/simulation/modelsim {D:/Users/Berton/Desktop/SingleCPU/AMycpu/simulation/modelsim/Cpu.vt}

vsim -t 1ps -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclonev_ver -L cyclonev_hssi_ver -L cyclonev_pcie_hip_ver -L rtl_work -L work -voptargs="+acc"  Cpu_vlg_tst

add wave *
view structure
view signals
run 2000 ns
