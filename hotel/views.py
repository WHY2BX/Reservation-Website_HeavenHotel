from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.http import JsonResponse, HttpRequest

from django.views import View
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin 

from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import *

from django.contrib import messages

# Create your views here.

# no need login (annonymous user)
def homepage(request):
    return render(request, "homepage.html")

# no need login (annonymous user)
def mainpage(request):
    room = Rooms.objects.all().order_by("id")
    promotion = Promotion.objects.all()

    context = {
        "room" : room,
        "promotion": promotion
    }

    if request.method == 'POST':
        # เอาค่าจากฟอร์ม
        searched = request.POST['searched']

        # Query ให้หาได้จากทั้งชื่อ และประเภทห้อง iconstain = ไม่สนตัวเล็กใหญ่ distinct = ไม่ให้มันแสดงห้องซ้ำ
        searched_rooms = Rooms.objects.filter(
            Q(name__icontains=searched) | Q(room_types__name__icontains=searched)
        ).distinct().order_by("id")
       
        # ถ้าไม่เจอห้อง
        if not searched_rooms:
            messages.success(request, "Room does not exist...")
        else:
            # เพิ่มข้อมูลผลลัพธ์การค้นหาเข้าไปใน context ให้มันแสดงห้องที่ค้นหา
            context['searched'] = searched_rooms

    # ส่ง context ที่มีข้อมูลห้องทั้งหมด และผลการค้นหาถ้ามี ไปที่ mainpage.html
    return render(request, "mainpage.html", context)


@login_required(login_url="/auth/login/")
@permission_required("hotel.change_rooms")
def manageRoom(request):
    # เรียงตัวอักษร น้อย->มาก
    room = Rooms.objects.all().order_by("name")
    context = {
        "room" : room
    }

    return render(request, "manageroom.html", context)

@login_required(login_url="/auth/login/")
@permission_required("hotel.change_promotion")
def managePromotion(request):
    promotion = Promotion.objects.all()
    context = {
        "promotion" : promotion
    }

    return render(request, "managepro.html", context)

@login_required(login_url="/auth/login/")
@permission_required("hotel.add_rooms")
def createRoom(request):
    if request.method == "POST":
        form = createRoomForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            new_room = Rooms.objects.create(
                name = form.cleaned_data['name'],
                price = form.cleaned_data['price'],
            )
            # room_type เป็น many-to-many เพิ่มไปพร้อมกันเลยไม่ได้ ต้องเอามาเพิ่มแยก
            new_room.room_types.set(form.cleaned_data['types'])
        
            return redirect("manageRoom")
        
    else:
        form = createRoomForm()

    return render(request, "createroom.html", {"form": form})

@login_required(login_url="/auth/login/")
@permission_required("hotel.add_promotion")
def createPromotion(request):
    if request.method == "POST":
        form = createPromotionForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            new_promotion = Promotion.objects.create(
                name = form.cleaned_data['name'],
                discount_percent = form.cleaned_data['discount_percent'],
                description = form.cleaned_data['description'],
                start_date = form.cleaned_data['start_date'],
                expire_date = form.cleaned_data['expire_date'],
            )
        
            return redirect("managePromotion")
        
    else:
        form = createPromotionForm()

    return render(request, "createpro.html", {"form": form})

@login_required(login_url="/auth/login/")
@permission_required("hotel.delete_rooms")
def deleteRoom(request, room_id):
    delete_room = Rooms.objects.get(pk=room_id)
    print(delete_room)
    delete_room.delete()
    return JsonResponse({'deleteRoom':'delete'}, status=200)

@login_required(login_url="/auth/login/")
@permission_required("hotel.delete_promoiton")
def deletePromotion(request, promotion_id):
    delete_promotion = Promotion.objects.get(pk=promotion_id)
    print(promotion_id)
    delete_promotion.delete()
    return JsonResponse({'deletePromotion':'delete'}, status=200)


#--------------------------------------------------------------------------------------
#2B's zone

# ดูประวัติการจอง
class BookingListView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.view_bookings"]

    def get(self, request):

        user = request.user

        if user.is_staff:
            # เรียงตามอักษร น้อย->มาก
            book = Bookings.objects.all().order_by("user")
        else:
            book = Bookings.objects.filter(user=request.user).order_by("room__name")

        context = {
            "book" : book
        }

        return render(request, "booking-list.html", context)
    
class DeleteBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.delete_bookings"]

    def delete(self, request, booking_id):
        delete_booking = Bookings.objects.get(pk=booking_id)
        print(booking_id)
        delete_booking.delete()
        return JsonResponse({'deleteBooking':'delete'}, status=200)

# จองห้อง
class BookingView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.view_bookings"] 

    def get(self, request, room_id):
        form = NewBookingForm()
        room = Rooms.objects.get(pk=room_id)
        context = {
            "NewBookingForm": form,
            'room' : room
            }
        return render(request, "booking_form.html", context)

    def post(self, request, room_id):
        form = NewBookingForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            
            final_price = Rooms.objects.get(pk=room_id).price
            if form.cleaned_data['promotion'] != None:
                getPromotion = form.cleaned_data['promotion']
                final_price = final_price * ((100-(Promotion.objects.get(name=getPromotion).discount_percent))/100)
            else:
                getPromotion = None

            Bookings.objects.create(
                user = request.user,
                room = Rooms.objects.get(pk=room_id),
                start_date = form.cleaned_data['start_date'],
                end_date = form.cleaned_data['end_date'],
                promotion = getPromotion,
                total_price = final_price,
                payment_status = False
                )
            return redirect('bookingList')
        else:
        # ถ้าฟอร์มไม่ถูกต้องให้ส่งข้อมูลกลับไปยังเทมเพลต
            room = Rooms.objects.get(pk=room_id)
            context = {
                "NewBookingForm": form,  # ส่งฟอร์มที่มีข้อผิดพลาดกลับไป
                'room': room
            }
            return render(request, "booking_form.html", context)
        
    

class EditBookingView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.change_bookings"]

    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        form = EditBookingForm(instance=booking)
        context = {
            "booking": booking,
            "form": form  
        }
        return render(request, "edit_booking.html", context)
    
    def post(self, request: HttpRequest, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        
        form = EditBookingForm(request.POST, instance=booking) 
        
        if form.is_valid():
            form.save()  
            return redirect('bookingList')
        else:
            context = {
            "booking": booking,
            "form": form  
        }
        return render(request, "edit_booking.html", context)


class EditRoomView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.change_rooms"]

    def get(self, request, room_id):
        room = get_object_or_404(Rooms, pk=room_id)
        form = EditRoomForm(instance=room)
        context = {
            "room": room,
            "form": form  
        }
        return render(request, "edit_room.html", context)
    
    def post(self, request: HttpRequest, room_id):
        room = get_object_or_404(Rooms, pk=room_id)
        
        form = EditRoomForm(request.POST, instance=room)
        
        if form.is_valid():
            form.save()  
            return redirect('manageRoom')
        else:
            context = {
            "room": room,
            "form": form  
        }
        return render(request, "edit_room.html", context)


class EditPromotionView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.change_promotion"]

    def get(self, request, promotion_id):
        promotion = get_object_or_404(Promotion, pk=promotion_id)
        form = EditPromotionForm(instance=promotion)
        context = {
            "promotion": promotion,
            "form": form    
        }
        return render(request, "edit_promotions.html", context)
    
    def post(self, request: HttpRequest, promotion_id):
        promotion = get_object_or_404(Promotion, pk=promotion_id)
        
        form = EditPromotionForm(request.POST, instance=promotion)
        
        if form.is_valid():
            form.save()  
            return redirect('managePromotion')
        else:
            context = {
            "promotion": promotion,
            "form": form  
        }
        return render(request, "edit_promotions.html", context)


class PaymentView(LoginRequiredMixin, PermissionRequiredMixin, View):

    login_url = '/authen/'
    permission_required = ["hotel.add_bookings"]

    def get(self, request, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        context = {
            "booking": booking,   
        }
        return render(request, "payment.html", context)
    
    def post(self, request: HttpRequest, booking_id):
        booking = get_object_or_404(Bookings, pk=booking_id)
        
        booking.payment_status = True
        booking.save()

        return redirect("bookingList")


class ProfileView(LoginRequiredMixin, View):

    login_url = '/authen/'

    def get(self, request):
        return render(request, "profile.html")