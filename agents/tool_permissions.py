ALLOWED_TOOLS = {
    "USER": [
        "calculator",
        "document_search"
    ],

    "OPERATOR": [
        "calculator",
        "document_search"
    ],

    "ADMIN": [
        "calculator",
        "document_search",
        "database_query",
        "send_email"
    ]
}


class ToolPermissionManager:

    def __init__(self, role):
        self.role = role.upper()

    def is_allowed(self, tool_name):

        allowed_tools = ALLOWED_TOOLS.get(
            self.role,
            []
        )

        return tool_name in allowed_tools

    def check_permission(self, tool_name):

        if self.is_allowed(tool_name):
            print(
                f"ALLOWED: {self.role} can use {tool_name}"
            )
            return True

        print(
            f"DENIED: {self.role} cannot use {tool_name}"
        )
        return False


if __name__ == "__main__":

    user_permissions = ToolPermissionManager("USER")

    operator_permissions = ToolPermissionManager("OPERATOR")

    admin_permissions = ToolPermissionManager("ADMIN")

    print("\nUSER:")

    user_permissions.check_permission(
        "calculator"
    )

    user_permissions.check_permission(
        "database_query"
    )

    print("\nOPERATOR:")

    operator_permissions.check_permission(
        "document_search"
    )

    operator_permissions.check_permission(
        "database_query"
    )

    print("\nADMIN:")

    admin_permissions.check_permission(
        "database_query"
    )

    admin_permissions.check_permission(
        "send_email"
    )
