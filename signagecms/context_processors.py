from signagecms import constants

def global_settings(request):
    # return any necessary values
    return {
        'DROP_BOX_ACCESS_TOKEN': constants.DROP_BOX_ACCESS_TOKEN,
        'API_HOST': constants.API_HOST
    }