from mongoengine.errors import ValidationError


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    except ValidationError:
        return None
