from datetime import datetime

def parse_date_year(date_str):
    if not date_str:
        return "Desconocido"
    try:
        fecha_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return fecha_obj.strftime("%Y")
    except ValueError:
        if len(date_str) == 4 and date_str.isdigit():
            return date_str
        return "Formato inválido"
