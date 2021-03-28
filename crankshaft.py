from math import pi,sin,cos,sqrt
from global_reqs import *

class crankshaft(object):

	_fixed_pars = {
		'Sy2': 275e6,  	# Yield stress of the piston head material in Pa(N/m^2)
		'rho2':8e3,		# density of crank shaft material in kg/m^3
		'NC': 4,    # No. of cylinders
		'n_m':0.70, # Mechanical efficiency as ratio
		'f_p': 0.08, # Fluctuation percentage as ratio
	}

	# outside_inputs = {
	# 	'ds':10e-03, 	#fly-wheel shaft diameter in meters: obtained from fly-wheel team
	# 	't_fw':0.01,	#fly-wheel thickness in meters: obtained from fly-wheel team
	# 	'D': 0.081		# bore diameter in meters
	# }
	# _initial_inputs = {
	# 	'c':0.3,
	# 	'dc': 0.05
	# }

	# _initial_outside_inputs = {
	# 	'ds': 0.060,
	# 	't_f': 0.051,
	# 	'D': 0.105
	# }

	roles = ['piston', 'flywheel', 'crankshaft', 'conrod', 'pistonpin']

	def __init__(self, global_reqs, _fixed_pars=_fixed_pars):
		self.team_label = self.roles[2]
		self.input_labels = ['crankshaft bearing offset in mm', 'crankshaft-pin diameter in mm']
		self.input_symbols = ['c', 'dc']
		self.inputs_min = {
			'engine': [0.150*1000, 0.030*1000],
			'lawn_mower': [0.060*1000, 0.010*1000]
		}
		self.inputs_max = {
			'engine': [0.300*1000, 0.050*1000],
			'lawn_mower': [0.13*1000, 0.020*1000]
		}

		self.outside_input_labels = ['flywheel shaft diameter in mm', 'flywheel thickness in mm', 'piston bore diameter in mm']
		self.outside_input_symbols = ['ds', 't_f', 'D']
		self.outside_inputs_min = {
			'engine': [0.040*1000,0.004*1000,0.075*1000],
			'lawn_mower': [0.015*1000, 0.010*1000, 0.040*1000]
		}
		self.outside_inputs_max = {
			'engine': [0.060*1000, 0.051*1000, 0.105*1000],
			'lawn_mower': [0.025*1000, 0.030*1000, 0.070*1000]
		}

		self.input_catalog = { 
			'engine': [[150.0, 30.0],
					 [187.5, 30.0],
					 [225.0, 30.0],
					 [262.5, 30.0],
					 [300.0, 30.0],
					 [150.0, 35.0],
					 [187.5, 35.0],
					 [225.0, 35.0],
					 [262.5, 35.0],
					 [300.0, 35.0],
					 [150.0, 40.0],
					 [187.5, 40.0],
					 [225.0, 40.0],
					 [262.5, 40.0],
					 [300.0, 40.0],
					 [150.0, 45.0],
					 [187.5, 45.0],
					 [225.0, 45.0],
					 [262.5, 45.0],
					 [300.0, 45.0],
					 [150.0, 50.0],
					 [187.5, 50.0],
					 [225.0, 50.0],
					 [262.5, 50.0],
					 [300.0, 50.0]],
			'lawn_mower': [[60.0, 10.0],
					 [77.5, 10.0],
					 [95.0, 10.0],
					 [112.5, 10.0],
					 [130.0, 10.0],
					 [60.0, 12.5],
					 [77.5, 12.5],
					 [95.0, 12.5],
					 [112.5, 12.5],
					 [130.0, 12.5],
					 [60.0, 15.0],
					 [77.5, 15.0],
					 [95.0, 15.0],
					 [112.5, 15.0],
					 [130.0, 15.0],
					 [60.0, 17.5],
					 [77.5, 17.5],
					 [95.0, 17.5],
					 [112.5, 17.5],
					 [130.0, 17.5],
					 [60.0, 20.0],
					 [77.5, 20.0],
					 [95.0, 20.0],
					 [112.5, 20.0],
					 [130.0, 20.0]]
		}

		for key, value in {**global_reqs, **_fixed_pars}.items():
			setattr(self, key, value)

		"""
		Variables: 
		
		D            : Cylinder bore diameter in meters:  Obtained from piston team
		N            : rotational speed of engine in rpm
		T            : Torque in N-m
		b = b1+b2 in meters
		c = c1+c2 in meters
		b1,b2        : bearings 1,2 support offsets in meters
		c1,c2        : bearings 2,3 support offsets in meters
		Sy2          : yield strength of crank shaft material in Pa
		rho2         : density of crankshaft material in kg/m^3
		dc           : crank-pin diameter in meters
		ds           : fly-wheel shaft diameter in meters: obtained from fly-wheel team
		t_fw         : fly-wheel thickness in meters: obtained from fly-wheel team
		
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
		
	def factor_of_safety(self, x, outside_x):
		c = x['c']/1000
		dc = x['dc']/1000

		ds = outside_x['ds']/1000
		t_fw = outside_x['t_f']/1000
		D = outside_x['D']/1000

		Fl, r = self.get_Fl_r(D)

		"""crankshaft"""
		# assuming bearing locations are equidistant
		b1 = b2 = c/2
		c1 = c2 = c/2
		
		H1 = Fl*b1/(b1+b2)              # horizontal reactions at bearings in N
		H2 = Fl*b2/(b1+b2)
		# net bearing reactions in N
		R1 = H1
		#R2 = sqrt(H2**2+V2**2)
		#R3 = V3
		
		# crank-pin 
		fos_cp = pi*self.Sy2*dc**3/(32*H1*b2) # bending fos of crank-pin
		Pb = 24.5*10**6                    # permissible bearing pressure in Pa. range = [10.5 24.5]
		lc = Fl/(dc*Pb)                  # length of crank-pin in meters
		
		
		# crank-web
		t_cw = (0.65*(dc*1000)+6.35)/1000             # crank-web thickness in meters
		w_cw = (1.125*(dc*1000)+12.7)/1000            # crank-web width in meters
		M_cw = H1*(b2-lc/2-t_cw/2)                    # max. bending moment on crank-web in N-m
		Z_cw = (w_cw*t_cw**2)/6                       # section-modulus of crank-web in m^3
		s_be = M_cw/Z_cw                              # bending stress in crank-web in Pa.
		s_c = H1/(w_cw*t_cw)                          # compressive stress in crank-web in Pa.
		s_total = s_be+s_c                            # total stress in crank-web in Pa.
		fos_cw = self.Sy2/s_total                          # fos againt yield for crank-web
		
		return round(min(fos_cp, fos_cw),2)

	def mass(self, x, outside_x):
		c = x['c']/1000
		dc = x['dc']/1000
		
		ds = outside_x['ds']/1000
		t_fw = outside_x['t_f']/1000
		D = outside_x['D']/1000

		Fl, r = self.get_Fl_r(D)

		# assuming bearing locations are equidistant
		b1 = b2 = c/2
		c1 = c2 = c/2

		# crank-pin
		Pb = 17*10**6                    # permissible bearing pressure in Pa. range = [10.5 24.5]
		lc = Fl/(dc*Pb)                  # length of crank-pin in meters
		mass_cp  = self.rho2*(pi/4)*lc*dc**2  # mass of crank pin in kgs. 

		# crank-web
		t_cw = (0.65*(dc*1000)+6.35)/1000             # crank-web thickness in meters
		w_cw = (1.125*(dc*1000)+12.7)/1000            # crank-web width in meters
		mass_cw = t_cw*w_cw*r*2*self.rho2                  # mass of crank webs, assuming each crank web is a cuboid with dimensions w_cw,t_cw and r in kgs.
		mass_cs = (pi/4)*self.rho2*(ds**2)*(b1+b2+c1+c2-lc-2*t_cw-t_fw)     # mass of crank shaft in kgs, assuming crank shaft has diameter of flywheel shaft diameter            
		m_total = mass_cp+mass_cw+mass_cs
		
		return round(self.NC*m_total,2)