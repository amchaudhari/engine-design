from math import pi,sin,cos,sqrt
from global_reqs import *

class flywheel(object):

	_fixed_pars = {
		'Sy2': 275e6,  	# Yield stress of the piston head material in Pa(N/m^2)
		'rho1':8e3,		# density of flywheel material in kg/m^3
		'rho2':8e3,		# density of crank shaft material in kg/m^3
		# 'fp': 0.08,		# fluctuation percentage as ratio
		# 'P': 130e03		# Power output in Watts,
		'NC': 4,    # No. of cylinders
		'n_m':0.70, # Mechanical efficiency as ratio
		'f_p': 0.08, # Fluctuation percentage as ratio
	}

	# outside_inputs = {
	# 	'c': 0.075,	# crank shaft breaing 2,3 support offsets in meters: obtained from crank shaft design 
	# }

	# _initial_inputs = {
	# 	't_f': 0.051,
	# 	'ds': 0.060,
	# }

	# _initial_outside_inputs = {
	# 	'c': 0.300
	# }

	roles = ['piston', 'flywheel', 'crankshaft', 'conrod', 'pistonpin']

	def __init__(self, global_reqs, _fixed_pars=_fixed_pars):
		self.team_label = self.roles[1]
		self.input_labels = ['flywheel thickness in mm', 'flywheel shaft diameter in mm']
		self.input_symbols = ['t_f', 'ds']
		self.inputs_min = {
			'engine': [0.012*1000, 0.040*1000],
			'lawn_mower': [0.010*1000, 0.015*1000]
		}
		self.inputs_max =  {
			'engine': [0.051*1000, 0.060*1000],
			'lawn_mower': [0.030*1000, 0.025*1000]
		}

		self.outside_input_labels = ['crank-shaft bearing support offset in mm']
		self.outside_input_symbols = ['c']
		self.outside_inputs_min = {
			'engine':[0.150*1000],
			'lawn_mower': [0.060*1000]
		}
		self.outside_inputs_max =  {
			'engine': [0.300*1000],
			'lawn_mower': [0.130*1000]
		}

		self.input_catalog = { 
			'engine': [[12.0, 40.0],
					 [21.75, 40.0],
					 [31.5, 40.0],
					 [41.25, 40.0],
					 [51.0, 40.0],
					 [12.0, 45.0],
					 [21.75, 45.0],
					 [31.5, 45.0],
					 [41.25, 45.0],
					 [51.0, 45.0],
					 [12.0, 50.0],
					 [21.75, 50.0],
					 [31.5, 50.0],
					 [41.25, 50.0],
					 [51.0, 50.0],
					 [12.0, 55.0],
					 [21.75, 55.0],
					 [31.5, 55.0],
					 [41.25, 55.0],
					 [51.0, 55.0],
					 [12.0, 60.0],
					 [21.75, 60.0],
					 [31.5, 60.0],
					 [41.25, 60.0],
					 [51.0, 60.0]],
			'lawn_mower': [[10.0, 15.0],
					 [15.0, 15.0],
					 [20.0, 15.0],
					 [25.0, 15.0],
					 [30.0, 15.0],
					 [10.0, 17.5],
					 [15.0, 17.5],
					 [20.0, 17.5],
					 [25.0, 17.5],
					 [30.0, 17.5],
					 [10.0, 20.0],
					 [15.0, 20.0],
					 [20.0, 20.0],
					 [25.0, 20.0],
					 [30.0, 20.0],
					 [10.0, 22.5],
					 [15.0, 22.5],
					 [20.0, 22.5],
					 [25.0, 22.5],
					 [30.0, 22.5],
					 [10.0, 25.0],
					 [15.0, 25.0],
					 [20.0, 25.0],
					 [25.0, 25.0],
					 [30.0, 25.0]]
		}

		for key, value in {**global_reqs, **_fixed_pars}.items():
			setattr(self, key, value)

		"""
		Variables: 
		
		n_m          : mechanical efficiency as ratio 
		P            : Power output in Watts 
		T            : Torque in N-m
		N            : maximum angular velocity in cycle in rpm
		fp           : fluctuation percentage as ratio
		rho1         : density of flywheel material in kg/m^3
		rho2         : density of crank shaft material in kg/m^3
		t_fw         : thickness of flywheel in meters
		c1,c2        : crank shaft bearings 2,3 support offsets in meters : Obtained from crank shaft design
		Sy2          : yield strength of crank shaft material in Pa
		ds           : fly-wheel shaft diameter in meters
		
		"""
		   
		"""fly-wheel"""
		w_max = self.N*pi/30             # max angular velocity in rad/s
		w_mean = w_max/(1+self.f_p/2)     # mean angular velocity in rad/s
		Cs = self.f_p                     	# coefficient of fluctuation of speed
		W_cycle = (self.P/self.n_m)*60/self.N            # work done by fly-wheel per cycle in Joules
		C_E = 0.066                     # energy coefficient: 1.93 for 4-stroke 1 cylinder, 0.066 for 4 cylinder, 0.031 for 6 cylinder
		del_E = C_E*W_cycle                 # maximum fluctuation of energy in Joules

		self.w_mean=w_mean
		self.Cs=Cs
		self.del_E=del_E


	def factor_of_safety(self, x, outside_x):
		t_fw = x['t_f']/1000
		ds = x['ds']/1000

		c = outside_x['c']/1000

		c1 = c/2
		c2 = c/2

		"""fly-wheel"""
		m_flywheel = sqrt(self.del_E*pi*self.rho1*t_fw/(self.Cs*self.w_mean**2)) # mass of flywheel in kgs. 
		r_flywheel = sqrt((ds/2)**2+m_flywheel/(self.rho1*pi*t_fw))          # radius of flywheel in meters
		

		"""fly-wheel shaft"""
		W_fw = m_flywheel*9.81          # weight of flywheel in N
		V3 = W_fw*c2/(c1+c2)            # vertical reaction at bearings in N
		
		fos_fws = (pi*self.Sy2*ds**3)/(32*V3*c1)  # yield fos of flywheel shaft against bending

		# if r_flywheel<1.1*ds/2:
  #       	fos_fws=0

		# self.r_flywheel=r_flywheel
		return round(fos_fws,2)

	def mass(self, x, outside_x):
		t_fw = x['t_f']/1000
		ds = x['ds']/1000

		c = outside_x['c']/1000

		c1 = c/2
		c2 = c/2

		"""fly-wheel"""
		m_flywheel = sqrt(self.del_E*pi*self.rho1*t_fw/(self.Cs*self.w_mean**2)) # mass of flywheel in kgs. 
		r_flywheel = sqrt((ds/2)**2+m_flywheel/(self.rho1*pi*t_fw))           # radius of flywheel in meters

		m_fws = self.rho2*(pi/4)*(ds**2)*t_fw     # mass of flywheel shaft
		m_total = m_flywheel+m_fws           # total mass: mass of fly-wheel + mass of fly-wheel shaft in kgs.
		
		# self.r_flywheel=r_flywheel
		return round(m_total,2)