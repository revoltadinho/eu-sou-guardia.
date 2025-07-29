import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Carregar variáveis do ambiente
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Verificação básica de segurança
if BOT_TOKEN is None:
    raise ValueError("Erro: A variável BOT_TOKEN não está definida.")
if ADMIN_ID is None:
    raise ValueError("Erro: A variável ADMIN_ID não está definida.")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Eu sou o RevoltadinhoBot. Pronto para revoluções. 💥")

# Comando secreto só para o admin
async def segredo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == ADMIN_ID:
        await update.message.reply_text("⚠️ Acesso concedido ao painel secreto.")
    else:
        await update.message.reply_text("🚫 Acesso negado.")

# Inicializar a aplicação do bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Adicionar comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("segredo", segredo))

# Iniciar polling
app.run_polling()

  
