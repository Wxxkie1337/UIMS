# ==================================================
#                      CATEGORIES
# ==================================================

USER_CATEGORY_OPTIONS = [
    ("🚧 Дороги и тротуары", "Дороги"),
    ("🗑 Мусор и уборка", "Мусор"),
    ("💡 Освещение", "Освещение"),
    ("🚰 Вода и канализация", "Вода"),
    ("🏠 Дом и подъезд", "Дом"),
    ("🚗 Парковка", "Парковка"),
    ("🐕 Животные", "Животные"),
    ("👥 Соседи и люди", "Люди"),
]


# ==================================================
#                    COMMON BUTTONS
# ==================================================

MAIN_MENU = "🏠 В главное меню"
UNDERSTAND = "Понятно"
CANCEL = "❌ Отменить"
CONFIRM = "✅ Подтвердить"
APPEAL_PREV = "⬅️ Назад"
APPEAL_NEXT = "➡️ Вперёд"
GOOGLE_MAPS = "🗺 Google Maps"
YANDEX_MAPS = "🟡 Яндекс Карты"
BACK_BUTTON = "Назад"


# ==================================================
#                     USER BUTTONS
# ==================================================

CREATE_APPEAL = "📝 Создать обращение"
VIEW_APPEALS = "📂 Мои обращения"
LOCATION = "📍 Отправить текущее местоположение"
CUSTOM_CATEGORY = "✏️ Своя категория"
DELETE_APPEAL = "🗑 Удалить обращение"
USER_APPEAL_DETAILS_BUTTON = "Подробнее"


# ==================================================
#                  MODERATOR BUTTONS
# ==================================================

MODERATOR_MODE = "🛡 Модератор"
MODERATOR_NEW_APPEALS = "📂 Новые обращения"
MODERATOR_ACCEPT_APPEAL = "✅ Принять"
MODERATOR_REJECT_APPEAL = "❌ Отклонить"
REASON_CANCEL = "↩️ Отменить"


# ==================================================
#                    ADMIN BUTTONS
# ==================================================

ADMIN_MODE = "🗳️ Администратор"
ADMIN_APPROVED_APPEALS = "📋 Проверенные обращения"
ADMIN_DEFERRED_APPEALS = "⏳ Отложенные обращения"
ADMIN_ACTIVE_APPEALS = "🛠️ Обращения в работе"
ADMIN_MENU_BUTTON = "🗂️ Меню администратора"
ADMIN_TAKE_TO_WORK_BUTTON = "🛠️ Взять в работу"
ADMIN_DEFER_BUTTON = "⏳ Отложить"
ADMIN_COMPLETE_BUTTON = "✅ Завершить обращение"
ADMIN_REJECT_BUTTON = "❌ Отклонить обращение"
ADMIN_REASON_CANCEL_BUTTON = "↩️ Отменить"
ADMIN_REASON_CONFIRM_BUTTON = "✅ Подтвердить"
ADMIN_REASON_BACK_BUTTON = "↩️ Назад к обращениям"
ADMIN_RETURN_TO_DEFERRED_BUTTON = "⏳ Вернуть в отложенные"
ADMIN_RETURN_TO_MODERATED_BUTTON = "📋 Вернуть в проверенные"
ADMIN_CANCEL_BUTTON = "❌ Отмена"


# ==================================================
#                    OWNER BUTTONS
# ==================================================

OWNER_MODE = "🫅 Владелец"
OWNER_GENERATE_ROLE_BUTTON = "🔗 Сгенерировать ссылку на роль"
OWNER_MODERATOR_ROLE_BUTTON = "🛡 Модератор"
OWNER_ADMIN_ROLE_BUTTON = "🗳 Администратор"
OWNER_MENU_BUTTON = "🫅 Меню владельца"
OWNER_EMPLOYEES_BUTTON = "👥 Сотрудники"
OWNER_APPEALS_BUTTON = "📄 Обращения"
OWNER_BANS_BUTTON = "🚫 Блокировки"
OWNER_EMPLOYEES_MODERATORS_BUTTON = "🛡 Модераторы"
OWNER_EMPLOYEES_ADMINS_BUTTON = "🗳 Администраторы"
OWNER_EMPLOYEE_MANAGER_BUTTON = "↩️ К списку сотрудников"
OWNER_REMOVE_ROLE_BUTTON = "❌ Снять роль"
OWNER_BAN_BUTTON = "🚫 Заблокировать"
OWNER_UNBAN_BUTTON = "✅ Разблокировать"
OWNER_BAN_AUTHOR_BUTTON = "🚫 Заблокировать автора"
OWNER_ROLE_MODERATOR_TEXT = "Модератор"
OWNER_ROLE_ADMIN_TEXT = "Администратор"
OWNER_ROLE_USER_TEXT = "Пользователь"


