from io import StringIO
from pathlib import Path
# pip install rich
from rich.console import Console
from datetime import datetime
from enum import Enum
import hashlib
from inspect import stack
from os import path
import traceback
from typing import Final, Literal
from typing import Optional, Any, Callable, Union

from .log_row import LogRow
from .helpful import MetaLogger
from .independent.helpful import toBitSize
from .independent.log_file import LogFile
from .independent.zip_file import ZippFile, ZipCompression

__all__ = ["logger", "loglevel", ]


class CompressionLog(Enum):
    """
    Варианты действий при достижении лимита размера файла
    """
    #: Перезаписать файл (Удалить все и начать с 0)
    def rewrite_file(
        _path_file): return CompressionLog._rewrite_file(_path_file)

    #: Сжать лог файл в архив, а после удалить лог файл
    def zip_file(_path_file): return CompressionLog._zip_file(_path_file)

    @staticmethod
    def _rewrite_file(_path_file: str):
        """Стереть данные из лог файла"""
        _f = LogFile(_path_file)
        logger.system_info(f"{_path_file}:{_f.sizeFile()}", flags=["DELETE"])
        _f.deleteFile()

    @staticmethod
    def _zip_file(_path_file: str):
        """Сжать лог файл в архив"""
        ZippFile(f"{_path_file}.zip").writeFile(
            _path_file, compression=ZipCompression.ZIP_LZMA)
        LogFile(_path_file).deleteFile()
        logger.system_info(_path_file, flags=["ZIP_AND_DELETE"])


class loglevel:
    """
    Создание логгера
    """

    #: Через сколько записей в лог файл, проверять его размер.
    CONT_CHECK_SIZE_LOG_FILE = 10

    # : Значение, которое определяет срабатывания логгера, если у экземпляра логера значение меньше чем это,
    # то он не сработает
    required_level: int = 10

    def __init__(
            self,
            title_logger: str,
            int_level: int = 10,
            fileout: Optional[Path] = None,
            console_out: bool = True,
            color_flag: str = "",
            color_title_logger: str = "",
            max_size_file: Optional[Union[int, str]] = "10mb",
            max_len_console: int = 0,
            compression: Optional[Union[CompressionLog, Callable]] = None,
            template_console: str = "{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}:{data}",
            **kwargs,
    ):
        """
        Создать логгер

        :param title_logger: Название логгера
        :param int_level: Цифровое значение логгера
        :param fileout: Куда записать данные
        :param console_out: Нужно ли выводить данные в ``stdout``
        :param max_size_file: Максимальный размер(байтах), файла после которого происходит ``compression``.
            Также можно указать:
            - kb - Например 10kb
            - mb - Например 1mb
            - None - Без ограничений
        :param max_len_console: Скольки максимум символов выводить в консоль, остальное обрезать.По умолчанию не обрезать
        :param compression: Что делать с файлам после достижение ``max_size_file``
        :param template_console: Доступные аргументы в :meth:`allowed_template_loglevel`
        """
        self.title_logger: str = title_logger
        self.fileout: Optional[Path] = fileout
        if fileout:
            # Если указан файл, то добавляем функцию для записи в файл
            self._base_logic = lambda data, flags: (self._file_write(
                data, flags), self._console_print(data, flags))
        else:
            self._base_logic = lambda data, flags: self._console_print(
                data, flags)

        self.console_out: bool = console_out
        self.color_flag: str = color_flag
        self.color_title_logger: str = color_title_logger
        self.max_size_file: Optional[int] = toBitSize(
            max_size_file) if max_size_file else None
        self.max_len_console: int = max_len_console
        self.compression: Callable = compression if compression else CompressionLog.rewrite_file
        self.int_level: int = int_level
        self.template_console: str = template_console

        #: Сколько раз было записей в лог файл, до выполнения
        #: условия ``self._cont_write_log_file < CONT_CHECK_SIZE_LOG_FILE``
        self._cont_write_log_file = 0

    def __call__(self, data: str, flags: list[str] = ""):
        """
        Вызвать логгер

        :param data:
        :param flags:
        """
        # Если уровень доступа выше или равен требуемому
        if self.int_level >= self.required_level:
            # Выполняем логику логера
            self._base_logic(data, flags)

    def _file_write(self, data: Any, flags: list[str]):
        """
        Метод вызваться для записи в файл

        :param data:
        :param flags:
        """
        # Формируем сообщение в файл
        log_formatted = allowed_template_loglevel(
            None, data, flags, self, 'file')
        # Записываем в файл
        _f = LogFile(self.fileout)
        _f.appendFile(log_formatted)
        # Проверить размер файла, если размер больше ``self.max_size_file`` то произойдет ``self.compression``
        self._check_size_log_file(_f)

    def _console_print(self, data: Any, flags: list[str]):
        """
        Метод вызваться для вывода данных в консоль

        :param data:
        :param flags:
        """
        if self.console_out:
            # Формируем сообщение в консоль
            log_formatted = allowed_template_loglevel(
                self.template_console, data, flags, self, 'console')
            print(log_formatted)

    def _check_size_log_file(self, _file: LogFile):
        """
        Для оптимизации, проверка размера файла происходит
        при достижении условия определенного количества записи в файл

        :param _file: Файл
        """
        if self._cont_write_log_file > self.CONT_CHECK_SIZE_LOG_FILE or self._cont_write_log_file == 0:
            self._check_compression_log_file(size_file=_file.sizeFile())
        self._cont_write_log_file += 1

    def _check_compression_log_file(self, size_file: int):
        """
        Проверить размер файла.
        Если он превышает ``self.max_size_file`` то  выполнять  ``self.compression``

        :param size_file: Размер файла в байтах
        """
        if self.max_size_file is not None:
            if size_file > self.max_size_file:
                self.compression(self.fileout)

    def _base_logic(self, data: Any, flags: list[str]):
        """
        Логика работы логера

        :param data:
        :param flags:
        """
        ...

    def updateCopy(self, **kwargs):
        """
        Вернуть обновленную версию loglevel

        kwargs: Обновление для loglevel.__init__
        """
        return loglevel(**dict(self.__dict__, **kwargs))


