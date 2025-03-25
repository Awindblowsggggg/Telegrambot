import json
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, filters
import re

# Definición de los estados del formulario
ID_CARRO, CONDICION, TIPO, FECHA, HORA, AM_PM, IMPORTE, CONDUCTOR1, CONDUCTOR2, OBSERVACION, TONELADAS = range(11)

# Archivo para almacenar los formularios
FORMULARIOS_FILE = "formularios.json"

# Cargar formularios existentes
def cargar_formularios():
    if os.path.exists(FORMULARIOS_FILE):
        with open(FORMULARIOS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Guardar formularios
def guardar_formularios(formularios):
    with open(FORMULARIOS_FILE, 'w') as file:
        json.dump(formularios, file)

# Función para iniciar el formulario
async def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [
        ['4227', '4242', '4243'],
        ['4245', '4254', '5441'],
        ['5524', '9061', '9063'],
        ['VW1', 'VW2', 'VW3']
    ]
    await update.message.reply_text(
        "¡Hola! Vamos a comenzar el formulario 🧾.\n\n"
        "1️⃣. Selecciona el ID del Carro 🚛:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return ID_CARRO

# Función para manejar el campo "ID Carro"
async def id_carro(update: Update, context: CallbackContext) -> int:
    context.user_data['id_carro'] = update.message.text
    reply_keyboard = [
        ['Listo', 'MC', 'MP'],
        ['PH', 'Op', 'T.Inact'],
        ['ESP']
    ]
    await update.message.reply_text(
        "2️⃣. Selecciona la condición ♻️  (List, MC, MP , PH , Op , T.Inact , ESP):",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CONDICION

# Función para manejar el campo "Condición"
async def condicion(update: Update, context: CallbackContext) -> int:
    context.user_data['condicion'] = update.message.text
    reply_keyboard = [['Inicio', 'Fin']]
    await update.message.reply_text(
        "3️⃣. Elige el tipo (✅Inicio/❌Fin):",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return TIPO

# Función para manejar el campo "Tipo"
async def tipo(update: Update, context: CallbackContext) -> int:
    id_carro = context.user_data.get('id_carro')
    tipo = update.message.text

    # Cargar formularios existentes
    formularios = cargar_formularios()

    # Verificar si ya hay un formulario con Tipo: inicio para el mismo ID Carro
    if tipo == "Inicio" and any(f['id_carro'] == id_carro and f['tipo'] == "Inicio" for f in formularios.values()):
        await update.message.reply_text(
            f"No se puede iniciar un nuevo formulario para el ID CARRO 🚛 {id_carro} porque ya existe otro en proceso. Por favor, debe darle fin a la Condición anterior antes de iniciar una nueva.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    context.user_data['tipo'] = tipo

    if tipo == "Inicio":
        await update.message.reply_text(
            "4️⃣. Introduce la fecha en formato día/mes/año 📆 (ejemplo: 16/03/2025):",
            reply_markup=ReplyKeyboardRemove()
        )
    elif tipo == "Fin":
        await update.message.reply_text(
            "Finalizando el formulario. Por favor, completa los demás campos.",
            reply_markup=ReplyKeyboardRemove()
        )

    return FECHA

# Función para manejar el campo "Fecha"
async def fecha(update: Update, context: CallbackContext) -> int:
    fecha = update.message.text
    if not re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', fecha):
        await update.message.reply_text("Formato incorrecto. Intenta de nuevo 📆 (día/mes/año):")
        return FECHA
    context.user_data['fecha'] = fecha
    await update.message.reply_text(
        "5️⃣. Introduce la hora en formato hora:minutos ⏰ (ejemplo: 02:30):"
    )
    return HORA

# Función para manejar el campo "Hora"
async def hora(update: Update, context: CallbackContext) -> int:
    hora = update.message.text
    if not re.match(r'^\d{1,2}:\d{2}$', hora):
        await update.message.reply_text("Formato incorrecto. Intenta de nuevo  ⏰ (hora:minutos):")
        return HORA
    context.user_data['hora'] = hora
    reply_keyboard = [['AM', 'PM']]
    await update.message.reply_text(
        "Selecciona si es AM o PM:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return AM_PM

# Función para manejar el campo "AM/PM"
async def am_pm(update: Update, context: CallbackContext) -> int:
    context.user_data['am_pm'] = update.message.text
    context.user_data['hora_completa'] = f"{context.user_data['hora']} {context.user_data['am_pm']}"
    await update.message.reply_text("6️⃣. Introduce el importe en valor numérico:")
    return IMPORTE

# Función para manejar el campo "Importe"
async def importe(update: Update, context: CallbackContext) -> int:
    importe = update.message.text
    if not importe.isdigit():
        await update.message.reply_text("El importe debe ser un número. Intenta de nuevo:")
        return IMPORTE
    context.user_data['importe'] = int(importe)
    reply_keyboard = [
        ['Raidel Castel Neyra'],
        ['Serguei Lago López'],
        ['Oscar Cruz Figueredo'],
        ['Leonides Ruiz Núñez'],
        ['Carlos Fonseca Tamayo'],
        ['Diosdado Quezada Aguilera'],
        ['Lienmi Almarales Oña'],
        ['Reynaldo Real Almarales']
    ]
    await update.message.reply_text(
        "7️⃣. Selecciona al Conductor 1:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CONDUCTOR1

# Función para manejar el campo "Conductor 1"
async def conductor1(update: Update, context: CallbackContext) -> int:
    context.user_data['conductor1'] = update.message.text
    reply_keyboard = [
        ['Raidel Castel Neyra'],
        ['Serguei Lago López'],
        ['Oscar Cruz Figueredo'],
        ['Leonides Ruiz Núñez'],
        ['Carlos Fonseca Tamayo'],
        ['Diosdado Quezada Aguilera'],
        ['Lienmi Almarales Oña'],
        ['Reynaldo Real Almarales']
    ]
    await update.message.reply_text(
        "8️⃣. Selecciona al Conductor 2:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return CONDUCTOR2

# Función para manejar el campo "Conductor 2"
async def conductor2(update: Update, context: CallbackContext) -> int:
    context.user_data['conductor2'] = update.message.text
    await update.message.reply_text("9. Escribe cualquier observación:")
    return OBSERVACION

# Función para manejar el campo "Observación"
async def observacion(update: Update, context: CallbackContext) -> int:
    context.user_data['observacion'] = update.message.text
    await update.message.reply_text("10. Introduce el número de toneladas (1-100):")
    return TONELADAS

# Función para manejar el campo "Toneladas"
async def toneladas(update: Update, context: CallbackContext) -> int:
    toneladas = update.message.text
    if not toneladas.isdigit() or not (1 <= int(toneladas) <= 100):
        await update.message.reply_text("El valor debe ser un número entre 1 y 100. Intenta de nuevo:")
        return TONELADAS
    context.user_data['toneladas'] = int(toneladas)

    # Obtener nombre del usuario
    nombre_usuario = update.effective_user.first_name or "Usuario desconocido"

    # Crear resumen con solo los datos válidos
    resumen = (
        f"Formulario completado por: {nombre_usuario}\n"
        f"1. ID Carro: {context.user_data.get('id_carro', 'No especificado')}\n"
        f"2. Condición: {context.user_data.get('condicion', 'No especificada')}\n"
        f"3. Tipo: {context.user_data.get('tipo', 'No especificado')}\n"
        f"4. Fecha: {context.user_data.get('fecha', 'No especificada')}\n"
        f"5. Hora: {context.user_data.get('hora_completa', 'No especificada')}\n"
        f"6. Importe: {context.user_data.get('importe', 'No especificado')}\n"
        f"7. Conductor 1: {context.user_data.get('conductor1', 'No especificado')}\n"
        f"8. Conductor 2: {context.user_data.get('conductor2', 'No especificado')}\n"
        f"9. Observación: {context.user_data.get('observacion', 'No especificada')}\n"
        f"10. Toneladas: {context.user_data.get('toneladas', 'No especificadas')}"
    )

    # Enviar resumen al usuario
    await update.message.reply_text(resumen)

    # Guardar el formulario en el archivo JSON
    formularios = cargar_formularios()
    formulario_id = f"{id_carro}_{context.user_data.get('fecha')}_{context.user_data.get('hora_completa')}"
    formularios[formulario_id] = context.user_data
    guardar_formularios(formularios)

    # Enviar resumen al grupo
    grupo_id = -1002459560918
    await context.bot.send_message(chat_id=grupo_id, text=resumen)

    return ConversationHandler.END

# Función para cancelar
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Formulario cancelado.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Configuración del bot
def main():
    application = Application.builder().token("7915698639:AAGvT0Ouwth1AYAN6oC98u_fJa8O1lL2h7w").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ID_CARRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, id_carro)],
            CONDICION: [MessageHandler(filters.TEXT & ~filters.COMMAND, condicion)],
            TIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, tipo)],
            FECHA: [MessageHandler(filters.TEXT & ~filters.COMMAND, fecha)],
            HORA: [MessageHandler(filters.TEXT & ~filters.COMMAND, hora)],
            AM_PM: [MessageHandler(filters.TEXT & ~filters.COMMAND, am_pm)],
            IMPORTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, importe)],
            CONDUCTOR1: [MessageHandler(filters.TEXT & ~filters.COMMAND, conductor1)],
            CONDUCTOR2: [MessageHandler(filters.TEXT & ~filters.COMMAND, conductor2)],
            OBSERVACION: [MessageHandler(filters.TEXT & ~filters.COMMAND, observacion)],
            TONELADAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, toneladas)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

# Ejecución principal
if __name__ == '__main__':
    main()