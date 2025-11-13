from ..extensions import ma
from ..models.booking import Booking

class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking
        load_instance = True
        include_fk = True