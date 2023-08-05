
from .parse_qs import dict_from_qs
from .parse_qs import qs_from_dict


class ExpanderSerializerMixin(object):
    def __init__(self, *args, **kwargs):
        expanded_fields = kwargs.pop('expanded_fields', None)
        expandable_fields = getattr(self.Meta, 'expandable_fields', None)

        super(ExpanderSerializerMixin, self).__init__(*args, **kwargs)

        if not expandable_fields:
            return

        if not expanded_fields:
            context = self.context
            if not context:
                return

            request = context.get('request', None)
            if not request:
                return

            expanded_fields = request.query_params.get('expand', None)
            if not expanded_fields:
                return

        expansions = dict_from_qs(expanded_fields)
        for expanded_field, nested_expand in expansions.items():
            next_level_expanded_field = ''

            if expanded_field in expandable_fields:
                serializer_class_info = expandable_fields[expanded_field]

                # Two formats
                # 1. CLASS
                # 2. (CLASS, args, kwargs)
                if isinstance(serializer_class_info, tuple):
                    serializer_class, args, kwargs = serializer_class_info
                else:
                    args = ()
                    kwargs = {}
                    serializer_class = serializer_class_info

                kwargs = kwargs.copy()
                kwargs.setdefault('context', self.context)

                # If the serializer class isn't an expander then it can't
                # handle the expanded_fields kwarg.
                if issubclass(serializer_class, ExpanderSerializerMixin):
                    serializer = serializer_class(
                        *args, expanded_fields=qs_from_dict(nested_expand),
                        **kwargs)
                else:
                    serializer = serializer_class(*args, **kwargs)

                self.fields[expanded_field] = serializer