# ==================================================
#                    USER TEXTS
# ==================================================

WELCOME_TEXT = (
    "<b>Добро пожаловать в помощник ЖК «Янино-1»</b>\n\n"
    "Здесь вы можете отправить обращение о любой проблеме на территории комплекса: "
    "например, о мусоре, освещении, протечке или другой ситуации."
)

USER_MAIN_MENU_TEXT = (
    "<b>Главное меню</b>\n\n"
    "Выберите, что хотите сделать: создать новое обращение или посмотреть уже отправленные."
)

STEP_CATEGORY_SELECT_TEXT = (
    "<b>Шаг 1 из 4: Категория</b>\n"
    "Выберите категорию обращения."
)

STEP_CUSTOM_CATEGORY_TEXT = (
    "<b>Шаг 1 из 4: Категория</b>\n"
    "Введите название категории."
)

INVALID_CATEGORY_TEXT = (
    "❌ <b>Некорректная категория</b>\n"
    "Название должно содержать от 3 до 30 символов."
)

STEP_DESCRIPTION_TEXT = (
    "<b>Шаг 2 из 4: Описание</b>\n"
    "Опишите проблему подробнее (минимум 10 символов)."
)

SHORT_DESCRIPTION_TEXT = (
    "❌ <b>Описание слишком короткое</b>\n"
    "Добавьте больше деталей (минимум 10 символов)."
)

STEP_PHOTO_TEXT = (
    "<b>Шаг 3 из 4: Фото</b>\n"
    "Отправьте фото, чтобы было проще разобраться в проблеме."
)

PHOTO_REQUIRED_TEXT = (
    "📸 <b>Нужно фото</b>\n"
    "Пожалуйста, отправьте фотографию проблемы."
)

STEP_LOCATION_TEXT = (
    "<b>Шаг 4 из 4: Местоположение</b>\n"
    "Отправьте геопозицию или напишите адрес вручную.\n"
    "Используйте кнопку 📎 → «Геопозиция»."
)

CHECK_BEFORE_SUBMIT_TEXT = (
    "<b>Проверьте данные перед отправкой 👇</b>"
)

APPEAL_CANCELLED_TEXT = (
    "✅ <b>Создание обращения отменено</b>\n"
    "Вы можете начать заново в любое время."
)

NO_ACTIVE_APPEAL_TEXT = (
    "ℹ️ <b>Нет активного обращения</b>\n"
    "Сейчас нечего отменять."
)

APPEAL_SENT_TEXT = (
    "✅ <b>Обращение отправлено</b>\n"
    "Мы передали его на модерацию."
)

OUTDATED_APPEAL_TEXT = (
    "ℹ️ <b>Обращение больше не актуально</b>\n"
    "Создайте новое из главного меню."
)

NO_APPEALS_TEXT = (
    "ℹ️ <b>У вас пока нет обращений</b>\n"
    "Создайте первое обращение."
)

STATUS_PENDING = "🕓 На модерации"
STATUS_ACCEPTED = "📋 Принято"
STATUS_IN_PROGRESS = "🛠 В работе"
STATUS_REJECTED = "❌ Отклонено"
STATUS_COMPLETED = "✅ Выполнено"

REJECT_REASON_EMPTY = "Причина не указана."
INVALID_INVITE_TEXT = "❌ Ссылка недействительна."
TEXT_MISSING = "Не указано"
ADMIN_MESSAGE_TEXT = "💬 Сообщение администратора:\n{text}"


# ==================================================
#                 MODERATOR TEXTS
# ==================================================

MODERATOR_MENU_TEXT = (
    "<b>Меню модератора</b>\n"
    "Выберите действие."
)

MODERATOR_ACCEPTED_NOTIFY_TEXT = (
    "✅ <b>Обращение № {appeal_id} принято</b>\n"
    "Оно передано в дальнейшую работу."
)

