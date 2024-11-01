import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
import asyncio
import unicodedata

# Set Intents
intents = discord.Intents.all()
intents.guilds = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

ANNOUNCEMENTS_CHANNEL_ID = int(os.getenv("ANNOUNCEMENTS_CHANNEL"))  # ID announcements channel
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL"))  # ID vocal channel

# Recipes list (min 8 ingredients)
recipes = {
    "Spaghetti alla Carbonara": ["spaghetti", "guanciale", "uova", "pecorino", "pepe nero", "sale", "olio", "parmigiano"],
    "Lasagna al Ragù": ["lasagne", "carne macinata", "passata di pomodoro", "cipolla", "carota", "sedano", "besciamella", "parmigiano"],
    "Risotto alla Milanese": ["riso", "zafferano", "burro", "brodo di carne", "cipolla", "vino bianco", "parmigiano", "sale"],
    "Tiramisù": ["savoiardi", "mascarpone", "caffè", "uova", "zucchero", "cacao amaro", "rum", "cioccolato"],
    "Pizza Margherita": ["farina", "acqua", "lievito", "pomodoro", "mozzarella", "basilico", "olio", "sale"],
    "Pasta al Pesto": ["pasta", "basilico", "pinoli", "aglio", "parmigiano", "pecorino", "olio", "sale"],
    "Arancini di Riso": ["riso", "carne macinata", "piselli", "mozzarella", "farina", "uova", "pangrattato", "olio per friggere"],
    "Ossobuco alla Milanese": ["ossobuco", "burro", "brodo di carne", "cipolla", "vino bianco", "prezzemolo", "limone", "sale"],
    "Parmigiana di Melanzane": ["melanzane", "pomodoro", "mozzarella", "parmigiano", "basilico", "farina", "uova", "olio"],
    "Cannelloni Ricotta e Spinaci": ["cannelloni", "ricotta", "spinaci", "parmigiano", "mozzarella", "noce moscata", "burro", "sale"],
    "Ragù alla Bolognese": ["carne macinata", "pomodoro", "carota", "cipolla", "sedano", "olio", "vino rosso", "sale"],
    "Polpette al Sugo": ["carne macinata", "pane", "latte", "parmigiano", "uovo", "prezzemolo", "aglio", "sugo di pomodoro"],
    "Gnocchi alla Sorrentina": ["gnocchi", "mozzarella", "pomodoro", "parmigiano", "basilico", "olio", "aglio", "sale"],
    "Pasta alla Norma": ["pasta", "melanzane", "pomodoro", "ricotta salata", "basilico", "olio", "aglio", "sale"],
    "Saltimbocca alla Romana": ["fettine di vitello", "prosciutto crudo", "salvia", "burro", "vino bianco", "sale", "pepe", "olio"],
    "Risotto ai Funghi": ["riso", "funghi porcini", "cipolla", "vino bianco", "brodo", "parmigiano", "burro", "prezzemolo"],
    "Pasta e Fagioli": ["pasta", "fagioli", "cipolla", "carota", "sedano", "pomodoro", "olio", "sale"],
    "Polenta e Salsiccia": ["polenta", "salsiccia", "passata di pomodoro", "cipolla", "aglio", "vino rosso", "sale", "olio"],
    "Penne all'Arrabbiata": ["penne", "pomodoro", "peperoncino", "aglio", "olio", "prezzemolo", "sale", "pepe"],
    "Caponata Siciliana": ["melanzane", "pomodoro", "sedano", "cipolla", "olive", "capperi", "aceto", "zucchero"],
    "Vitello Tonnato": ["fettine di vitello", "tonno", "maionese", "capperi", "acciughe", "limone", "prezzemolo", "olio"],
    "Pasta al Forno": ["pasta", "ragù", "mozzarella", "parmigiano", "besciamella", "olio", "sale", "pepe"],
    "Zuppa di Pesce": ["pesce misto", "pomodoro", "aglio", "prezzemolo", "vino bianco", "olio", "sale", "pepe"],
    "Bucatini all'Amatriciana": ["bucatini", "guanciale", "pomodoro", "pecorino", "pepe nero", "sale", "olio", "vino bianco"],
    "Frittata di Patate": ["uova", "patate", "cipolla", "parmigiano", "olio", "sale", "pepe", "prezzemolo"],
    "Involtini di Melanzane": ["melanzane", "mozzarella", "prosciutto cotto", "parmigiano", "pomodoro", "basilico", "olio", "sale"],
    "Minestrone di Verdure": ["zucchine", "carote", "sedano", "pomodori", "patate", "fagioli", "cipolla", "olio"],
    "Stracciatella alla Romana": ["brodo di carne", "uova", "parmigiano", "noce moscata", "sale", "pepe", "prezzemolo", "olio"],
    "Scaloppine al Limone": ["fettine di vitello", "limone", "burro", "farina", "sale", "pepe", "prezzemolo", "olio"],
    "Baccalà alla Livornese": ["baccalà", "pomodoro", "cipolla", "aglio", "prezzemolo", "vino bianco", "olio", "sale"],
    "Zuppa di Lenticchie": ["lenticchie", "cipolla", "carota", "sedano", "pomodoro", "olio", "sale", "pepe"],
    "Calamari Ripieni": ["calamari", "pangrattato", "parmigiano", "prezzemolo", "aglio", "pomodoro", "olio", "sale"],
    "Risotto agli Asparagi": ["riso", "asparagi", "cipolla", "vino bianco", "brodo", "parmigiano", "burro", "sale"],
    "Cacciucco alla Livornese": ["polpo", "seppie", "pomodoro", "aglio", "peperoncino", "vino rosso", "pane", "olio"],
    "Ravioli Ricotta e Spinaci": ["ravioli", "ricotta", "spinaci", "parmigiano", "burro", "noce moscata", "sale", "pepe"],
    "Cozze alla Tarantina": ["cozze", "pomodoro", "aglio", "prezzemolo", "peperoncino", "vino bianco", "olio", "sale"],
    "Sarde a Beccafico": ["sarde", "pangrattato", "pinoli", "uvetta", "aglio", "prezzemolo", "olio", "sale"],
    "Linguine allo Scoglio": ["linguine", "cozze", "vongole", "pomodoro", "aglio", "prezzemolo", "olio", "vino bianco"],
    "Pasta con le Sarde": ["pasta", "sarde", "finocchietto", "uvetta", "pinoli", "pomodoro", "olio", "cipolla"],
    "Pasta al Sugo di Cozze": ["pasta", "cozze", "pomodoro", "aglio", "prezzemolo", "peperoncino", "olio", "sale"],
    "Pasta alla Puttanesca": ["pasta", "pomodoro", "olive", "capperi", "acciughe", "aglio", "prezzemolo", "olio"],
    "Tagliatelle ai Funghi": ["tagliatelle", "funghi porcini", "aglio", "prezzemolo", "olio", "vino bianco", "parmigiano", "sale"],
    "Insalata di Polpo": ["polpo", "patate", "sedano", "olio", "limone", "sale", "prezzemolo", "pepe"],
    "Pollo alla Cacciatora": ["pollo", "pomodoro", "cipolla", "carota", "sedano", "olio", "vino rosso", "rosmarino"]
}

