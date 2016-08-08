def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('reset_pwd', '/resetpwd')
    config.add_route('my_meeting', '/mymeeting')
    config.include(user_include, '/touser')
    config.include(org_include, '/toorg')
    config.include(role_include, '/role')
    config.include(auth_include, '/toauthorization')
    config.include(boardroom_include, '/toboardroom')
    config.include(terminal_include, '/toterminal')


def user_include(config):
    config.add_route('user', '/user')
    config.add_route('user_setting', '/usersetting')
    config.add_route('user_list', '/userlist')
    config.add_route('add_user', '/adduser')
    config.add_route('delete_user', '/deleteuser')
    config.add_route('update_user', '/updateuser')


def org_include(config):
    config.add_route('org', '/org')
    config.add_route('org_list', '/orglist')
    config.add_route('add_org', '/addorg')
    config.add_route('delete_org', '/deleteorg')
    config.add_route('update_org', '/updateorg')


def role_include(config):
    config.add_route('to_role', '/torole')
    config.add_route('list_role', '/list')
    config.add_route('to_add_role', '/to_add')
    config.add_route('add_role', '/add')


def auth_include(config):
    config.add_route('auth', '/auth')


def boardroom_include(config):
    config.add_route('boardrooms', '/boardrooms')
    config.add_route('boardroom_list', '/boardroomlist')
    config.add_route('add_boardroom', '/addboardroom')
    config.add_route('delete_boardroom', '/deleteboardroom')
    config.add_route('update_boardroom', '/updateboardroom')
    config.add_route('boardroom_booking', '/boardroombooking')
    config.add_route('boardroom_info', '/boardroominfo')


def terminal_include(config):
    config.add_route('terminal', '/terminal')
    config.add_route('terminal_list', '/terminallist')
    config.add_route('add_terminal', '/addterminal')
    config.add_route('delete_terminal', '/deleteterminal')
    config.add_route('update_terminal', '/updateterminal')