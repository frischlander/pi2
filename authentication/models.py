from django.db import models
from django.contrib.auth.models import User
import pyotp
import qrcode
from io import BytesIO
import base64

#class UserTwoFactorAuth(models.Model):
    #Modelo para armazenar configurações de autenticação de dois fatores
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor_auth')
    #is_enabled = models.BooleanField(default=False)
    #secret_key = models.CharField(max_length=32, blank=True)
    #backup_codes = models.TextField(blank=True)  # Códigos de backup JSON
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    #def __str__(self):
       # return f"2FA - {self.user.username}"

    def generate_secret(self):
        """Gera uma nova chave secreta"""
        self.secret_key = pyotp.random_base32()
        return self.secret_key

    def get_totp(self):
        """Retorna o objeto TOTP para o usuário"""
        return pyotp.TOTP(self.secret_key)

    def get_qr_code_url(self):
        """Gera a URL do código QR"""
        if not self.secret_key:
            return None
        
        totp = self.get_totp()
        provisioning_uri = totp.provisioning_uri(
            name=self.user.email,
            issuer_name='Conecta CAA'
        )
        return provisioning_uri

    def get_qr_code_image(self):
        """Gera a imagem do código QR em base64"""
        qr_uri = self.get_qr_code_url()
        if not qr_uri:
            return None
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converter para base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def verify_token(self, token):
        """Verifica se o token TOTP é válido"""
        if not self.is_enabled or not self.secret_key:
            return False
        
        totp = self.get_totp()
        # Permite uma margem de erro de 30 segundos (um step anterior e posterior)
        return totp.verify(token, valid_window=1)

    def generate_backup_codes(self, count=10):
        """Gera códigos de backup"""
        import json
        codes = [pyotp.random_base32()[:8] for _ in range(count)]
        self.backup_codes = json.dumps(codes)
        return codes

    def verify_backup_code(self, code):
        """Verifica e usa um código de backup"""
        import json
        if not self.backup_codes:
            return False
        
        codes = json.loads(self.backup_codes)
        if code in codes:
            codes.remove(code)
            self.backup_codes = json.dumps(codes)
            self.save()
            return True
        return False
