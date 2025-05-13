from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Inline-кнопка "Далее"
# Inline-кнопка "Слушатель"
# Inline-кнопка "Преподаватель"

button_continue = [[InlineKeyboardButton(text="Далее", callback_data="continue_button")]]
button_student = [[InlineKeyboardButton(text="Слушатель", callback_data="button_student")]]
button_tutor = [[InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")]]

#Inline-клавиатура "Продолжить"
#Inline-клавиатура "Выберите роль"

main_keyboard = InlineKeyboardMarkup(inline_keyboard=button_continue)

main_keyboard_start = InlineKeyboardMarkup(inline_keyboard=[
    [button_student, button_tutor]
    ])
