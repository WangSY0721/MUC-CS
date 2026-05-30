transcript on
if {[file exists gate_work]} {
	vdel -lib gate_work -all
}
vlib gate_work
vmap work gate_work

vlog -vlog01compat -work work +incdir+. {lab2_4.vo}

vlog -vlog01compat -work work +incdir+E:/Quartus_Projects/lab2_4/simulation/modelsim {E:/Quartus_Projects/lab2_4/simulation/modelsim/lab2_4.vt}

vsim -t 1ps +transport_int_delays +transport_path_delays -L altera_ver -L cycloneive_ver -L gate_work -L work -voptargs="+acc" lab2_4_vlg_tst

add wave *
view structure
view signals
run -all
