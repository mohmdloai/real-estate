class AuthRouter():

    route_app_labels = {'users'} #users app


    """
        Attempts to read users and contenttypes models go to users db.
    """
    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'users' # better to make it with hint like users_db
        return None



    def db_for_write(self, model, **hints):

        """
        Attempts to write users and contenttypes models go to users db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "users"
        return None



    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the users or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None



    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the users and contenttypes apps only appear in the
        'users' database.
        """
        if app_label in self.route_app_labels:
            return db == "users"
        return None
