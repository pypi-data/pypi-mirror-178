from django.conf import settings


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'auth', 'contenttypes', 'admin', }
    try:
        auth_db = settings.AUTH_DB
    except NameError:
        auth_db = 'default'

    try:
        token_table = settings.REST_AUTH_TOKEN_TABLE
    except NameError:
        token_table = 'AUTHENTICATION_TOKEN'

    def db_for_read(self, model, **hints):
        if model._meta.db_table == self.token_table:
            return self.auth_db
        if model._meta.app_label in self.route_app_labels:
            return self.auth_db
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table == self.token_table:
            return self.auth_db
        if model._meta.app_label in self.route_app_labels:
            return self.auth_db
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels or
                obj1._meta.db_table == self.token_table or
                obj2._meta.db_table == self.token_table
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == self.auth_db
        return None
