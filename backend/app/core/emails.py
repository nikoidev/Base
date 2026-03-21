from loguru import logger

async def send_reset_password_email(email_to: str, token: str) -> None:
    """
    Simulates sending an email by using structured logging.
    In a real app, this would use a service like SendGrid, AWS SES, or an SMTP client.
    """
    logger.info(f"📧 Sending password reset email to: {email_to}")
    
    # In a frontend framework like Next.js, the reset link typically points to a web page
    # which then calls the /api/auth/reset-password endpoint with the token.
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    
    email_body = f"""
    --- EMAIL CONTENT ---
    Subject: Reestablecer tu contraseña
    To: {email_to}
    
    Hemos recibido una solicitud para reestablecer tu contraseña.
    Haz clic en el siguiente enlace para crear una nueva:
    
    {reset_link}
    
    Si no fuiste tú, ignora este correo.
    El enlace expirará en 1 hora.
    ---------------------
    """
    logger.debug(email_body)
    logger.info("📧 Email sent successfully (SIMULATED).")