MESSAGGI_RIMOZIONE = [
    "Oops! 🎩 Sembra che il tuo nickname non sia tra gli ingredienti della ricetta segreta! Riprova con un nome più saporito. 😉",
    "Ehi, chef! 👨‍🍳 Purtroppo il tuo nome non è un ingrediente del piatto del giorno! Torna con un nome più speziato e riprova. 🌶️",
    "Nome non in lista, niente party! 🕺 Riprova con un nome che ci faccia venire fame. 🍕",
    "Ops, stai cercando di entrare nella cucina sbagliata! 🍲 Cambia nome e torna con qualcosa di più… gustoso! 🍔",
    "Nome non riconosciuto! 🚫 Solo gli ingredienti giusti possono entrare qui. Torna con un nome che sappia di buono! 🍞",
    "Come direbbe uno chef stellato: 'Il tuo nome? Non è al dente!' Prova un altro ingrediente per entrare. 🍝",
    "Avviso dalla cucina: senza un nome da ingrediente, niente accesso al tavolo VIP! 🍽️",
    "Oh no! Sembra che il tuo nickname non sia tra quelli da chef… prova con un nome più saporito! 🍲",
    "Hey, non puoi entrare senza la password… cioè, l’ingrediente giusto! 🔒",
    "Nella nostra cucina, solo ingredienti selezionati! Riprova con un nickname più delizioso! 🧄",
    "Accesso negato! Solo gli ingredienti del giorno possono entrare in cucina! 🍤 Riprova, chef!",
    "Attenzione: Il tuo nome non è nella ricetta segreta! Torna con qualcosa di più… speziato. 🧂",
    "Ahia! 😬 Sei fuori dal mix! Torna con un nickname più da ingrediente, e sarai il benvenuto! 🥄",
    "Chiave d’accesso non valida! Solo ingredienti freschi ammessi. 🍋",
    "Non tutte le carote sono uguali! Scegli un nome più… cucinabile per entrare! 🥕",
    "Nome sbagliato, nessun servizio! Riprova con un nickname più… croccante! 🍟",
    "Il tuo nome non è in menu! Torna con un altro nickname per entrare. 🍿",
    "Sei stato scottato! Torna con un nome che faccia parte della ricetta e riprova! 🔥",
    "Nickname non riconosciuto! Solo gli ingredienti migliori possono entrare qui! 🥗",
    "Accesso vietato! 🛑 Hai dimenticato l’ingrediente segreto… il tuo nome! Prova un altro nickname! 🍳"
]

tentativi_utente = {}

# Variabile track recipe
current_recipe = None
current_ingredients = []

# Normalize string for accent
def normalize_string(s):
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower()

