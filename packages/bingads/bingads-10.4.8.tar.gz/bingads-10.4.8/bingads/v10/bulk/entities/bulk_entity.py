from abc import ABCMeta, abstractproperty

from future.utils import with_metaclass

from bingads.internal.error_messages import _ErrorMessages
from bingads.v10.internal.bulk.bulk_object import _BulkObject


class BulkEntity(with_metaclass(ABCMeta, _BulkObject)):
    """ The abstract base class for all bulk entities that can be read or written in a bulk file.

    For more information, see Bulk File Schema at http://go.microsoft.com/fwlink/?LinkID=620269.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    @abstractproperty
    def has_errors(self):
        """ Determines whether the bulk entity has associated errors.

        :rtype: bool
        """

        raise NotImplementedError()

    @abstractproperty
    def last_modified_time(self):
        """ Gets the last modified time for the entity.

        :rtype: :class:`datetime.datetime`
        """

        raise NotImplementedError()

    def _validate_property_not_null(self, property_value, property_name):
        if property_value is None:
            raise ValueError(_ErrorMessages.get_property_must_not_be_null_message(type(self).__name__, property_name))

    def _validate_list_not_null_or_empty(self, list_object, list_value, property_name):
        self._validate_property_not_null(list_object, property_name)
        if not list_value:
            raise ValueError(_ErrorMessages.get_list_must_not_be_null_or_empty(type(self).__name__, property_name))
