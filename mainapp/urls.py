from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from mainapp.view import login, home, add_manager, add_customer, add_purchase, call_notes, attachments, chat, task, \
    invoices, offer


app_name = 'mainapp'
urlpatterns = [
    path('', login.LoginView.as_view(), name='login'),
    path('logout', login.logout_view, name='logout'),

    # Home
    path('home/', home.HomeView.as_view(), name='home'),
    path('home/customer/<customer_id>/', home.CustomerHomeView.as_view(), name='customer_home'),

    path('manager/', add_manager.CreateManagerView.as_view(), name='add_manager'),
    path('manager/<int:pk>/', add_manager.UpdateManagerView.as_view(), name='edit_manager'),
    path('delete_manager/<manager_id>', add_manager.delete_manager, name='delete_manager'),

    path('customer/', add_customer.AddCustomerView.as_view(), name='add_customer'),
    path('customer/<int:pk>/', add_customer.UpdateCustomerView.as_view(), name='edit_customer'),
    path('delete/customer/<int:pk>/', add_customer.DeleteCustomerView.as_view(), name='delete_customer'),

    path('add_purchase/', add_purchase.AddPurchaseView.as_view(), name='add_purchase'),
    path('purchases/', add_purchase.ListPurchaseView.as_view(), name='list_purchase'),
    path('purchases/<int:pk>/', add_purchase.UpdatePurchaseView.as_view(), name='edit_purchase'),
    path('delete/purchases/<int:pk>/', add_purchase.DeletePurchaseView.as_view(), name='delete_purchase'),
    
    path('task_list/', task.TasksView.as_view(), name='open_task_list'),
    path('task/<int:pk>/', task.TaskUpdateView.as_view(), name='edit_task'),
    path('delete/task/<int:pk>/', task.DeleteTaskView.as_view(), name='delete_task'),
    path('mark_complete/<int:pk>/', task.mark_completed, name='mark_completed'),

    path('call_notes/<customer_id>/', call_notes.CallNotesCreateView.as_view(), name='add_call_notes'),
    path('call_notes/<customer_id>/<int:pk>/', call_notes.CallNotesUpdateView.as_view(), name='edit_call_notes'),
    path('delete/call_notes/<customer_id>/<int:pk>/', call_notes.CallNotesDeleteView.as_view(), name='delete_call_notes'),

    path('chat/', include(('chat.urls', 'chat'), 'chat')),

    path('<int:customer_id>/attachments/', attachments.AttachmentCreateView.as_view(), name='add_attachments'),

    # path('chat2/', chat.ChatView.as_view(), name='chat2'),
    # path('fetch_twilio_access_token/<identity>', chat.GetAccessToken.as_view(), name='fetch_twilio_access_token'),
    path('user_search/', chat.user_search, name='user_search'),
    # path('chat_messages/', chat.chat_messages, name='chat_messages'),
    # path('send_messages/', chat.send_messages, name='send_messages'),
    path('invoices/<customer_id>', invoices.InvoicesView.as_view(), name='invoices'),
    path('generate_invoices/<purchase_id>', invoices.download_invoice, name='generate_invoices'),
    path('offer/<customer_id>', offer.OfferView.as_view(), name='offer'),
    path('generate_offer/<purchase_id>', offer.download_offer, name='generate_offer'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
