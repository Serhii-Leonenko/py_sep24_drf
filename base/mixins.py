class BaseViewMethodsMixin:
    def get_serializer_class(self):
        if (
                hasattr(self, "action_serializer_classes")
                and self.action_serializer_classes.get(self.action)
        ):
            return self.action_serializer_classes.get(self.action)

        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute,"
                "or an `action_serializer_classes` attribute,"
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

        return self.serializer_class

    def get_permissions(self):
        if (
                hasattr(self, "action_permission_classes")
                and self.action_permission_classes.get(self.action)
        ):
            return [permission() for permission in self.action_permission_classes.get(self.action)]

        return super().get_permissions()
