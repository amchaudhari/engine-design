from math import pi,sin,cos,sqrt
from global_reqs import *

class conrod(object):

	_fixed_pars = {
		'Syc': 250e6,  	# Yield stress of the piston head material in Pa(N/m^2)
		'rho_cr':8e3,		# density of crank shaft material in kg/m^3
		'NC': 4,    # No. of cylinders
		'n_m':0.70, # Mechanical efficiency as ratio
		'f_p': 0.08, # Fluctuation percentage as ratio
	}

	# outside_inputs = {
	# 	'D': 0.081		# bore diameter in meters
	# }
	
	# _initial_inputs = {
	# 	't_I':0.015,
	# 	'r1': 5
	# }

	# _initial_outside_inputs = {
	# 	'D': 0.105
	# }

	roles = ['piston', 'flywheel', 'crankshaft', 'conrod', 'pistonpin']

	def __init__(self, global_reqs, _fixed_pars=_fixed_pars):
		self.team_label = self.roles[3]
		self.input_labels = ['thickness of connecting rod I-section in mm', 'ratio of length of connecting rod and crank length, l/r,']
		self.input_symbols = ['t_I', 'r1']
		self.inputs_min = {
			'engine': [0.005*1000, 4.000],
			'lawn_mower': [0.002*1000, 3.000]
		}
		self.inputs_max =  {
			'engine': [0.015*1000, 5.000],
			'lawn_mower': [0.008*1000, 6.000]
		}

		self.outside_input_labels = ['piston bore diameter in meters']
		self.outside_input_symbols = ['D']
		self.outside_inputs_min = {
			'engine':[0.075*1000],
			'lawn_mower': [0.040*1000]
		}
		self.outside_inputs_max =  {
			'engine': [0.105*1000],
			'lawn_mower': [0.070*1000]
		}

		self.input_catalog = { 
			'engine': [[5.0, 4.0],
					 [7.5, 4.0],
					 [10.0, 4.0],
					 [12.5, 4.0],
					 [15.0, 4.0],
					 [5.0, 4.25],
					 [7.5, 4.25],
					 [10.0, 4.25],
					 [12.5, 4.25],
					 [15.0, 4.25],
					 [5.0, 4.5],
					 [7.5, 4.5],
					 [10.0, 4.5],
					 [12.5, 4.5],
					 [15.0, 4.5],
					 [5.0, 4.75],
					 [7.5, 4.75],
					 [10.0, 4.75],
					 [12.5, 4.75],
					 [15.0, 4.75],
					 [5.0, 5.0],
					 [7.5, 5.0],
					 [10.0, 5.0],
					 [12.5, 5.0],
					 [15.0, 5.0]],
			'lawn_mower': [[2.0, 3.0],
					 [3.5, 3.0],
					 [5.0, 3.0],
					 [6.5, 3.0],
					 [8.0, 3.0],
					 [2.0, 3.75],
					 [3.5, 3.75],
					 [5.0, 3.75],
					 [6.5, 3.75],
					 [8.0, 3.75],
					 [2.0, 4.5],
					 [3.5, 4.5],
					 [5.0, 4.5],
					 [6.5, 4.5],
					 [8.0, 4.5],
					 [2.0, 5.25],
					 [3.5, 5.25],
					 [5.0, 5.25],
					 [6.5, 5.25],
					 [8.0, 5.25],
					 [2.0, 6.0],
					 [3.5, 6.0],
					 [5.0, 6.0],
					 [6.5, 6.0],
					 [8.0, 6.0]]
		}

		for key, value in {**global_reqs, **_fixed_pars}.items():
			setattr(self, key, value)

		"""
		Variables: 
		
		D            : Cylinder bore diameter in meters : obtained from piston team
		N            : rotational speed of engine in rpm
		T            : Torque in N-m
		tI           : thickness of I-section in meters
		Syc          : compressive yield strength of the connecting rod in Pa
		rho_cr       : density of connecting rod in kg/m^3
		
		"""
	def get_Fl_r(self, D):
		N = self.N*(pi/30)                     # output rpm; rpm to rad/s
		L = self.LDr*D                         # stroke = [1.25D to 2D] in meters
		r = L/2                           # crank length in meters   
		Vd = (pi/4)*(D**2)*L              # displaced volume in m^3
		P_b = N*self.T                         # brake power in Watts
		mep = 2*P_b/(N*Vd)                # brake mean effective pressure in Pa
		p_max = 9.5*mep                   # max pressure = 9-10 times mep in Pa
		Fl = p_max*(pi/4)*D**2            # max. gas force on the piston (Fl=Fp=Fc) in N

		return Fl, r

	def mass(self, x, outside_x):
		t_I = x['t_I']/1000
		r1 = x['r1']

		D = outside_x['D']/1000

		Fl, r = self.get_Fl_r(D)

		"""connecting rod"""
		
		l = r1*r                          # length of connecting rod = 4-5 times crank length in meters
		
		a = 1/1600                         # material specific: 1/7500 for mild steel, 1/9000 for wrought iron, 1/1600 for cast iron 
		
		BI = 4*t_I                          # width of I-section in meters
		HI = 5*t_I                          # height of I-section in meters
		kxx = 1.78*t_I                       # radius of gyration about x-axis in meters
		A = 11*t_I**2                        # cross-sectional area in m^2
		mass_cr = self.rho_cr*l*A               # mass of connecting rod in kgs.
		return round(self.NC*mass_cr,2)

	def factor_of_safety(self, x, outside_x):
		t_I = x['t_I']/1000
		r1 = x['r1']

		D = outside_x['D']/1000
		Fl, r = self.get_Fl_r(D)
		"""connecting rod"""
		
		l = r1*r                          # length of connecting rod = 4-5 times crank length in meters
		
		a = 1/1600                         # material specific: 1/7500 for mild steel, 1/9000 for wrought iron, 1/1600 for cast iron 
		
		BI = 4*t_I                          # width of I-section in meters
		HI = 5*t_I                          # height of I-section in meters
		kxx = 1.78*t_I                       # radius of gyration about x-axis in meters
		A = 11*t_I**2                        # cross-sectional area in m^2
		fos_cr = self.Syc*A/(Fl*(1+a*(l/kxx)**2)) # fos against buckling
		return round(fos_cr,2)