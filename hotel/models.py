from django.db import models

# Create your models here.
    
class RoomTypes(models.Model):
    name = models.CharField(max_length=155)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    name = models.CharField(max_length=155)
    price = models.IntegerField()
    room_types = models.ManyToManyField(RoomTypes, related_name='rooms')

    def __str__(self):
        return self.name
       
class Promotion(models.Model):
    name = models.CharField(max_length=100)
    discount_percent = models.IntegerField()
    description = models.TextField()
    start_date = models.DateField()
    expire_date = models.DateField()

    def __str__(self):
        return self.name
    
class Bookings(models.Model):
    user = models.ForeignKey('auth.User', null=True, on_delete=models.PROTECT)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)  # เชื่อมกับตาราง Room
    start_date = models.DateField()
    end_date = models.DateField()
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)  # เชื่อมกับ Promotion (สามารถเป็นค่าว่างได้)
    total_price = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_status = models.BooleanField()