# When bot is ready
@bot.event
async def on_ready():
    print(f'Bot {bot.user} è online.')
    change_channel_name.start()  # Start daily task
    bot.loop.create_task(check_voice_channel_members())

@bot.command(name="menu")
async def cambia_nome(ctx):
    global current_recipe, current_ingredients

    # Pick random recipe
    current_recipe, current_ingredients = random.choice(list(recipes.items()))

    # Load voice channel
    guild = ctx.guild
    voice_channel = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)

    if voice_channel:
        await voice_channel.edit(name=current_recipe)
        await ctx.send(f"Il nome del canale vocale è stato cambiato in: {current_recipe}")
    else:
        await ctx.send("Canale vocale non trovato. Verifica che il bot abbia i permessi necessari.")

# Task change voice channel name
@tasks.loop(hours=24)
async def change_channel_name():
    global current_recipe, current_ingredients
    
    # Pick random recipe
    current_recipe, current_ingredients = random.choice(list(recipes.items()))
    
    # Load voice channel
    guild = bot.guilds[0]
    voice_channel = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)  # First name voice channel
    
    if voice_channel:
        # Rename voice channel
        await voice_channel.edit(name=current_recipe)
        print(f"Nome del canale cambiato in: {current_recipe}")
    else:
        print("Canale vocale non trovato.")

# Check if user nick is compliant
@bot.event
async def on_voice_state_update(member, before, after):
    # Load text chat
    text_channel = discord.utils.get(member.guild.text_channels, id=ANNOUNCEMENTS_CHANNEL_ID)

    # Use nick or name
    user_nick_or_name = member.nick if member.nick else member.name
    normalized_member_name = normalize_string(user_nick_or_name)
    
    #Check if is right channel
    if after.channel is not None and after.channel.name == current_recipe:
        # Load all user active in channel
        voice_channel = after.channel
        members_in_channel = voice_channel.members

        # Check for duplicate
        for other_member in members_in_channel:
            if other_member != member:
                other_nick_or_name = other_member.nick if other_member.nick else other_member.name
                normalized_other_name = normalize_string(other_nick_or_name)
                
                if normalized_member_name == normalized_other_name:
                    # Kick if duplicate
                    await member.move_to(None)
                    if text_channel is not None:
                        messaggio_random = random.choice(MESSAGGI_RIMOZIONE)
                        await text_channel.send(f"{member.mention} {messaggio_random}")
                    print(f"{user_nick_or_name} è stato rimosso dal canale vocale per nickname duplicato.")
                    return
        
        # Check if name is compliant
        if not any(normalize_string(ingredient) in normalized_member_name for ingredient in current_ingredients):
            await member.move_to(None)
            if text_channel is not None:
                messaggio_random = random.choice(MESSAGGI_RIMOZIONE)
                await text_channel.send(f"{member.mention} {messaggio_random}")
            print(f"{user_nick_or_name} è stato rimosso dal canale vocale perché il nickname non è pertinente.")


# Check every 60 seconds
async def check_voice_channel_members():
    await bot.wait_until_ready()  # Is bot ready?
    while not bot.is_closed():
        try:
            guild = bot.guilds[0]
            if guild is None:
                print("Gilda non trovata.")
                await asyncio.sleep(60)
                continue

            # Load channel with recipe or None
            voice_channel = discord.utils.get(guild.voice_channels, name=current_recipe)
            if voice_channel is None:
                print(f"Canale vocale '{current_recipe}' non trovato.")
                await asyncio.sleep(60)
                continue

            # Load text chat
            text_channel = discord.utils.get(guild.text_channels, id=ANNOUNCEMENTS_CHANNEL_ID)
            if text_channel is None:
                print("Canale di testo per notifiche non trovato.")
                await asyncio.sleep(60)
                continue

            unique_nicknames = set()

            for member in voice_channel.members:
                user_nick_or_name = member.nick if member.nick else member.name
                normalized_member_name = normalize_string(user_nick_or_name)

                if normalized_member_name in unique_nicknames:
                    await member.move_to(None)
                    messaggio_random = random.choice(MESSAGGI_RIMOZIONE)
                    await text_channel.send(f"{member.mention} {messaggio_random}")
                    continue

                if not any(normalize_string(ingredient) in normalized_member_name for ingredient in current_ingredients):
                    await member.move_to(None)
                    messaggio_random = random.choice(MESSAGGI_RIMOZIONE)
                    await text_channel.send(f"{member.mention} {messaggio_random}")
                    continue

                unique_nicknames.add(normalized_member_name)

            print("Controllo completato.")
        
        except Exception as e:
            print(f"Errore durante l'esecuzione di check_voice_channel_members: {e}")

        await asyncio.sleep(60)

@change_channel_name.before_loop
async def before_change_channel_name():
    await bot.wait_until_ready()
    await asyncio.sleep(5)  # Add delay to be sure it is ready

# Run bot
bot.run(os.getenv("KEY"))