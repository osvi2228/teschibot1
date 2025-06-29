from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import unicodedata
import re
import difflib
import random

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto.strip()

faq_respuestas = {
    "qué es el vandalismo": "El vandalismo es cualquier daño intencional a las instalaciones, objetos o espacios públicos. En el TESChI afecta el ambiente de estudio y perjudica a toda la comunidad.",
    "qué se considera vandalismo": "Rayar paredes, romper mobiliario, dañar pizarras, desconectar equipos o destruir material escolar son actos de vandalismo en el TESChI.",
    "por qué el vandalismo es un problema": "Porque impide que se aprovechen los espacios de forma adecuada, genera gastos innecesarios y afecta la convivencia y el respeto.",
    "tipos de vandalismo": "Físico, verbal, tecnológico y ambiental. Todos dañan el entorno escolar de distintas formas.",
    "diferencia entre vandalismo y accidente": "El vandalismo es intencional. Un accidente ocurre sin intención de causar daño.",
    "daños comunes": "Pupitres rotos, puertas forzadas, paredes rayadas, proyectores dañados y basura acumulada son algunos ejemplos comunes en los salones.",
    "cómo evitar el vandalismo": "Cuida los objetos, reporta daños, promueve el respeto y da buen ejemplo. Todos somos responsables del espacio.",
    "medidas para prevenir vandalismo": "Vigilancia, cámaras, campañas de concientización, reglamento interno y colaboración de alumnos y docentes.",
    "qué hacer si veo vandalismo": "Aléjate y reporta de inmediato a un docente, al equipo de seguridad o a través del bot si es posible.",
    "rol de alumnos": "Ser conscientes del valor de los recursos, reportar incidentes y actuar con responsabilidad.",
    "cómo promover el cuidado": "Habla con tus compañeros, organiza campañas, y actúa con respeto. El cambio empieza contigo.",
    "actitudes que previenen vandalismo": "Respeto, empatía, responsabilidad y participación activa.",
    "dónde reportar vandalismo": "Puedes reportarlo a un docente, al departamento de seguridad, o usar este bot si permite reportes.",
    "a quién aviso": "Informa a un maestro, prefecto o al personal de vigilancia más cercano.",
    "denunciar anónimamente": "Sí, puedes denunciar sin dar tu nombre. Lo importante es reportar para detener el daño.",
    "qué pasa después de reportar": "Se revisa el caso, se investiga y se aplican medidas según el reglamento.",
    "el bot recibe reportes": "Sí, puedes escribir lo que viste y se enviará a las autoridades correspondientes.",
    "información para reportar": "Lugar del incidente, qué ocurrió, hora aproximada y si hay testigos o evidencia.",
    "falsa denuncia": "Las denuncias falsas tienen consecuencias, ya que afectan a personas inocentes.",
    "sanciones por vandalismo": "Las sanciones pueden ir desde advertencias y suspensiones hasta expulsión, según la gravedad del caso.",
    "qué hace seguridad": "El personal de seguridad verifica la situación, identifica a los responsables y genera un informe.",
    "qué pasa si un salón queda dañado": "Se reporta, se restringe su uso y se repara. A veces los responsables deben cubrir los costos.",
    "se llama a los padres": "Sí, en casos graves se informa a los padres o tutores y se trabaja con ellos.",
    "reparar daño para evitar sanciones": "En algunos casos sí, si hay reconocimiento del error y colaboración.",
    "reglamento del teschi": "El reglamento interno prohíbe el vandalismo y establece sanciones proporcionales a la falta.",
    "dónde está seguridad": "El departamento de seguridad se encuentra generalmente cerca de la entrada principal.",
    "quién me puede ayudar": "Tu tutor, prefecto, jefe de carrera o el coordinador de disciplina pueden ayudarte.",
    "horario del personal de vigilancia": "Están presentes durante el horario escolar. Siempre hay al menos un guardia.",
    "nadie responde al momento": "Puedes reportarlo más tarde o usar el bot si permite dejar reportes fuera de horario.",
    "ver cámaras de seguridad": "El acceso a grabaciones lo tiene solo el personal autorizado. Si hiciste un reporte, será revisado.",
    "qué hace este bot": "Responde dudas sobre vandalismo, orienta sobre cómo reportar, y ayuda a actuar con responsabilidad.",
    "el bot me ayuda a reportar": "Sí, puedes describir lo que viste y se canalizará con las autoridades.",
    "el bot guarda lo que escribo": "La información puede almacenarse para seguimiento, pero se mantiene confidencial.",
    "es seguro usar el bot": "Sí. Tu privacidad está protegida. No se compartirá tu identidad sin motivo.",
    "puedo escribir en cualquier momento": "Sí, el bot está disponible 24/7. El seguimiento puede hacerse durante el horario escolar."
}

