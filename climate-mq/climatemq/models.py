from django.contrib.gis.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Station(BaseModel):
    name = models.CharField(
        max_length=255
    )
    location = models.PointField()
    accepted = models.BooleanField(default=False)
    battery_level = models.FloatField(default=100.0)
    status = models.CharField(
        max_length=50,
        default='ACTIVE'
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name
    
class Unit(BaseModel):
    symbol = models.CharField(
        max_length=16,
        unique=True
    )

    name = models.CharField(
        max_length=256,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.symbol
    
class Variable(BaseModel):
    symbol = models.CharField(
        max_length=8,
    )

    name = models.CharField(
        max_length=40,
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
    )

    precision = models.IntegerField(
        null=True,
        blank=True,
    )

    scale = models.IntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class Sensor(BaseModel):
    name = models.CharField(
        max_length=256
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.RESTRICT
    )

class Data(BaseModel):
    value = models.FloatField(
        max_length=32
    )

    variable = models.ForeignKey(
        Variable,
        on_delete=models.RESTRICT,
    )

    station = models.ForeignKey(
        Station,
        on_delete=models.RESTRICT
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.value) + self.variable.unit.symbol
    

class ActuatorAction(BaseModel):
    """
    Represents concrete actions the system can perform on a station.
    Examples: 'Set Frequency', 'Reboot', 'Low Power Mode', 'Emergency Alert'.
    """
    name = models.CharField(max_length=100)
    command_key = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Goal(BaseModel):
    """
    The 'High-Level Goal' specification logic.
    Defines thresholds that trigger autonomic responses.
    """
    OPERATOR_CHOICES = (
        ('>', 'Greater Than'),
        ('<', 'Less Than'),
        ('==', 'Equal To'),
    )

    name = models.CharField(max_length=255)
    variable = models.ForeignKey(Variable, on_delete=models.CASCADE)
    operator = models.CharField(max_length=2, choices=OPERATOR_CHOICES)
    threshold = models.FloatField()
    action = models.ForeignKey(ActuatorAction, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}: {self.variable.name} {self.operator} {self.threshold}"
