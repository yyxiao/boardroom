def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('reset_pwd', '/reset_pwd')
    config.add_route('my_meeting', '/my_meeting')
    config.include(user_include, '/user')
    config.include(org_include, '/org')
    config.include(role_include, '/role')
    config.include(auth_include, '/authorization')
    config.include(boardroom_include, '/boardroom')
    config.include(terminal_include, '/terminal')


def user_include(config):
    config.add_route('to_user', '/to_user')
    config.add_route('user_setting', '/user_setting')
    config.add_route('list_user', '/list')
    config.add_route('add_user', '/add_user')
    config.add_route('delete_user', '/delete_user')
    config.add_route('update_user', '/update_user')


def org_include(config):
    config.add_route('to_org', '/to_org')
    config.add_route('list_org', '/list')
    config.add_route('add_org', '/add_org')
    config.add_route('delete_org', '/delete_org')
    config.add_route('update_org', '/update_org')


def role_include(config):
    config.add_route('to_role', '/to_role')
    config.add_route('list_role', '/list')
    config.add_route('to_add', '/to_add')
    config.add_route('delete_role', '/del')
    config.add_route('add', '/add')
    config.add_route('to_update', '/to_update')
    config.add_route('update_role', '/update')


def auth_include(config):
    config.add_route('to_auth', '/to_auth')


def boardroom_include(config):
    config.add_route('to_brs_info', '/to_brs_info')
    config.add_route('to_br', '/to_boardroom')
    config.add_route('list_br', '/list')
    config.add_route('add_br', '/add_boardroom')
    config.add_route('delete_br', '/delete_boardroom')
    config.add_route('update_br', '/update_boardroom')
    config.add_route('br_booking', '/boardroom_booking')


def terminal_include(config):
    config.add_route('to_terminal', '/to_terminal')
    config.add_route('list_terminal', '/list')
    config.add_route('add_terminal', '/add_terminal')
    config.add_route('delete_terminal', '/delete_terminal')
    config.add_route('update_terminal', '/update_terminal')