MODERATOR_REJECT_PROMPT_TEXT = (
    "<b>Отклонение обращения</b>\n\n"
    "Введите причину. Пользователь увидит это сообщение."
)

MODERATOR_REJECT_CONFIRM_TEXT = (
    "<b>Подтвердите отклонение</b>\n\n"
    "Проверьте причину:\n\n"
    "{reason}"
)

MODERATOR_REJECTED_NOTIFY_TEXT = (
    "❌ Обращение № {appeal_id} отклонено.\n"
    "Причину можно посмотреть в карточке."
)

MODERATOR_NO_APPEALS_TEXT = (
    "ℹ️ <b>Новых обращений нет</b>\n"
    "Попробуйте позже или выберите другое действие."
)


# ==================================================
#                   ADMIN TEXTS
# ==================================================

ADMIN_ACCESS_DENIED_TEXT = (
    "⛔ <b>Доступ запрещён</b>\n"
    "У вас нет прав для этого раздела."
)

ADMIN_MENU_TEXT = (
    "<b>Меню администратора</b>\n"
    "Выберите действие."
)

ADMIN_NO_APPEALS_TEXT = (
    "ℹ️ <b>Проверенных обращений нет</b>\n"
    "Выберите другой раздел."
)

ADMIN_NO_DEFERRED_APPEALS_TEXT = (
    "ℹ️ <b>Отложенных обращений нет</b>\n"
    "Они появятся здесь, когда будут созданы."
)

ADMIN_NO_ACTIVE_APPEALS_TEXT = (
    "ℹ️ <b>Нет обращений в работе</b>\n"
    "Сейчас у вас нет активных задач."
)

ADMIN_REJECT_PROMPT_TEXT = (
    "❌ <b>Отклонение обращения</b>\n\n"
    "Введите причину. Пользователь увидит это сообщение."
)

ADMIN_REJECT_CONFIRM_TEXT = (
    "❓ <b>Подтвердить отклонение?</b>\n\n"
    "{reason}"
)

ADMIN_REJECTED_NOTIFY_TEXT = (
    "❌ <b>Обращение отклонено</b>\n"
    "Причину можно посмотреть в карточке.\n"
    "{appeal_number}"
)

ADMIN_REASON_SENT_TEXT = (
    "✅ Причина отклонения отправлена пользователю."
)

ADMIN_REJECT_FAILED_TEXT = (
    "❌ Не удалось отклонить обращение.\n"
    "Попробуйте ещё раз позже."
)

ADMIN_TO_WORK_NOTIFY_TEXT = (
    "🛠 Обращение взято в работу.\n"
    "{appeal_number}"
)

ADMIN_COMPLETED_NOTIFY_TEXT = (
    "✅ <b>Обращение выполнено</b>\n"
    "{appeal_number}"
)

ADMIN_COMPLETE_APPEAL_PROMPT_TEXT = (
    "💬 Отправьте сообщение о завершении обращения.\n"
    "Можно добавить текст, фото или видео."
)

ADMIN_RETURNED_TO_APPROVED_NOTIFY_TEXT = (
    "📋 Обращение возвращено в список проверенных."
)

ADMIN_RETURN_TO_APPROVED_FAILED_TEXT = (
    "❌ Не удалось вернуть обращение."
)

ADMIN_RETURN_TO_DEFERRED_FAILED_TEXT = (
    "❌ Не удалось переместить обращение в отложенные."
)

ADMIN_COMPLETE_PREVIEW_TEXT = (
    "👀 <b>Предпросмотр</b>\n\n"
    "{text}"
)

ADMIN_COMPLETE_INVALID_MESSAGE_TEXT = (
    "❌ Сообщение не может быть пустым."
)

ADMIN_COMPLETE_MEDIA_GROUP_ERROR_TEXT = (
    "❌ Нельзя отправить альбом.\n"
    "Пришлите одно сообщение или файл."
)

ADMIN_APPEAL_NO_LONGER_ACTIVE_TEXT = (
    "ℹ️ Обращение больше не активно."
)

ADMIN_ACTION_FAILED_TEXT = (
    "❌ Не удалось выполнить действие.\n"
    "Попробуйте ещё раз."
)


# ==================================================
#                   OWNER TEXTS
# ==================================================

OWNER_MENU_TEXT = (
    "<b>Меню владельца</b>\n"
    "Выберите действие."
)

