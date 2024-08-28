from config_site.models import Config, Config_seo


def config(request):
    config_data = {
        'config': Config.objects.first(),
        'config_seo': Config_seo.objects.first(),
    }
    return config_data
