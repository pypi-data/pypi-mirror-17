"""
Defines a Field object. Fields can be plotted on a Map, and store certain properties,
such as contour levels, contour colors,  contour labels, etc.
"""

# Built-ins
import numbers

# This package
from .exceptions import FieldError


class Field:
    """
    Field object
    """
    def __init__(self, data, geogrid, levels='auto', contour_colors='auto', contour_labels=False,
                 smoothing_factor=0, fill_colors='auto', fill_alpha='auto'):
        # ------------------------------------------------------------------------------------------
        # Attributes
        #
        # Positional args
        self.data = data
        self.geogrid = geogrid
        # Kwargs
        self.levels = levels
        self.contour_colors = contour_colors
        self.contour_labels = contour_labels
        self.smoothing_factor = smoothing_factor
        self.fill_colors = fill_colors
        self.fill_alpha = fill_alpha
        # ------------------------------------------------------------------------------------------
        # Validate some attributes
        #
        # Smoothing factor - must be a number
        if not isinstance(smoothing_factor, numbers.Number):
            raise FieldError('smoothing_factor must be a number')

    def can_be_plotted_subsequently(self):
        """
        Determines if this Field can be plotted subsequently

        A Field can be plotted subsequently, in a list of multiple fields, if it has certain
        properties:

        - fill_colors must be None
        - fill_alpha must be None

        ### Returns

        - *dict* containing the following keys:
            - result: *boolean* - True if the Field can be plotted subsequently, otherwise False
            - error: *string* or None - Error if the Field can't be plotted subsequently,
            otherwise None
        """
        if self.fill_colors not in ['auto', None]:
            return {'result': False, 'error': 'fill_colors must be \'auto\' or None'}
        elif self.fill_alpha not in ['auto', None]:
            return {'result': False, 'error': 'fill_alpha must be \'auto\' or None'}
        else:
            return {'result': True, 'error': None}