OWNER_CHOOSE_ROLE_TEXT = (
    "<b>Выдача роли</b>\n"
    "Выберите роль для создания ссылки."
)

OWNER_ROLE_LINK_TEXT = (
    "<b>Ссылка для активации роли</b>\n"
    "https://t.me/{bot_user}?start=invite_{token}"
)

OWNER_ROLE_LINK_ERROR_TEXT = (
    "❌ Не удалось создать ссылку."
)

OWNER_EMPLOYEES_MENU_TEXT = (
    "<b>Сотрудники</b>\n"
    "Выберите категорию."
)

OWNER_ADMINS_LIST_TEXT = (
    "<b>Администраторы</b>\n"
    "Выберите сотрудника."
)

OWNER_MODERATORS_LIST_TEXT = (
    "<b>Модераторы</b>\n"
    "Выберите сотрудника."
)

OWNER_EMPLOYEE_NOT_FOUND_TEXT = "Сотрудник не найден."
OWNER_EMPLOYEE_USERNAME_MISSING = "Не указан"

OWNER_EMPLOYEE_CARD_TEXT = (
    "<b>Карточка сотрудника</b>\n\n"
    "{ban_notice}"
    "Пользователь: <a href='{userlink}'>{username}</a>\n"
    "Роль: {role}\n"
    "Назначена: {created_at}\n"
    "{stats_block}"
)

OWNER_EMPLOYEE_BANNED_TEXT = (
    "⚠️ <b>Пользователь заблокирован</b>\n\n"
)

OWNER_MODERATOR_STATS_TEXT = (
    "Принято: {accepted}\n"
    "Отклонено: {rejected}\n"
)

OWNER_NOTIFY_MODERATOR_REMOVED_TEXT = "Ваша роль модератора снята."
OWNER_NOTIFY_ADMIN_REMOVED_TEXT = "Ваша роль администратора снята."
OWNER_NOTIFY_UNBANNED_TEXT = "Ваш аккаунт разблокирован."
OWNER_NOTIFY_BANNED_TEXT = "Ваш аккаунт заблокирован."

OWNER_APPEALS_HISTORY_EMPTY_TEXT = (
    "ℹ️ <b>История пуста</b>\n"
    "Нет обращений для отображения."
)

OWNER_BAN_HISTORY_EMPTY_TEXT = (
    "ℹ️ <b>Нет заблокированных пользователей</b>"
)

OWNER_BAN_HISTORY_TITLE_TEXT = (
    "<b>Заблокированные пользователи</b>\n"
    "Выберите пользователя."
)

OWNER_BAN_HISTORY_USER_CARD_TEXT = (
    "<b>Карточка пользователя</b>\n\n"
    "Профиль: <a href='{userlink}'>{username}</a>\n"
    "Роль: {role}\n"
    "Дата регистрации: {created_at}"
)


# ==================================================
#                    LABEL TEXTS
# ==================================================

LABEL_USER = "✌️ <b><a href='{}'>Отправитель обращения</a></b>"
LABEL_STATUS = "📌 <b>Статус:</b>"
LABEL_DATE = "📅 <b>Дата:</b>"
LABEL_CATEGORY = "🗂 <b>Категория:</b>"
LABEL_DESCRIPTION = "📝 <b>Описание:</b>"
LABEL_COORDINATES = "📍 <b>Координаты:</b>"
LABEL_ADDRESS = "📍 <b>Адрес:</b>"
LABEL_REJECT_REASON = "❌ <b>Причина отклонения:</b>"
LABEL_APPEAL_NUMBER = "Номер обращения:"
PLACEHOLDER_DASH = "—"
PAGE_INDICATOR = "📄 {current}/{total}"


# ==================================================
#                   SYSTEM TEXTS
# ==================================================

TODAY = "Сегодня"
YESTERDAY = "Вчера"
UNKNOWN_MAP_SERVICE = "Неподдерживаемый сервис карты: {service}"
CONFIG_ENV_ERROR = "Заполните BOT_TOKEN и DATABASE_URL в data/.env"
DB_NOT_CONNECTED = (
    "База данных не подключена. Вызовите метод connect() перед использованием."
)
ACCESS_DENIED_ALERT = "⛔ У вас нет прав."
BANNED_ALERT = "⛔ Вы заблокированы."
