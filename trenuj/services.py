from .models import Tag, Shortcut


def save_tags(shortcut_id, tags):
    shortcut = Shortcut.objects.get(id=shortcut_id)
    tags = tags.split(',')
    for tag in tags:
        new_tag = Tag(shortcut=shortcut, name=tag)
        new_tag.save()

