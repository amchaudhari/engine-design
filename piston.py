from math import pi,sin,cos,sqrt
from global_reqs import *

class piston(object):

	_fixed_pars = {
		'Sy':275e6,  #Yield stress of the piston head material in Pa(N/m^2)
		'rho_piston': 8e03, #Density of piston head material in kg/m^3
		'NC': 4,    # No. of cylinders
		'n_m':0.70, # Mechanical efficiency as ratio
		'f_p': 0.08, # Fluctuation percentage as ratio
	}

	# _initial_inputs = {
	# 	't_H':0.0105,
	# 	'D': 0.105
	# }

	# _initial_outside_inputs = dict()

	roles = ['piston', 'flywheel', 'crankshaft', 'conrod', 'pistonpin']

	def __init__(self, global_reqs, _fixed_pars=_fixed_pars):
		self.team_label = self.roles[0]
		self.input_labels = ['piston head thickness in mm', 'piston bore diameter in mm']
		self.input_symbols = ['t_H', 'D']
		self.inputs_min = {
			'engine': [0.004*1000, 0.075*1000],
			'lawn_mower': [0.002*1000, 0.040*1000]
		}
		self.inputs_max = {
			'engine': [0.0105*1000, 0.105*1000],
			'lawn_mower': [0.007*1000, 0.070*1000]
		}

		self.input_catalog = { 
			'engine': [[4.0, 75.0],
					 [5.62, 75.0],
					 [7.25, 75.0],
					 [8.88, 75.0],
					 [10.5, 75.0],
					 [4.0, 82.5],
					 [5.62, 82.5],
					 [7.25, 82.5],
					 [8.88, 82.5],
					 [10.5, 82.5],
					 [4.0, 90.0],
					 [5.62, 90.0],
					 [7.25, 90.0],
					 [8.88, 90.0],
					 [10.5, 90.0],
					 [4.0, 97.5],
					 [5.62, 97.5],
					 [7.25, 97.5],
					 [8.88, 97.5],
					 [10.5, 97.5],
					 [4.0, 105.0],
					 [5.62, 105.0],
					 [7.25, 105.0],
					 [8.88, 105.0],
					 [10.5, 105.0]],
			'lawn_mower': [[2.0, 40.0],
					 [3.25, 40.0],
					 [4.5, 40.0],
					 [5.75, 40.0],
					 [7.0, 40.0],
					 [2.0, 47.5],
					 [3.25, 47.5],
					 [4.5, 47.5],
					 [5.75, 47.5],
					 [7.0, 47.5],
					 [2.0, 55.0],
					 [3.25, 55.0],
					 [4.5, 55.0],
					 [5.75, 55.0],
					 [7.0, 55.0],
					 [2.0, 62.5],
					 [3.25, 62.5],
					 [4.5, 62.5],
					 [5.75, 62.5],
					 [7.0, 62.5],
					 [2.0, 70.0],
					 [3.25, 70.0],
					 [4.5, 70.0],
					 [5.75, 70.0],
					 [7.0, 70.0]]
		}

		self.outside_input_labels = {
		}
		self.outside_input_symbols = {
		}
		self.outside_inputs_min = {
			'engine':0,
			'lawn_mower':0
		}
		self.outside_inputs_max = {
			'engine':0,
			'lawn_mower':0
		}

		for key, value in {**global_reqs, **_fixed_pars}.items():
			setattr(self, key, value)

		"""
		Variables: 
		
		ED           : Engine displacement in liters
		NC           : No.of cylinders
		t_H          : Piston head thickness in meters
		N            : rotational speed of engine in rpm
		T            : Torque in N-m
		Sy           : Yield stress of the piston head material in Pa(N/m^2)
		rho_piston   : Density of piston head material in kg/m^3
		
		"""
		# ED = self.ED*0.001                     # Engine displacement in m^3
		# Vd = ED/self.NC                        # Displacement volume in m^3       

	def factor_of_safety(self, x, outside_x):
		t_H = x['t_H']/1000
		D = x['D']/1000

		N = self.N*(pi/30)                     # output rpm; rpm to rad/s
		LDr = self.LDr                               # Stroke-to-bore ratio. typically, stroke = [1.25D to 2D] in meters 
		
		Vd = pi*D**3*LDr/4
		# D = ceil(1000*((4*Vd/(pi*LDr))**(1/3)))/1000  # bore diameter in m.
		P_b = N*self.T                         # brake power in Watts
		mep = 2*P_b/(N*Vd)                # brake mean effective pressure in Pa
		
		"""piston subassembly"""
		
		p_max = 9.5*mep                          # max pressure = 9-10 times mep in Pa
		L_p = self.LDr*D                             # Piston length = 1-1.5 times D in meters

		fos_y = 16*(t_H**2)*self.Sy/(3*p_max*D**2)    # yield fos against bending
		return round(fos_y,2)

	def mass(self, x, outside_x):
		t_H = x['t_H']/1000
		D = x['D']/1000

		"""piston subassembly"""
		
		L_p = 1.25*D                             # Piston length = 1-1.5 times D in meters

		m_p = (pi/4)*self.rho_piston*((D**2)*L_p-((D-2*t_H)**2)*(L_p-t_H))  # mass of piston head in Kgs.
		return round(self.NC*m_p,2)