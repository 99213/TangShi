from django.urls import path
from . import views


app_name = 'trytest'

urlpatterns = [
    path(r'talk_index/', views.talkRoom.index, name='index'),

    path('', views.views.index, name='index'),
    path(r'sign/', views.views.sign, name='sign'),
    path(r'register/', views.views.register, name='register'),
    path(r'get_tangshi_name/', views.views.get_tangshi_name, name='get_tangshi_name'),
    path(r'add_love_dish/', views.views.add_love_dish, name='add_love_dish'),
    path(r'add_user_image/', views.views.add_user_image, name='add_user_image'),

    path(r'order/', views.order.order, name='order'),
    path(r'pay/', views.order.pay, name='pay'),
    path(r'get_all_dish/', views.order.get_all_dish, name='get_all_dish'),
    path(r'name_search_dish/', views.order.name_search_dish, name='name_search_dish'),
    path(r'id_search_dish/', views.order.id_search_dish, name='id_search_dish'),
    path(r'get_order_status/', views.order.get_order_status, name='get_order_status'),
    path(r'canteen_get_money/', views.order.canteen_get_money, name='canteen_get_money'),
    path(r'trade_comment/', views.order.trade_comment, name='trade_comment'),
    path(r'undo_order/', views.order.undo_order, name='undo_order'),
    path(r'get_category/', views.order.get_category, name='get_category'),

    path(r'new_proposal/', views.proposal.new_proposal, name='new_proposal'),
    path(r'delete_proposal/', views.proposal.delete_proposal, name='delete_proposal'),
    path(r'likes_change/', views.proposal.likes_change, name='likes_change'),

    path(r'worker_index/', views.canteen.worker_index, name='worker_index'),
    path(r'worker_sign/', views.canteen.worker_sign, name='worker_sign'),
    path(r'worker_register/', views.canteen.worker_register, name='worker_register'),
    path(r'worker_home/', views.canteen.worker_home, name='worker_home'),
    path(r'dish_page/', views.canteen.dish_page, name='dish_page'),
    path(r'dish_modify/', views.canteen.dish_modify, name='dish_modify'),
    path(r'new_dish/', views.canteen.new_dish, name='new_dish'),
    path(r'delete_dish/', views.canteen.delete_dish, name='delete_dish'),
    path(r'comment_reply/', views.canteen.comment_reply, name='comment_reply'),
    path(r'get_comment/', views.canteen.get_comment, name='get_comment'),
]
