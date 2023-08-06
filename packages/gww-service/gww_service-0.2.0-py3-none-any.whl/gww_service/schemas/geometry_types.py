from geojson_pydantic import Feature

class PatchedFeature(Feature):

    @classmethod
    def validate(cls, value):
        if cls.__config__.orm_mode and type(value) != dict:
            return cls.from_orm(value)
        else:
            return super().validate(value)
