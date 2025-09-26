import re
from django.core.exceptions import ValidationError


BR_STATE_CHOICES = (
    ("AC", "Acre"), ("AL", "Alagoas"), ("AP", "Amapá"), ("AM", "Amazonas"), ("BA", "Bahia"),
    ("CE", "Ceará"), ("DF", "Distrito Federal"), ("ES", "Espírito Santo"), ("GO", "Goiás"), ("MA", "Maranhão"),
    ("MT", "Mato Grosso"), ("MS", "Mato Grosso do Sul"), ("MG", "Minas Gerais"), ("PA", "Pará"), ("PB", "Paraíba"),
    ("PR", "Paraná"), ("PE", "Pernambuco"), ("PI", "Piauí"), ("RJ", "Rio de Janeiro"), ("RN", "Rio Grande do Norte"),
    ("RS", "Rio Grande do Sul"), ("RO", "Rondônia"), ("RR", "Roraima"), ("SC", "Santa Catarina"), ("SP", "São Paulo"),
    ("SE", "Sergipe"), ("TO", "Tocantins"),
)


def validate_state_code(value: str):
    if not value:
        return
    if not re.fullmatch(r"[A-Z]{2}", value or ""):
        raise ValidationError("Estado deve ser um código de 2 letras em maiúsculas.")
    codes = {c for c, _ in BR_STATE_CHOICES}
    if value not in codes:
        raise ValidationError("Estado inválido.")


