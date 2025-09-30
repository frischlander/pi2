from django.db import migrations

def update_processo_format(apps, schema_editor):
    OrdemServico = apps.get_model('caaordserv', 'OrdemServico')
    
    # Primeiro, adiciona um prefixo temporário para evitar conflitos
    ordens = OrdemServico.objects.all().order_by('data_criacao')
    for index, ordem in enumerate(ordens, start=1):
        ordem.processo = f'TEMP{index:07d}'
        ordem.save()
    
    # Depois, renumera com o novo formato de 6 dígitos
    for index, ordem in enumerate(ordens, start=1):
        novo_numero = str(index).zfill(6)
        ordem.processo = f'CAA{novo_numero}'
        ordem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('caaordserv', '0004_update_processo_format'),
    ]

    operations = [
        migrations.RunPython(update_processo_format),
    ] 