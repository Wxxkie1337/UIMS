from utils.decorators import ensure_connected
import secrets


class RoleInvitesMixin:
    @ensure_connected
    async def create_invite(self, role: str) -> str:
        while True:
            token = secrets.token_urlsafe(16)

            result = await self._connection.execute(
                "INSERT INTO role_invites (token, role) VALUES ($1, $2) ON CONFLICT (token) DO NOTHING",
                token,
                role
            )

            if result != "INSERT 0 0":
                return token
        
    
    @ensure_connected
    async def use_role(self, token: str) -> str:        
        result = await self._connection.fetchrow(
            "DELETE FROM role_invites WHERE token = $1 RETURNING role",
            token
        )
        
        role = result["role"] if result else None
        if not role:
            return None
        
        return role
    

    @ensure_connected
    async def cleanup_role_invites(self) -> None:
        await self._connection.execute(
            """
            DELETE FROM role_invites
            WHERE created_at < NOW() - INTERVAL '1 hour'
            """
        )
