from sympy import Symbol,N,S,sympify
from sympy.core import Mul,Pow
from sympy.functions import sign
from errorpro.dimensions.dimensions import Dimension
from errorpro.dimensions.simplifiers import dim_simplify
from errorpro.dimensions.solvers import subs_symbols
from sympy.parsing.sympy_parser import parse_expr

class Unit(Symbol):
	"""
	class for handling unit system internally.
	Output will also be given as expressions containing Unit-objects.
	Calculations must be done with Dimension objects!
	properties:
	 - dim: corresponding dimension
	 - factor: factor with respect to base unit system
	 - complexity: number summing up all exponents
	 - standard: bool if unit should appear in output
	"""
	def __new__(cls,name):
		self = Symbol.__new__(cls, name)
		self.abbrev=name
		self.name=name
		return self

class BaseUnit(Unit):
	"""
	all units forming the base unit system
	"""
	def __new__(cls,name,dim):
		self = Unit.__new__(cls, name)
		self.dim=dim
		self.factor=1
		self.complexity=1
		self.standard=True
		return self

class DerivedUnit(Unit):
	"""
	all units derived from other units
	"""
	def __new__(cls,name,dependency,unit_system,standard=True):

		self = Unit.__new__(cls, name)
		self.standard=standard
		if isinstance(dependency,str):
			self.dependency=parse_expr(dependency,local_dict=unit_system)
			for u in self.dependency.free_symbols:
				if not isinstance(u,Unit):
					raise ValueError("%s is not a unit." % u.name)
		else:
			self.dependency=dependency

		#calculate factor
		self.factor=self.dependency
		for var in self.dependency.free_symbols:
			exponent=self.factor.as_coeff_exponent(var)[1]
			self.factor*=var.factor**exponent
			self.factor/=var**exponent
		assert self.factor.is_number

		#calculate dimension
		dim=self.dependency
		for var in self.dependency.free_symbols:
			dim=subs_symbols(dim,{var.name:var.dim})
		self.dim=dim_simplify(dim)

		# calculate complexity
		# (sum over all absolute values of composing base units exponents)
		self.complexity=0
		for exponent in self.dim.values():
			self.complexity+=abs(exponent)

		return self


# default unit system is SI
from errorpro.si import system as DEF_UNIT_SYSTEM

def parse_unit(unit, unit_system=None):
	"""
	parses a unit string or unit expression and returns (factor,dimension,unit)
	where factor is the correction factor to get to the base unit system,
	dimension is the physical dimension as a Dimension object
	and unit is the unit as an Expression containing Unit objects

	Returns:
	tuple of factor, dimension and unit
	"""

	if unit_system is None:
		unit_system = DEF_UNIT_SYSTEM

	if isinstance(unit,str):
		if unit=="":
			unit=S.One
		else:
			unit=parse_expr(unit,local_dict=unit_system)
	for u in unit.free_symbols:
		if not isinstance(u,Unit):
			raise ValueError("%s is not a unit." % u.name)

	# calculate dimension
	dim=unit
	factor=unit
	for var in unit.free_symbols:
		exp=unit.as_coeff_exponent(var)[1]
		if exp==0:
			raise ValueError("%s is not a valid unit string." % unitStr)
		dim=subs_symbols(dim,{var.name:var.dim})
		factor=factor.subs(var,var.factor)

	return (factor,dim_simplify(dim),unit)


def convert_to_unit(input_dimension, output_unit=None, only_base=False, unit_system=None):
	"""
	function that converts dimension to unit

	Args:
	 - input_dimension: physical dimension as Dimension object
	 - output_unit: if specified, this function will only calculate the corresponding factor
	 - only_base: if True, will just use base units
	 - unit_system: dictionary of unit system to use

	Returns tuple of factor and unit.
	"""
	dim = input_dimension

	if unit_system is None:
		unit_system = DEF_UNIT_SYSTEM

	if output_unit == None:
		output_unit = S.One
		if dim.is_dimensionless:
			return (S.One,S.One)
		assert isinstance(dim, Dimension)
		factor = S.One

		sortedComplexities=sorted(set(map(lambda x:unit_system[x].complexity,unit_system)), reverse=True)
		fractions = False
		# try first integral exponents, then also fractions
		while True:
			# iterate all complexities
			for complexity in sortedComplexities:
				reciprocal = S.One
				# try first putting in normally, then putting in reciprocally
				while True:
					# iterates all units of this complexity
					for unit in unit_system.values():
						if (not only_base) or isinstance(unit,BaseUnit):
							if unit.standard and unit.complexity == complexity:
								# tries to put in as often as possible
								possible_exp = _fits_in(unit, dim, reciprocal, fractions)
								if not possible_exp is S.Zero:
									dim=dim_simplify(dim/(unit.dim**(possible_exp*reciprocal)))
									output_unit*=unit**(possible_exp*reciprocal)
									factor*=unit.factor**(possible_exp*reciprocal)
									if dim.is_dimensionless:
										return (factor,output_unit)

					if reciprocal==S.One:
						reciprocal=S.NegativeOne
					else:
						break
			if dim.is_dimensionless:
				break
			if fractions is False:
				fractions = True
			else:
				raise RuntimeError("Could not convert dimension %s to unit." % dim)
				break
	else:
		factor, unit_dim, unit=parse_unit(output_unit,unit_system)
		if not dim==unit_dim:
			raise RuntimeError("unit %s does not fit dimension %s."
								% (output_unit, dim))

	return (factor,output_unit)

def _fits_in(unit, dimension, reciprocal, fractions):
	"""
	Checks if unit "fits in" given dimension. This is true if there is some
	exponent for the unit to describe part of the dimension.
	(just for use inside this module)

	Args:
	 - unit
	 - dimension
	 - reciprocal: 1 or -1 to show if unit is supposed to be fitted in as
	   reciprocal or not
	 - fractions: bool if fractions are allowed

	Returns:
	  maximal possible exponent (positive)
	"""
	assert isinstance(unit,Unit)
	assert isinstance(dimension,Dimension)
	assert reciprocal is S.One or reciprocal is S.NegativeOne

	max_exp = None
	for lookAtThis, unitExp in unit.dim.items():
		dimExp=dimension.get(lookAtThis,0)
		if not unitExp==0:
			if not sign(unitExp)==sign(dimExp*reciprocal):
				return 0
			exponent = sympify(abs(dimExp))/sympify(abs(unitExp))
			if not fractions and not exponent.is_integer:
				return S.Zero
			if max_exp is None or exponent < max_exp:
				max_exp = exponent
	return max_exp