faq_palabras_clave = {
    "qué es el vandalismo": [
        "vandalismo", "significa", "significado", "definición", "se entiende", "se llama",
        "quiere decir", "se define", "considera",
    ],
    "qué se considera vandalismo": [
        "actos", "conductas", "acciones", "comportamiento", "ejemplos",
        "implica", "clasifica", "considera", "tipo", "categoria", "vandalismo",
        "cometer", "acto", "vandalico", "vandálico"
    ],
    "por qué el vandalismo es un problema": [
        "problema", "causa", "impacto", "afecta", "negativo",
        "consecuencia", "conflicto", "evitar"
    ],
    "tipos de vandalismo": [
        "tipos", "clases", "formas", "categorias", "modalidades", "variedades",
        "clasificación", "clasificar"
    ],
    "diferencia entre vandalismo y accidente": [
        "diferencia", "distinto", "caracteriza", "identificar",
        "distinguir", "comparacion", "vandalismo", "accidente"
    ],
    "daños comunes": [
        "daños", "comunes", "frecuentes", "habituales", "tipos", "normales",
        "típicos"
    ],
    "cómo evitar el vandalismo": [
        "evitar", "prevenir", "medidas", "acciones", "estrategias", "controlar",
        "métodos", "formas"
    ],
    "medidas para prevenir vandalismo": [
        "medidas", "prevenir", "acciones", "estrategias", "métodos", "precauciones",
        "controlar", "formas"
    ],
    "qué hacer si veo vandalismo": [
        "ver", "viendo", "presenciar", "actuar", "pasos", "testigo",
        "avisar", "acciones", "proceder"
    ],
    "rol de alumnos": [
        "rol", "papel", "funcion", "responsabilidades", "deberes", "importancia",
        "espera", "cumplen", "actuar", "clase"
    ],
    "cómo promover el cuidado": [
        "promover", "fomentar", "acciones", "estrategias", "motivar", "conciencia",
        "incentivar", "generar", "pasos", "hábitos", "comunidad"
    ],
    "actitudes que previenen vandalismo": [
        "actitudes", "comportamientos", "formas", "valores", "hábitos",
        "mentalidad", "previenen", "evitan", "reducir", "contribuyen"
    ],
    "dónde reportar vandalismo": [
        "donde", "lugar", "denunciar", "reportar", "informar", "reporte",
        "autoridad", "a quien", "debo", "hacer"
    ],
    "a quién aviso": [
        "quien", "avisar", "reporto", "informar", "llamar", "comunicar",
        "notificar", "emergencia"
    ],
    "denunciar anónimamente": [
        "anónima", "anónimamente", "sin nombre", "sin revelar", "identidad",
        "opciones", "funciona", "puedo", "seguro"
    ],
    "qué pasa después de reportar": [
        "pasa", "ocurre", "después", "tras", "proceso", "pasos", "acciones",
        "sucede", "continúa"
    ],
    "el bot recibe reportes": [
        "bot", "recibe", "reportes", "denuncias", "acepta", "envía",
        "diseñado", "funciona", "procesa"
    ],
    "información para reportar": [
        "información", "datos", "necesito", "proporcionar", "incluir",
        "hacer", "completar", "enviar", "obtener"
    ],
    "falsa denuncia": [
        "falsa", "mentira", "acusación", "no fue cierto"
    ],
    "sanciones por vandalismo": [
        "sanciones", "castigo", "consecuencias", "pena", "aplica",
        "legales", "sanciona", "tipo", "reciben"
    ],
    "qué hace seguridad": [
        "seguridad", "funcion", "tareas", "responsabilidades",
        "acciones", "actúa", "papel", "trabajo", "medidas", "equipo"
    ],
    "qué pasa si un salón queda dañado": [
        "salón", "dañado", "daño", "resultado", "consecuencias",
        "medidas", "acciones", "procedimiento", "autoridades", "respuesta"
    ],
    "se llama a los padres": [
        "padres", "llamar", "contactar", "informar", "avisar",
        "notificar", "obligatorio", "situaciones", "incidente"
    ],
    "reparar daño para evitar sanciones": [
        "reparar", "daño", "evitar", "sanciones", "castigos",
        "opciones", "colaboración", "reconocimiento"
    ],
    "reglamento del teschi": [
        "reglamento", "teschi", "reglas", "normas", "contenido", "sanciones",
        "disponible", "cumplir"
    ],
    "dónde está seguridad": [
        "dónde", "seguridad", "personal", "oficina", "puesto", "caseta",
        "equipo", "guardia", "localizar", "encontrar"
    ],
    "quién me puede ayudar": [
        "quién", "ayudar", "apoyo", "asistir", "orientar", "acudir",
        "disponible", "pedir", "encargado"
    ],
    "horario del personal de vigilancia": [
        "horario", "vigilancia", "turno", "trabaja", "horas",
        "equipo", "inicia", "termina", "cubrir", "servicio"
    ],
    "nadie responde al momento": [
        "nadie", "respuesta", "contestan", "disponible", "atención",
        "momento", "instante"
    ],
    "ver cámaras de seguridad": [
        "cámaras", "seguridad", "ver", "acceder", "grabaciones",
        "en vivo", "mostrar", "revisar", "acceso", "visualizar",
        "monitorear", "consultar", "imágenes"
    ],
    "qué hace este bot": [
        "bot", "funcion", "uso"
    ],
    "el bot me ayuda a reportar": [
        "reportar", "ayuda", "denunciar", "apoyo"
    ],
    "el bot guarda lo que escribo": [
        "guarda", "almacena", "registra", "confidencial"
    ],
    "es seguro usar el bot": [
        "seguro", "privacidad", "confidencial"
    ],
    "puedo escribir en cualquier momento": [
        "momento", "hora", "cuando", "disponible"
    ]
}

