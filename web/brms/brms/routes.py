def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('reset_pwd', '/reset_pwd')
    config.add_route('my_meeting', '/my_meeting')
    config.include(app_include, '/app')
    config.include(user_include, '/user')
    config.include(org_include, '/org')
    config.include(role_include, '/role')
    config.include(auth_include, '/auth')
    config.include(boardroom_include, '/boardroom')
    config.include(terminal_include, '/terminal')
    config.include(meeting_include, '/meeting')
    config.include(booking_include, '/booking')


def app_include(config):
    config.add_route('padLogin', '/padLogin')
    config.add_route('userCheck', '/userCheck')
    config.add_route('meetingList', '/meetingList')
    config.add_route('app_index', '/index')
    config.add_route('pad_add_meeting', '/addMeeting')
    config.add_route('pad_del_meeting', '/delMeeting')
    config.add_route('pad_update_meeting', '/updateMeeting')
    config.add_route('pad_org_list', '/orgList')
    config.add_route('pad_set_room', '/setRoom')


def user_include(config):
    config.add_route('to_user', '/to_user')
    config.add_route('list_user', '/list')
    config.add_route('to_add_user', '/to_add_user')
    config.add_route('add_user', '/add_user')
    config.add_route('to_delete_user', '/to_delete_user')
    config.add_route('delete_user', '/delete_user')
    config.add_route('to_update_user', '/to_update_user')
    config.add_route('update_user', '/update_user')
    config.add_route('to_user_setting', '/to_user_setting')
    config.add_route('user_setting', '/user_setting')


def org_include(config):
    config.add_route('to_org', '/to_org')
    config.add_route('list_org', '/list')
    config.add_route('to_add_org', '/to_add_org')
    config.add_route('add_org', '/add_org')
    config.add_route('to_update_org', '/to_update_org')
    config.add_route('update_org', '/update_org')
    config.add_route('delete_org', '/delete_org')


def role_include(config):
    config.add_route('to_role', '/to_role')
    config.add_route('list_role', '/list')
    config.add_route('to_add_role', '/to_add')
    config.add_route('delete_role', '/del')
    config.add_route('add_role', '/add')
    config.add_route('to_update_role', '/to_update')
    config.add_route('update_role', '/update')


def auth_include(config):
    config.add_route('to_auth', '/to_auth')
    config.add_route('to_auth_user', '/to_auth_user')


def boardroom_include(config):
    config.add_route('to_brs_info', '/to_brs_info')
    config.add_route('to_br', '/to_boardroom')
    config.add_route('list_br', '/list')
    config.add_route('to_add_br', '/to_add_boardroom')
    config.add_route('add_br', '/add_boardroom')
    config.add_route('delete_br', '/delete_boardroom')
    config.add_route('to_update_br', '/to_update_boardroom')
    config.add_route('update_br', '/update_boardroom')
    config.add_route('br_upload_pic', '/br_upload_pic')
    config.add_route('br_booking', '/boardroom_booking')


def terminal_include(config):
    config.add_route('to_terminal', '/to_terminal')
    config.add_route('list_terminal', '/list')
    config.add_route('add_terminal', '/add')
    config.add_route('to_add_terminal', '/to_add')
    config.add_route('to_update_terminal', '/to_update')
    config.add_route('delete_terminal', '/del')
    config.add_route('update_terminal', '/update')


def meeting_include(config):
    config.add_route('to_meeting', '/to_meeting')
    config.add_route('list_meeting', '/list')
    config.add_route('to_add_meeting', '/to_add')
    config.add_route('delete_meeting', '/del')
    config.add_route('add_meeting', '/add')
    config.add_route('to_update_meeting', '/to_update')
    config.add_route('update_meeting', '/update')


def booking_include(config):
    config.add_route('list_my_meeting', '/list_my')
    config.add_route('list_booking', '/list')
    config.add_route('delete_booking', '/delete_booking')
    config.add_route('check_available', '/check_available')
    config.add_route('meeting_booking', '/meeting_booking')
    config.add_route('list_by_org', '/list_by_org')
    config.add_route('list_by_br', '/list_by_br')
