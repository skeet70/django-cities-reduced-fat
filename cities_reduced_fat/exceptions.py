class InvalidItems(Exception):
    """
    The cities_reduced_fat command will skip item if a city_items_pre_import signal
    reciever raises this exception.
    """
    pass
