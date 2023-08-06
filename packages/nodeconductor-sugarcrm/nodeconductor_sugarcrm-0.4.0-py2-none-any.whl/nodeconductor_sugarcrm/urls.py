from . import views


def register_in(router):
    router.register(r'sugarcrm', views.SugarCRMServiceViewSet, base_name='sugarcrm')
    router.register(r'sugarcrm-crms', views.CRMViewSet, base_name='sugarcrm-crms')
    router.register(r'sugarcrm-service-project-link', views.SugarCRMServiceProjectLinkViewSet, base_name='sugarcrm-spl')
    router.register(r'sugarcrm-crms/(?P<crm_uuid>[\w]+)/users', views.CRMUserViewSet, base_name='sugarcrm-users')
