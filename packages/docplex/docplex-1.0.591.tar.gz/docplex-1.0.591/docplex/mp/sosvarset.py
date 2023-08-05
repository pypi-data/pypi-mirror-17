# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------
from docplex.mp.basic import ModelingObjectBase


class SOSVariableSet(ModelingObjectBase):
    ''' This class models :index:`Special Ordered Sets` (SOS) of decision variables.
        An SOS has a type (SOS1, SOS2) and an ordered list of variables.

        This class is not meant to be instantiated directly.
        To create an SOS, use the :func:`docplex.mp.model.Model.add_sos`, :func:`docplex.mp.model.Model.add_sos1`,
        and :func:`docplex.mp.model.Model.add_sos2` methods in Model.
        
    '''

    def __init__(self, model, variable_sequence, sos_type, name=None):
        ModelingObjectBase.__init__(self, model, name)
        self._sos_type = sos_type
        self._variables = variable_sequence[:]  # copy sequence


    @property
    def sos_type(self):
        ''' This property returns the type of the SOS variable set.

        :returns: An enumerated value of type :class:`docplex.mp.constants.SOSType`.
        '''
        return self._sos_type

    def iter_variables(self):
        ''' Iterates over the variables in the SOS.

        Note that the sequence of variables cannot be empty.

        Returns:
            An iterator.
        '''
        return iter(self._variables)

    def __len__(self):
        ''' This special method makes it possible to call the `len()` function on an SOS,
        returning the number of variables in the SOS.

        Returns:
            The number of variables in the SOS.
        '''
        return len(self._variables)

    def __getitem__(self, item):
        ''' This special method enables the [] operator on special ordered sets,


        Args:
            item: an integer from 0 to the number of variables -1

        Returns:
            The variable in the set at location <item>
        '''
        return self._variables[item]

    def to_string(self):
        ''' Converts an SOS of variables to a string.

        This function is used by the `__str__()` method

        Returns:
            A string representation of the SOS of variables.
        '''
        vars_s = ', '.join(str(v) for v in self.iter_variables())
        name_s = '(\'%s\')' % self._name if self._name else ''
        return '{0!s}{2}[{1:s}]'.format(self._sos_type.name, vars_s, name_s)

    def get_ranks(self):
        # INTERNAL
        return list(range(1, len(self) + 1))

    def __str__(self):
        ''' Redefine the standard __str__ method of Python objects to customize string conversion.

        Returns:
            A string representation of the SOS of variables.
        '''
        return self.to_string()

    def __repr__(self):
        name_s = ', name=\'%s\'' % self._name if self._name else ''
        vars_s = ', '.join(str(v) for v in self.iter_variables())
        repr_s = 'docplex.mp.SOSVariableSet(type={0}{1}{2})'.format(self.sos_type.value, vars_s, name_s)
        return repr_s