class loglevel_extend(loglevel):
    """
    Логгер с расширенной информацией о коде

    В данном случае у нас будет возможность указать место в коде где вызван логгер
    """

    def _file_write(self, data: Any, flags: str):
        # Формируем сообщение в файл
        log_formatted = allowed_template_loglevel.debug_new(
            None, data, flags, self, 'file')
        # Записываем в файл
        _f = LogFile(self.fileout)
        _f.appendFile(log_formatted)
        # Проверить размер файла, если размер больше ``self.max_size_file`` то произойдет ``self.compression``
        self._check_size_log_file(_f)

    def _console_print(self, data: Any, flags: str):
        if self.console_out:
            # Формируем сообщение в консоль
            log_formatted = allowed_template_loglevel.debug_new(
                self.template_console, data, flags, self, 'console')
            print(log_formatted)

    def updateCopy(self, **kwargs):
        """
        Вернуть обновленную версию loglevel_extend

        kwargs: Обновление для loglevel_extend.__init__
        """
        return loglevel_extend(**dict(self.__dict__, **kwargs))


class loglevel_form_error(loglevel_extend):
    """
    Логгер для ошибок
    """

    def _file_write(self, data: Any, flags: str):
        # Формируем сообщение в файл
        log_formatted, error = self.detail(data)
        # Записываем в файл
        _f = LogFile(self.fileout)
        _f.appendFile(log_formatted)
        # Проверить размер файла, если размер больше ``self.max_size_file`` то произойдет ``self.compression``
        self._check_size_log_file(_f)
        return error

    def __call__(self, data: str, flags: list[str] = ""):
        """
        Вызвать логгер

        :param data:
        :param flags:
        """
        # Если уровень доступа выше или равен требуемому
        if self.int_level >= self.required_level:
            # Выполняем логику логера
            return self._base_logic(data, flags)[0]

    def _console_print(self, data: Any, flags: str):
        if self.console_out:
            # Формируем сообщение в консоль
            log_formatted = allowed_template_loglevel.debug_new(
                self.template_console, data, flags, self, 'console')
            error: str = traceback.format_exc()
            id_error_log: str = hashlib.md5(error.encode("utf-8")).hexdigest()
            log_formatted += f":::::ERROR_LOG:::::: {id_error_log}"
            print(log_formatted)

    def detail(self, msg: str) -> str:
        """Подробный вывод ошибки

        :param path_log: Путь лог файлу
        :param msg: Сообщение
        :return: Текст ошибки, и идентификатор(ERROR_LOG) на полный стек ошибки в файле
        """
        # traceback.format_exception(e) # В виде списка
        # traceback.format_exc(e) # В виде текста
        error: str = traceback.format_exc()
        id_error_log: str = hashlib.md5(error.encode("utf-8")).hexdigest()
        time_now = datetime.now()
        #
        console = Console(width=180, file=StringIO())
        console.print_exception(show_locals=True)
        str_output = console.file.getvalue()
        #
        res = """{0}{1}{2}""".format(
            f'BEGIN---|{time_now}|{id_error_log}|{msg}\n',
            str_output,
            f'END__---|{time_now}|{id_error_log}|{msg}\n'
        )
        return res, f'{error}\n:::::ERROR_LOG::::: {id_error_log}'

    def updateCopy(self, **kwargs):
        """
        Вернуть обновленную версию loglevel_form_error

        kwargs: Обновление для loglevel_form_error.__init__
        """
        return loglevel_form_error(**dict(self.__dict__, **kwargs))


