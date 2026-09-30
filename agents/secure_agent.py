from agents.tool_permissions import ToolPermissionManager


class SecureAgent:

    def __init__(self, role):

        self.permissions = ToolPermissionManager(
            role
        )

    def execute_tool(self, tool_name):

        print("\nRequested Tool:", tool_name)

        allowed = self.permissions.check_permission(
            tool_name
        )

        if not allowed:
            print("Tool Execution Denied.")
            return

        print(
            f"Executing {tool_name}..."
        )


if __name__ == "__main__":

    user_agent = SecureAgent("USER")

    user_agent.execute_tool(
        "calculator"
    )

    user_agent.execute_tool(
        "database_query"
    )


    admin_agent = SecureAgent("ADMIN")

    admin_agent.execute_tool(
        "database_query"
    )
