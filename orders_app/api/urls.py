from django.urls import path
from .views import OrderListCreateView, OrderDetailView, OrderCountView, OrderCompletedCountView

urlpatterns = [
    # URL für die Listung und Erstellung von Bestellungen
    # Route: /orders/ (GET für eine Liste, POST für eine neue Bestellung)
    path('orders/', OrderListCreateView.as_view()),

    # URL für das Abrufen, Aktualisieren oder Löschen einer Bestellung
    # Route: /orders/<int:pk>/ (GET, PATCH, DELETE für eine Bestellung mit der entsprechenden ID)
    path('orders/<int:pk>/', OrderDetailView.as_view()),

    # URL für das Zählen der Bestellungen eines bestimmten Business-Users
    # Route: /order-count/<int:business_user_id>/ (GET um die Anzahl der Bestellungen für einen Business-User zu erhalten)
    path('order-count/<int:business_user_id>/', OrderCountView.as_view()),

    # URL für das Zählen der abgeschlossenen Bestellungen eines bestimmten Business-Users
    # Route: /completed-order-count/<int:business_user_id>/ (GET um die Anzahl der abgeschlossenen Bestellungen zu erhalten)
    path('completed-order-count/<int:business_user_id>/', OrderCompletedCountView.as_view()),
]
