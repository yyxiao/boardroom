def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('resetpwd', '/resetpwd')
    # add user 目前仅供测试使用
    config.add_route('add_user', '/adduser')
    config.include(role_include, '/role')


def role_include(config):
    config.add_route('to_role', '/torole')
    config.add_route('list_role', '/list')
    config.add_route('to_add_role', '/to_add')
    config.add_route('add_role', '/add')




