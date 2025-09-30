from django.db import migrations

def update_processo_format(apps, schema_editor):
    OrdemServico = apps.get_model('caaordserv', 'OrdemServico')
    
    # Primeiro, adiciona um prefixo temporário para evitar conflitos
    ordens = OrdemServico.objects.all().order_by('data_criacao')
    for index, ordem in enumerate(ordens, start=1):
        ordem.processo = f'TEMP{index:05d}'
        ordem.save()
    
    # Depois, renumera com o novo formato de 4 dígitos
    for index, ordem in enumerate(ordens, start=1):
        novo_numero = str(index).zfill(4)
        ordem.processo = f'CAA{novo_numero}'
        ordem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('caaordserv', '0003_fix_duplicate_processo'),
    ]

    operations = [
        migrations.RunPython(update_processo_format),
    ] 