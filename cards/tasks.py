from django.core.mail import send_mail

from trelloclone.celery import app


@app.task(name='send_email')
def send_cards_duedate_notification(correo):
    #for _ in range len(correos):
        send_mail(
            'Recordatorio del vencimiento de tarea.',
            '<h1>Vencimientode tarea</h1><b><p>Le recordamos que su tarea vence mañana...</p><b><h2>APURESE!!!</h2>',
            'hola@recordatoriodetareas.com',
            [correo],
            fail_silently=False
        )
