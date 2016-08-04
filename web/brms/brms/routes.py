def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/')
    config.add_route('home', '/login')
    config.add_route('checkout', '/checkout')
    config.add_route('resetpwd', '/resetpwd')




