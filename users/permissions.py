from rest_framework import permissions


class StudyMaterialsPermission(permissions.BasePermission):
    """
    Ограничения действий по ролям преподавателей и модераторов:
    - Преподаватели: CRUD;
    - Модераторы: RU.
    """

    def has_permission(self, request, view):
        """
        Проверка доступа роли к контролеру.
        """
        groups = set(request.user.groups.values_list('name', flat=True))

        if 'Преподаватель' in groups:
            return True

        if 'Модератор' in groups:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка роли на действия с объектом
        """
        groups = set(request.user.groups.values_list('name', flat=True))

        if 'Преподаватель' in groups:
            return obj.owner == request.user

        if 'Модератор' in groups:
            if request.method in permissions.SAFE_METHODS or request.method in ['PUT', 'PATCH']:
                return True

        return False
