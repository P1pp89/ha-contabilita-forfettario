async def async_setup(hass, config):
    # Crea input_number
    await hass.services.async_call(
        'input_number', 'create', 
        {'name': 'Nome Input', 'min': 0, 'max': 100}
    )
    # Crea sensori template via configurazione
    # ...
    return True