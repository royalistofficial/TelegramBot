import logging

def setup_logger(log_file_path='logs/logs_bot.log'):
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.WARNING)  

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) 

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# logger.debug('Это отладочное сообщение')  # Не будет записано никуда
# logger.info('Это информационное сообщение')  # Будет выведено в консоль
# logger.warning('Это предупреждение')  # Будет записано в файл и выведено в консоль
# logger.error('Это сообщение об ошибке')  # Будет записано в файл и выведено в консоль
# logger.critical('Это критическое сообщение')  # Будет записано в файл и выведено в консоль