from django.conf import settings
from django.core import serializers
from mint import utils
import inspect


class Serializer(object):
    return_fields = ()

    can_update_fields = ()
    can_create_fields = ()

    required_update_fields = ()
    required_create_fields = ()

    transformers = {}

    default_transformers = {
        'DateTimeField': utils.string_from_datetime,
        'DateField': utils.string_from_datetime,
        'TimeField': utils.string_from_time,
        'DecimalField': float,
        'FileField': lambda value: "%s%s" % (settings.MEDIA_URL, value),
        'ManyToManyField': lambda value: []

    }

    def pack(self, model):
        fields = serializers.serialize('python', (model, ))[0]['fields']
        out = {}
        out_fields = self.return_fields
        for name, value in fields.items():
            if name in out_fields:
                if hasattr(self, name):
                    relationship = getattr(self, name)
                    out[name] = relationship.serialize(model)
                else:
                    my_type = model._meta.get_field(name).get_internal_type()
                    out[name] = self.transform_field(model, my_type, name, value)
                    if my_type in ['ForeignKey']:
                        key = "%s_id" % name
                        out[key] = value
                        del out[name]
        if 'id' in out_fields:
            out['id'] = model.id
        out['model'] = utils.camel_to_underscore(model.__class__.__name__)
        self.pre_return(model, out)
        return out

    def transform_field(self, model, type, name, value):
        transformers = dict(self.default_transformers, **self.transformers)
        if type in transformers:
            value = transformers[type](value)
        if hasattr(model, 'get_%s_display' % name):
            return getattr(model, 'get_%s_display' % name)()
        else:
            return value

    def pre_return(self, model, out):
        pass


class Relationship(object):
    def __init__(self, serializer_class, field_name):
        self.field_name = field_name
        self.serializer_class = serializer_class

    def get_serializer(self):
        return self.serializer_class()

    def serialize(self, model):
        raise NotImplementedError("Must be implemented in extending class.")


class ForeignKeyRelationship(Relationship):
    def serialize(self, model):
        field = getattr(model, self.field_name)
        if field is not None:
            return self.get_serializer().pack(field)
        return field


class ManyToManyFieldRelationship(Relationship):
    def serialize(self, model):
        out = []
        for model in getattr(model, self.field_name).all():
            out.append(self.get_serializer().pack(model))
        return out
