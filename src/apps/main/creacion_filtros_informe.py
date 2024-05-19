def crear_dict(mapping, key, value):
    """Se encarga de limpiar los valores que se envian en los filtros para crear el 
    diccionario de consulta.
    """
    if value !=0:
        mapping[key] = value
   