class allowed_template_loglevel:
    """
    Доступные ключи для шаблона лог сообщения в файл

    :Пример передачи:

    `{level}{flags}{data}`
    `{color_loglevel}{level}{reset}{color_flag}{flags}{reset}`
    """

    def __new__(
        cls,
        _template: str,
        data,
        flags,
        root_loglevel: loglevel,
        type_d: Literal['file', 'console'] = 'console'
    ) -> str:
        """
        Обычное сообщение

        :param _template:
        :param flags:
        :param data:
        """
        if type_d == 'console':
            return _template.format(
                #  Название логера
                title_logger=root_loglevel.title_logger,
                # Флаги
                flags=';'.join([str(x) for x in flags]),
                # Если нужно обрезаем сообщение
                data=data[:root_loglevel.max_len_console] if root_loglevel.max_len_console > 0 else data,
                #  Дата создания сообщения
                date_now=datetime.now(),
                # Закрыть цвет
                reset=MetaLogger.reset_,
                #  Цвет заголовка логера
                color_title_logger=root_loglevel.color_title_logger,
                # Цвет флага
                color_flag=root_loglevel.color_flag,
            )
        else:
            # file
            return LogRow._(title=root_loglevel.title_logger, flags=flags, data=data, is_trace=False, stack_back=5)

    @ classmethod
    def debug_new(
        cls,
        _template: str,
        data,
        flags,
        root_loglevel: loglevel,
        type_d: Literal['file', 'console'] = 'console'
    ):
        """
        Более подробное сообщение

        :param root_loglevel:
        :param _template:
        :param flags:
        :param data:
        """
        if type_d == 'console':
            caller = stack()[4]
            return _template.format(
                #  Название логера
                title_logger=root_loglevel.title_logger,
                # Флаги
                flags=';'.join([str(x) for x in flags]),
                # Если нужно обрезаем сообщение
                data=str(data)[
                    :root_loglevel.max_len_console] if root_loglevel.max_len_console > 0 else data,
                #  Дата создания сообщения
                date_now=datetime.now(),
                # Закрыть цвет
                reset=MetaLogger.reset_,
                #  Цвет заголовка логера
                color_title_logger=root_loglevel.color_title_logger,
                # Цвет флага
                color_flag=root_loglevel.color_flag,
                # Номер строки
                line_call=caller.lineno,
                # Функция в которой вызвана функция
                func_call=caller.function,
                # Контекст
                context_call=''.join(caller.code_context[0].split()),
                # Абсолютный путь к файлу в котором вызвана функция
                abs_file_call=caller.filename,
                # Файл в котором вызвана функция
                file_call=path.basename(caller.filename)
            )
        else:
            # file
            return LogRow._(title=root_loglevel.title_logger, flags=flags, data=data, is_trace=True, stack_back=5)


class logger:
    """
    Стандартные логгеры
    """

    test = loglevel(
        'TEST',
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}:\n{data}",
        color_flag=MetaLogger.gray,
        color_title_logger=MetaLogger.magenta
    )
    debug = loglevel_extend(
        "DEBUG",
        int_level=10,
        color_title_logger=MetaLogger.magenta,
        color_flag=MetaLogger.magenta,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}[{file_call}:{line_call}]:{data}\t\t\t[{context_call}]"
    )
    info = loglevel(
        "INFO",
        int_level=20,
        color_title_logger=MetaLogger.bright_blue,
        color_flag=MetaLogger.yellow,
    )
    success = loglevel(
        "SUCCESS",
        int_level=25,
        color_title_logger=MetaLogger.green,
        color_flag=MetaLogger.gray,
    )
    error = loglevel_extend(
        "ERROR",
        int_level=40,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}:{line_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        color_title_logger=MetaLogger.read,
        color_flag=MetaLogger.yellow,
    )
    errordet = loglevel_form_error(
        "ERROR",
        int_level=40,
        fileout='./errordet.log',
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}:{line_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        color_title_logger=MetaLogger.read,
        color_flag=MetaLogger.yellow,
    )
    warning = loglevel_extend(
        "WARNING",
        int_level=30,
        template_console="{color_title_logger}[{title_logger}]{reset}{color_flag}[{flags}]{reset}{color_flag}[{date_now}][{file_call}:{func_call}:{line_call}]{reset}\n{color_flag}Text:{reset}\t{data}\n{color_flag}Path:{reset}\t{abs_file_call}{line_call}\n{color_flag}Context:{reset}\t{context_call}{color_title_logger}\n[/END_{title_logger}]{reset}",
        color_flag=MetaLogger.read,
        color_title_logger=MetaLogger.yellow,
    )

    #: Логгер для системных задач
    system_info: Final[loglevel] = loglevel(
        "SYSTEM",
        int_level=40,
        color_title_logger=MetaLogger.gray,
        color_flag=MetaLogger.gray,
        console_out=True
    )
    #: Логгер для системных задач
    system_error: Final[loglevel] = loglevel(
        "SYSTEM",
        int_level=45,
        color_title_logger=MetaLogger.gray,
        color_flag=MetaLogger.read,
        console_out=True
    )
