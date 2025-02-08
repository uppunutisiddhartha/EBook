from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import lecturer_dashboard

from .views import authView,setting_view,lecturer_dashboard, index,profile, meet, logout_view,class_rejection_reason, accept_class, reject_class, details, Addbook, insert_book, approvebook, rejectbook, btech, book_detail, save_note, delete_note, searchbar, cart, add_to_cart, remove_from_cart, help, settings, feedback_view, fsuccess, update_note, group, send_invitation, chatAPI, application_success, lecturer_application, request_class ,withdraw,about_us,lecture_login, lec_profile,edit_lecturer_profile

urlpatterns = [
    path('', index, name='home'),
    path("", index, name="index"),
    path("meet/", meet, name="meet"),
    
    path("signup/", authView, name="authView"),
    path("details/", details, name="details"),
    path("logout/", logout_view, name="logout"),
    path("addbook/", Addbook, name="Addbook"),
    path("btech/", btech, name="btech"),
    path("insert_book/", insert_book, name="insert_book"),
  
    # Include Django's built-in authentication URLs
    path("accounts/", include("django.contrib.auth.urls")),
    
    path('approve/<uuid:token>/', approvebook, name='approve_book'),
    path('reject/<uuid:token>/', rejectbook, name='reject_book'),
    
    path('book/<int:pk>/', book_detail, name='book_detail'),
    
    path('save-note/<int:book_id>/', save_note, name='save-note'),
    path('delete-note/<int:book_id>/', delete_note, name='delete-note'),
    
    path('searchbar/', searchbar, name='searchbar'),
    
    path("cart/", cart, name="cart"),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),   
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    
    path('feedback/', feedback_view, name='feedback'),
    path('fsucess/', fsuccess, name="fsuccess"),
    
    path("help/", help, name="help.html"),
    path('chat-api', chatAPI, name='chat-api'),
    
    
    
    path('approval-status/', index, name='approval_status'),
    path('update-note/<int:book_id>/', update_note, name='update_note'),
    
    path('group/', group, name='group'),
    path('send-invitation/', send_invitation, name='send_invitation'),
    
    path('lecturer-application/', lecturer_application, name='lecturer_application'),
    path('application-success/', application_success, name='application_success'), 
    path("request_class/", request_class, name='request_class'),
    path("class_rejection_reason/",class_rejection_reason, name='class_rejectiontion_reason'),
    
    path('accept_class/<int:class_request_id>/',accept_class, name='accept_class'),
    path('reject_class/<int:class_request_id>/',reject_class, name='reject_class'),
      path('accept-class/<int:class_request_id>/', accept_class, name='accept_class'),
      path("profile/",profile,name="profile"),
      path('setting/',setting_view,name="setting"),
      path('withdraw/',withdraw,name="withdraw"),
      
      path("about_us/",about_us,name="about_us"),
      
      #lecturer urls 
      
    path('lecturer_login/', lecture_login, name='lecturer_login'),  # Ensure '/' is at the end of the URL
    path('lecturer_dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('lec_profile/', lec_profile, name='lec_profile'),
    path('edit_lecturer_profile/<id>',edit_lecturer_profile,name='edit_lecturer_profile')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
