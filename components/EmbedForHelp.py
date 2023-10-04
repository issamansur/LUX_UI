from discord import Embed, Colour

HELP_STRING = str(
'''
### Основные команды:
* `/ping`: Проверить доступность бота.
* `/help`: Получить справку о доступных командах.
* `/report`: Отправить отчет о проблеме или баге.
### Управление аккаунтом пользователя:
* `/register`: Зарегистрировать аккаунт пользователя.
* `/unregister`: Отвязать аккаунт пользователя.
* `/auth` `[id гильдии]` `[телефон]` `[пароль]`: Аутентификация.
### Поиск и воспроизведение музыки:
* `/search` `[песня/автор]`: Найти и воспроизвести песню.
* `/search-album` `[плейлист]`: Найти альбом исполнителя.
* `/search-playlist` `[плейлиста]`: Найти плейлист пользователя.
### Управление воспроизведением музыки:
* `/list`: Показать список воспроизведения.
* `/repeat` `[OFF | ONE | ALL]`: Установить режим повтора.
* `/skip`: Пропустить текущую композицию.
* `/quit`: Завершить воспроизведение музыки.
'''
)

embed = Embed(
    title="Kai'Sa умеет такое:",
    url=None,
    description=HELP_STRING,
    color=Colour.blue(),
)
