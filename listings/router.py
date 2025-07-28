class ListingsRouter:

    route_app_labels = {'listings'} #listings app

#    'listings.router.ListingsRouter'

    """
        Attempts to read listings and contenttypes models go to listings db.
    """
    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.route_app_labels:
            return 'listings' # better to make it with hint like listings_db
        return None



    def db_for_write(self, model, **hints):

        """
        Attempts to write listings and contenttypes models go to listings db.
        """
        if model._meta.app_label in self.route_app_labels:
            return "listings"
        return None



    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the listings or contenttypes apps is
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
        Make sure the listings and contenttypes apps only appear in the
        'listings' database.
        """
        if app_label in self.route_app_labels:
            return db == "listings"
        return None
