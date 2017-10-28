from django.conf.urls import url
from eventapp import views, statistics


urlpatterns = [
     url(r'user$', views.get_user, name='get_user'),
     url(r'exchange_token$', views.get_access_token, name='exchange_token'),
     url(r'login$', views.login_usr, name='login'),
     url(r'custom_plot$', views.custom_plot, name='geo_data'), #ok tested
     url(r'plot_by_place$', views.plot_by_place, name='plot_by_place'), #ok tested
     url(r'date_filter$', statistics.date_filter, name='date_filter'), #ok tested
     url(r'date_filter_by_locality$', statistics.date_filter_by_locality, name='date_filter_by_locality'), #ok tested
     url(r'date_filter_by_product$', statistics.date_filter_by_disease, name='date_filter_by_product'), #ok tested
     url(r'time_series_plot$', statistics.time_series_plot, name='time_series_plot'), #ok tested
     url(r'time_series_plot_by_locality$', statistics.time_series_plot_by_locality, name='time_series_plot_by_locality'), #ok tested
     url(r'quant_analysis$', statistics.quant_analysis, name='quantity_analysis'), #ok tested
     url(r'locality_analysis$', statistics.locality_analysis, name='locality_analysis'), #ok tested
     url(r'local_analysis$', statistics.locality__analysis_2, name='locality_analysis'), #ok tested


]
