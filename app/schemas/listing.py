from ..extensions import ma
from ..models.listing import Listing

class ListingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Listing
        load_instance = True
        include_fk = True