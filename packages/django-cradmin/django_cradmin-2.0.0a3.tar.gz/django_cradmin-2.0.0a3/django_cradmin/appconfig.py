from django.apps import AppConfig
from django.utils.translation import ugettext_lazy
from django_cradmin import javascriptregistry


class CradminAppConfig(AppConfig):
    name = 'django_cradmin'
    verbose_name = ugettext_lazy("Django CRadmin")
    
    def ready(self):
        javascriptregistry.Registry.get_instance().add(javascriptregistry.component.CradminMenu)


class CradminWithStyleguideAppConfig(CradminAppConfig):

    def ready(self):
        from django_cradmin.apps.cradmin_kss_styleguide import styleguide_registry
        super(CradminWithStyleguideAppConfig, self).ready()

        styleguide = styleguide_registry.CradminStyleGuide(
            unique_id='django_cradmin_theme_default',
            label='Django CRadmin default theme',
            appname='django_cradmin',
            sourcefolder='styles/cradmin_theme_default',
            sourcefile='styleguide.scss'
        )
        styleguide_registry.Registry.get_instance().add(styleguide)

        # styleguide = styleguide_registry.CradminStyleGuide(
        #     unique_id='django_cradmin_theme_example',
        #     label='Django CRadmin example theme',
        #     appname='django_cradmin',
        #     sourcefolder='styles/cradmin_theme_example',
        #     sourcefile='styleguide.scss',
        # )
        # styleguide_registry.Registry.get_instance().add(styleguide)
