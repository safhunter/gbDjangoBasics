class GetItemMixin:

    @classmethod
    def get_item(cls, **kwargs):
        return cls.objects.filter(**kwargs).first()

    @classmethod
    def get_items(cls, **kwargs):
        return cls.objects.filter(**kwargs)
