from signagecms import constants

def global_settings(request):
    # return any necessary values
    return {
        'DROP_BOX_ACCESS_TOKEN': constants.DROP_BOX_ACCESS_TOKEN,
        'API_HOST': constants.API_HOST,
        'SINGLE_100_100':constants.SINGLE_100_100,
        'one_reg_vertical_json':constants.one_reg_vertical_json,
        'two_reg_vertical_json':constants.two_reg_vertical_json,
        'two_reg_hoirz_json':constants.two_reg_hoirz_json,
        'two_horiz_one_below_json':constants.two_horiz_one_below_json,
        'two_reg_vertical_50_50_json':constants.two_reg_vertical_50_50_json,
        'two_vertical_20_70_json':constants.two_vertical_20_70_json,
        'r3_1h_2v_20_50_50_json':constants.r3_1h_2v_20_50_50_json,
        'r4_2h_2v_50_50_json':constants.r4_2h_2v_50_50_json,
        'store_location':constants.STORE_LOCATION,
        'allowed_image_formats':constants.allowed_image_formats,
        'allowed_video_formats':constants.allowed_video_formats,
        'content_pagination_limit':constants.content_pagination_limit,

    }