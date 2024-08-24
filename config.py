from configparser import ConfigParser

def config(filename='database.ini', section='postgresql') -> dict:
    """Загрузить параметры подключения к базе данных из конфигурационного файла."""
    parser = ConfigParser()
    parser.read(filename)

    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f'Section {0} is not found in the {1} file.'.format(section, filename))

    return db_params