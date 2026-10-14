from django.db import models
from django.core.validators import RegexValidator


class Area(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=200, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'area'

    def __str__(self):
        return self.nombre


class TipoReporte(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    prefijo = models.CharField(
        max_length=2,
        unique=True,
        validators=[RegexValidator(
            r'^[A-Z]{2}$',
            'El prefijo debe tener 2 letras mayúsculas. Ejemplo: RA.'
        )]
    )

    class Meta:
        db_table = 'tipo_reporte'

    def __str__(self):
        return f"{self.nombre} ({self.prefijo})"


class Responsable(models.Model):
    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=60, blank=True)
    correo = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'responsable'

    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        GENERADO = 'GENERADO', 'Generado'
        APROBADO = 'APROBADO', 'Aprobado'
        ARCHIVADO = 'ARCHIVADO', 'Archivado'

    codigo = models.CharField(max_length=10, unique=True, editable=False)
    tipo = models.ForeignKey(TipoReporte, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    responsable = models.ForeignKey(
        Responsable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    periodo = models.CharField(max_length=40)  # p. ej. "Enero - Marzo 2026"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.BORRADOR
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']
        db_table = 'reporte'

    def save(self, *args, **kwargs):
        # Genera el código la primera vez: prefijo del tipo + consecutivo
        # (RA-001, RC-002...).

        # Lee el último reporte, le suma 1 y rellena a 3 dígitos.
        if not self.codigo:
            ultimo = Reporte.objects.order_by('-id').first()
            n = (int(ultimo.codigo.split('-')[1]) + 1) if ultimo else 1
            self.codigo = f"{self.tipo.prefijo}-{n:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.tipo.nombre}"

# Create your models here.
