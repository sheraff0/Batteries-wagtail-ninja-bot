def update_instance(instance, attrs):
    for k, v in attrs.items():
        setattr(instance, k, v)
    return instance
