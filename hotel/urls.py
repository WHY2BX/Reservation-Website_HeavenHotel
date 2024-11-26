from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("mainpage/", views.mainpage, name="mainpage"),
    # Search
    path("search/", views.mainpage, name="search"),

    path("manageroom/", views.manageRoom, name="manageRoom"),
    path("manageroom/deleteroom/<int:room_id>/", views.deleteRoom, name="deleteRoom"),
    
    path("managepro/", views.managePromotion, name="managePromotion"),
    path("managepro/deletepro/<int:promotion_id>/", views.deletePromotion, name="deletePromotion"),

    # Create
    path("createroom/", views.createRoom, name="createRoom"),
    path("createpromotion/", views.createPromotion, name="createPromotion"),

    #---------------------------------------------------------------------------------------------------
    #2B's 

    path("booking/<int:room_id>/", views.BookingView.as_view(), name="booking"),
    path("edit-booking/<int:booking_id>/", views.EditBookingView.as_view(), name="editBooking"),
    path("edit-room/<int:room_id>/", views.EditRoomView.as_view(), name="editRoom"),
    path("edit-promotion/<int:promotion_id>/", views.EditPromotionView.as_view(), name="editPromotion"),

    path("<int:user_id>/booking-list/", views.BookingListView.as_view(), name="mybookingList"),
    
    path("booking-list/", views.BookingListView.as_view(), name="bookingList"),
    path("booking-list/deleteBooking/<int:booking_id>/", views.DeleteBookingView.as_view(), name="Deletebooking"),

    path("payment/<int:booking_id>/", views.PaymentView.as_view(), name="payment"),

    path("profile/", views.ProfileView.as_view(), name="profile"),
    


]