from math import pi,sin,cos,sqrt
from global_reqs import *

class pistonpin(object):

	_fixed_pars = {
		'Sb': 140e6,  	# Yield stress of the piston head material in Pa(N/m^2)
		'rho_pp':8e3,		# density of crank shaft material in kg/m^3
		'NC': 4,    # No. of cylinders
		'n_m':0.70, # Mechanical efficiency as ratio
		'f_p': 0.08, # Fluctuation percentage as ratio
	}

	# outside_inputs = {
	# 	'D': 0.081		# bore diameter in meters
	# }

	# _initial_inputs = {
	# 	'r2': 0.900,
	# 	'r3': 0.800
	# }

	# _initial_outside_inputs = {
	# 	'D': 0.105
	# }

	roles = ['piston', 'flywheel', 'crankshaft', 'conrod', 'pistonpin']

	def __init__(self, global_reqs,  _fixed_pars=_fixed_pars):
		self.team_label = self.roles[4]
		self.input_labels = ['piston-pin length to piston diameter ratio, l1/D,', 'piston-pin inner diameter to pin outer diameter ratio, do/di,']
		self.input_symbols = ['r2', 'r3']
		self.inputs_min = {
			'engine': [0.700, 0.300],
			'lawn_mower': [0.500, 0.2]
		}
		self.inputs_max =  {
			'engine': [0.900, 0.800],
			'lawn_mower': [0.95, 0.8]
		}

		self.outside_input_labels = ['piston bore diameter in mm']
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
			'engine': [[0.7, 0.3],
				 [0.75, 0.3],
				 [0.8, 0.3],
				 [0.85, 0.3],
				 [0.9, 0.3],
				 [0.7, 0.42],
				 [0.75, 0.42],
				 [0.8, 0.42],
				 [0.85, 0.42],
				 [0.9, 0.42],
				 [0.7, 0.55],
				 [0.75, 0.55],
				 [0.8, 0.55],
				 [0.85, 0.55],
				 [0.9, 0.55],
				 [0.7, 0.68],
				 [0.75, 0.68],
				 [0.8, 0.68],
				 [0.85, 0.68],
				 [0.9, 0.68],
				 [0.7, 0.8],
				 [0.75, 0.8],
				 [0.8, 0.8],
				 [0.85, 0.8],
				 [0.9, 0.8]],
			'lawn_mower': [[0.5, 0.2],
				 [0.61, 0.2],
				 [0.72, 0.2],
				 [0.84, 0.2],
				 [0.95, 0.2],
				 [0.5, 0.35],
				 [0.61, 0.35],
				 [0.72, 0.35],
				 [0.84, 0.35],
				 [0.95, 0.35],
				 [0.5, 0.5],
				 [0.61, 0.5],
				 [0.72, 0.5],
				 [0.84, 0.5],
				 [0.95, 0.5],
				 [0.5, 0.65],
				 [0.61, 0.65],
				 [0.72, 0.65],
				 [0.84, 0.65],
				 [0.95, 0.65],
				 [0.5, 0.8],
				 [0.61, 0.8],
				 [0.72, 0.8],
				 [0.84, 0.8],
				 [0.95, 0.8]]
		}

		for key, value in {**global_reqs, **_fixed_pars}.items():
			setattr(self, key, value)

		"""
			Variables: 
			
			D            : Cylinder bore diameter in meters : obtained from piston team
			N            : rotational speed of engine in rpm
			T            : Torque in N-m
			Sb           : Allowable bending stress of pin material in Pa: 140Mpa for alloy steel, 84MPa for carbon steel
			rho_pp       : density of piston pin material in kg/m^3
		"""


	def get_Fl_pmax(self, D):
		N = self.N*(pi/30)                     # output rpm; rpm to rad/s
		L = self.LDr*D                         # stroke = [1.25D to 2D] in meters
		r = L/2                           # crank length in meters   
		Vd = (pi/4)*(D**2)*L              # displaced volume in m^3
		P_b = N*self.T                         # brake power in Watts
		mep = 2*P_b/(N*Vd)                # brake mean effective pressure in Pa
		p_max = 9.5*mep                   # max pressure = 9-10 times mep in Pa
		Fl = p_max*(pi/4)*D**2            # max. gas force on the piston (Fl=Fp=Fc) in N

		return Fl, p_max

	def factor_of_safety(self, x, outside_x):
		r2 = x['r2']
		r3 = x['r3']
		D = outside_x['D']/1000

		Fl, p_max = self.get_Fl_pmax(D)

		"""piston pin"""
		
		l1 = r2*D                        # length of piston pin taken as 0.45 times diameter in meters
		p_b1 = 10e6                        # bearing pressure of bronze bushing in Pa
		d0 =Fl/(p_b1*l1)                  # OD of piston pin in meters
		
		M_max = (pi/32)*p_max*D**3         # max bending moment in N-m
		di = r3*d0                        # inner diameter of piston pin in meters
		Z = (pi/32)*(d0**4-di**4)/d0       # section modulus in m^3
		fos_pp = self.Sb/(M_max/Z)              # fos against bending 
		return round(fos_pp,2)

	def mass(self, x, outside_x):
		r2 = x['r2']
		r3 = x['r3']
		D = outside_x['D']/1000

		Fl, p_max = self.get_Fl_pmax(D)

		"""piston pin"""
		l1 = r2*D                        # length of piston pin taken as 0.45 times diameter in meters
		p_b1 = 10e6                        # bearing pressure of bronze bushing in Pa
		d0 =Fl/(p_b1*l1)                  # OD of piston pin in meters
		di = r3*d0                        # inner diameter of piston pin in meters
		mass_pp = self.rho_pp*(pi/4)*l1*(d0**2-di**2)               # mass piston pin in kgs. 
		return round(self.NC*mass_pp,2)