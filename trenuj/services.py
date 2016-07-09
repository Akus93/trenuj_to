from .models import Tag, Shortcut


def save_tags(shortcut_id, tags):
    shortcut = Shortcut.objects.get(id=shortcut_id)
    tags = tags.split(',')
    for tag in tags:
        new_tag = Tag(shortcut=shortcut, name=tag)
        new_tag.save()


def search_shortcuts(words):
    words = words.lower().split(' ')
    results = Shortcut.objects.filter(is_active=True, tag__name__in=words).distinct()
    return results


def get_shortcuts_by_tag(tag):
    result = Shortcut.objects.filter(is_active=True, tag__name__iexact=tag)
    return result