respuestas_genericas = [
    "¡Interesante! ¿Puedes decirme más sobre eso?",
    "No estoy seguro, ¿puedes darme más detalles?",
    "Esa es una buena pregunta. Intentaré ayudarte, ¿puedes ser más específico?",
    "¿Podrías aclarar un poco más tu duda para poder ayudarte mejor?",
    "¡Cuéntame más! Estoy aquí para ayudarte con temas de vandalismo y convivencia."
]

def pregunta_mas_parecida(mensaje, preguntas):
    mensaje = normalizar_texto(mensaje)
    mejor_pregunta = None
    mayor_similitud = 0
    for pregunta in preguntas:
        similitud = difflib.SequenceMatcher(None, mensaje, normalizar_texto(pregunta)).ratio()
        if similitud > mayor_similitud:
            mayor_similitud = similitud
            mejor_pregunta = pregunta
    return mejor_pregunta if mayor_similitud > 0.6 else None

def sugerencias_similares(mensaje):
    sugerencias = []
    for pregunta, palabras in faq_palabras_clave.items():
        if any(palabra in mensaje for palabra in palabras):
            sugerencias.append(pregunta)
    return sugerencias[:3]

def registrar_reporte(usuario, mensaje):
    import datetime
    with open("reportes.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.datetime.now()} - {usuario}: {mensaje}\n")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola, soy el bot contra el vandalismo del TESChi.\n"
        "Puedes preguntarme sobre vandalismo, prevención, sanciones o cómo reportar un caso.\n"
        "Si quieres reportar un incidente, solo dime 'quiero reportar' o 'denunciar'.\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ejemplos de preguntas que puedes hacerme:\n"
        "- ¿Qué es el vandalismo?\n"
        "- ¿Dónde lo reporto?\n"
        "- ¿Qué sanciones existen?\n"
        "- ¿Cómo lo puedo evitar?\n"
        "- Quiero denunciar un caso\n"
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = normalizar_texto(update.message.text)
    usuario = update.message.from_user.username or "usuario_desconocido"

    
    if context.user_data.get("reportando", False):
        if not context.user_data.get("lugar_preguntado", False):
            context.user_data["descripcion"] = mensaje
            context.user_data["lugar_preguntado"] = True
            await update.message.reply_text("¿En qué lugar ocurrió el incidente?")
            return
        else:
            context.user_data["lugar"] = mensaje
            descripcion = context.user_data.get("descripcion", "")
            lugar = context.user_data.get("lugar", "")
            registrar_reporte(usuario, f"Reporte de vandalismo: {descripcion} | Lugar: {lugar}")
            await update.message.reply_text(
                "¡Gracias! Tu reporte ha sido registrado y será canalizado con las autoridades correspondientes. Si tienes más detalles, házmelo saber."
            )
            context.user_data.clear()
            return

    
    if ("reportar" in mensaje or "denunciar" in mensaje) and not context.user_data.get("reportando", False):
        context.user_data["reportando"] = True
        context.user_data["lugar_preguntado"] = False
        await update.message.reply_text("Por favor describe brevemente lo que ocurrió.")
        return

    
    pregunta = pregunta_mas_parecida(mensaje, faq_respuestas.keys())
    if pregunta:
        await update.message.reply_text(faq_respuestas[pregunta])
        return

    
    sugerencias = sugerencias_similares(mensaje)
    if sugerencias:
        await update.message.reply_text("¿Quizás te refieres a:\n- " + "\n- ".join(sugerencias))
        return

    
    await update.message.reply_text(random.choice(respuestas_genericas))

TOKEN = "7827661487:AAGxLxS6-CCs_14uGwtfIJz1SQGeqLwUxrs"

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("El bot está en funcionamiento")
    app.run_polling()

if __name__ == '__main__':
    main()