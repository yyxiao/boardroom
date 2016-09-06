from pyramid.config import Configurator
from pyramid_redis_sessions import session_factory_from_settings


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    config.include('pyramid_redis_sessions')
    config.include('pyramid_jinja2')
    # config.include('pyramid_mako')
    # config.add_mako_renderer('.html')
    config.add_jinja2_renderer('.html')
    config.include('.models')
    config.include('.routes')
    config.include('pyramid_tm')

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.scan()
    return config.make_wsgi_app()
