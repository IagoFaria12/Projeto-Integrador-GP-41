import logging

def config_log():
    return logging.basicConfig(
        level=logging.DEBUG,
        filename="./logs/system.log",
        format="%(levelname)s - %(message)s - %(asctime)s ",
        filemode="a"
    )

def set_log(type, message):
    function_dict = {
        "debug": logging.debug,
        "info": logging.info,
        "warning": logging.warning,
        "error": logging.error,
        "critical": logging.critical
    }

    func = function_dict.get(type)
    return func(message)