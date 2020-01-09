# utils/permission.py


class SVIPPremission(object):
    message = "必须是SVIP才能访问"  # 这里的message表示如果不通过权限的时候，错误提示信息

    def has_permission(self, request,view):
        if request.user.user_type != 3:
            return False
        return True


class MyPremission(object):
    # 这个权限类表示当用户为SVIP时不可通过
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True