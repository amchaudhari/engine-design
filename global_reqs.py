_global_reqs = {
	'engine': {
		'N': 6500,   # Rotational speed of engine in rpm
		'T': 220,    # Torque in N-m
		'NC': 4,    # No. of cylinders
		# 'n_m':0.70, # Mechanical efficiency as ratio
		'P': 130e3,  # Power output in watts
		# 'f_p': 0.08, # Fluctuation percentage as ratio
		'LDr': 1.75,
		'm': 35,        # mass of the engine
		'fos': 2.0
	},

	'lawn_mower': {
		'N': 3000,   # Rotational speed of engine in rpm
		'T': 8,    # Torque in N-m
		'NC': 1,    # No. of cylinders
		# 'n_m': 0.70, # Mechanical efficiency as ratio
		'P': 4e03,  # Power output in watts
		# 'f_p': 0.08, # Fluctuation percentage as ratio
		'LDr': 1.2,
		'm': 3,        # mass of the engine
		'fos': 2.0
	}
}

_global_reqs_labels = {
		'N':'Min. rotational speed in rpm ',
		'T':'Min. torque in N-m',
		'NC':'Number of cylinders ',
		# 'n_m':'Min. mechanical efficiency as ratio',
		'P':'Min. power output in watts',
		# 'f_p':'Fluctuation percentage as ratio',
		'LDr': 'Stroke length to bore diameter ratio',
		'm':'Total mass of engine components in kg',
		'fos': 'System-level factor of safety'
}

	# _global_reqs_symbols = [ 'N', 'T', 'NC', 'n_m', 'P', 'f_p', 'm'	]

_initial_global_pars = {
	'engine': {
		'D': 0.105*1000, #bore diameter in mm
		'c': 0.3*1000, #bearings support offsets in mm
		't_f': 0.051*1000, #thickness of flywheel in mm
		'ds': 0.06*1000, #flywheel shaft diameter in mm
	},

	'lawn_mower': {
		'D': 0.070*1000, #bore diameter in mm
		'c': 0.13*1000, #bearings support offsets in mm
		't_f': 0.030*1000, #thickness of flywheel in mm
		'ds': 0.025*1000, #flywheel shaft diameter in mm
	}
}
_global_pars_labels = {
	'D': 'Piston bore diameter in mm',
	'c': 'Crankshaft bearing support offset in mm ',
	't_f': 'Thickness of flywheel in mm',
	'ds': 'Flywheel shaft diameter in mm'
}

#qualit scale for total mass of the syste,
_mass_scale = {
	'engine': {
		0: [50.001, 200],
		1: [45.001, 50],
		2: [40.001, 45],
		3: [35.001, 40.],
		4: [0.001, 35]
	},
	'lawn_mower': {
		0: [3.501, 200],
		1: [3.001, 3.5],
		2: [2.501, 3.0],
		3 : [2.001, 2.5],
		4: [0.001, 2.]
	}
}

_fos_scale = {
	0:[0.0, 1.499],
	1:[1.50, 1.749],
	2:[1.75, 1.999],
	4:[2.0, 200],
}

_format_scale = {
	0:'Poor',
	1:'Fair',
	2:'Good',
	3:'Very Good',
	4:'Excellent'
}

#Payoff per player, if the group satistfies fos requirement
_payoff_structure = {
	'Poor': 10,
	'Fair': 12,
	'Good': 15,
	'Very Good': 17,
	'Excellent': 20
}