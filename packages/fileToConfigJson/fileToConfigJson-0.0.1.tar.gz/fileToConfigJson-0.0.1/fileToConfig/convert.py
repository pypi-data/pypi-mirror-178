def configFile(filename=".env"):
    """
        Pass a valid filename to use as environment/config file.\n
        By default .env is set you can overide as you want
    """
    constants = {}
    try:
        with open('.env', 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=', 1)
                constants[key] = value
        return constants
    except:
        constants["error"] = "Invalid file name passed"
        return constants