class UserRole:
    NORMAL = "normal"
    ADMIN = "admin"

class UserPermission:
    CREATE_QUESTION = "create_question"
    PLACE_ORDER = "place_order"

ROLE_PERMISSIONS = {
    UserRole.ADMIN: [UserPermission.CREATE_QUESTION, UserPermission.PLACE_ORDER],
    UserRole.NORMAL: [UserPermission.PLACE_ORDER]
}
