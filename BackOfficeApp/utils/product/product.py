import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.product_item.name, instance.product_item.year,'productItemId', instance.product_item.id, ext)
    return os.path.join('product_images', filename)
