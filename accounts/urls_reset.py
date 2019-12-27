from django.urls.conf import urls
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_complete, password_reset_confirm, password_reset_done

urlpatterns = [
    url(r'^reset$', {'post_reset_redirect' : reverse_lazy('password_reset_done')}, name='password_reset')
]