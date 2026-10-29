import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Définit les intents nécessaires pour le bot
# Pour les intents privilégiés (members, message_content), assurez-vous de les avoir activés sur le portail développeur.
intents = discord.Intents.default()
intents.members = True # Nécessaire pour accéder aux informations des membres
intents.message_content = True # Nécessaire pour lire le contenu des messages
intents.presences = True # Nécessaire pour connaître le statut des membres

IGNORED_CHANNELS = [
    "690562112795312198",
    "1389951627787768020"
]

# Définit le préfixe des commandes (par exemple, "!ping" pour appeler la commande "ping")
bot = commands.Bot(command_prefix="!", intents=intents)

# Événement lorsque le bot est prêt et connecté à Discord
@bot.event
async def on_ready():
    print(f'{bot.user} est connecté à Discord!')
    # Vous pouvez envoyer un message à un salon spécifique quand le bot est en ligne
    # Remplacez 'NOM_DU_SALON' par le nom du salon où vous voulez envoyer le message
    # Ou utilisez l'ID du salon pour plus de fiabilité : channel = bot.get_channel(ID_DU_SALON)
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if "tests-bot" in channel.name.lower(): # Cherche un salon nommé "tests-bot"
                print(f"Salon 'tests-bot' trouvé dans {guild.name}")
                # await channel.send(f'Salut les gars ! {bot.user} est en ligne !')
                break # Une fois trouvé, on sort
        else:
            print(f"Aucun salon 'tests-bot' trouvé sur le serveur {guild.name}")

@bot.event
async def on_message(message):
    # Important : Ignore les messages envoyés par le bot lui-même pour éviter les boucles infinies
    if message.author == bot.user:
        return
    assert type(message) is discord.Message  # Assure que le message est bien de type discord.Message

    ignored = str(message.channel.id) in IGNORED_CHANNELS

    # Convertit le contenu du message en minuscules pour une détection insensible à la casse
    message_content = message.content.strip()  # Enlève les espaces superflus au début et à la fin
    message_content_lower = message.content.lower()
    message_emitter = message.author.name.lower() if message.author else "inconnu"

    # Vérifie si "quoi" est présent dans le message
    if not ignored:
        if "quoi" in message_content_lower:
            if random.randint(1, 5) <= 4:  # 80% de chance de répondre "feur."
                await message.reply(f"feur.", mention_author=False)
            elif random.choice([False, True]):  # 10% de chance de répondre "coubeh."
                await message.reply(f"coubeh.", mention_author=False)
            else:  # 10% de chance de répondre par un GIF feur
                await message.reply("https://tenor.com/bN6ju.gif", mention_author=False)
        elif "qui" in message_content_lower and "?" in message_content_lower:
            gifs = [
                "https://tenor.com/bz5cI.gif",
                "https://tenor.com/beZPA.gif",
                "https://tenor.com/SYpl.gif",
                "https://tenor.com/bFazm.gif"
            ]
            await message.reply(random.choice(gifs), mention_author=False)
        elif "faim" in message_content_lower or "mange" in message_content_lower or "bouffe" in message_content_lower or "la dalle" in message_content_lower:
            gifs = [
                "https://tenor.com/bnEBD.gif"
            ]
            await message.reply(random.choice(gifs), mention_author=False)
        elif message.guild.me.display_name.lower() in message_content_lower or bot.user.mention in message_content_lower:
            # Si le bot est mentionné ou son nom est utilisé, il répondra
            await message.reply(f"C'est moi ^^", mention_author=False)
        elif message.mention_everyone:
            gifs = [
                "https://tenor.com/bqyGy.gif",
                "https://cdn3.emoji.gg/emojis/4879-pepe-ateveryoneping.gif"
            ]
            await message.reply(random.choice(gifs), mention_author=False)
    
    if "bite" in message_content_lower or "zizi" in message_content_lower or "queue" in message_content_lower or "couille" in message_content_lower:
        await message.add_reaction("🍆")  # Ajoute une réaction aubergine si "bite" est mentionné
    
    # if message_emitter == "romain_3251" and message_content.startswith(".botsay "):
    #     # Si le message commence par ".say ", le bot répète le reste du message et supprime le message original
    #     await message.delete()
    #     try:
    #         content_to_repeat = message_content[message_content.index("|")+1:]
    #         if content_to_repeat:
    #             if message.channel_mentions:
    #                 # Si le message mentionne un salon, envoie le message dans ce salon
    #                 channel = message.channel_mentions[0]
    #                 await channel.send(content_to_repeat)
    #             else:
    #                 # Sinon, envoie le message dans le même salon
    #                 await message.channel.send(content_to_repeat)
    #     except ValueError:
    #         content_to_repeat = message_content[8:]
    #         await message.channel.send(content_to_repeat)
    

    # Très important : Permet aux commandes (comme !ping, !salut) de continuer à fonctionner
    await bot.process_commands(message)

# on message_edit pour répondre aux modifications de message
@bot.event
async def on_message_edit(before, after):
    """Répond aux modifications de message."""
    # Ignore les messages du bot lui-même
    if before.author == bot.user:
        return

    assert type(before) is discord.Message  # Assure que le message avant modification est bien de type discord.Message
    assert type(after) is discord.Message  # Assure que le message après modification est bien de type discord.Message

    await after.add_reaction("👀")


# Commande simple : !ping
@bot.command(name="ping")
async def ping(ctx):
    """Répond avec 'Pong!' lorsque la commande !ping est appelée."""
    await ctx.send("Pong!")

# Commande pour saluer un utilisateur
@bot.command(name="salut")
async def salut(ctx):
    """Répond avec un message de salutation."""
    await ctx.send(f"Salut, {ctx.author.display_name} !")

# Commande pour donner l'heure actuelle
import datetime
@bot.command(name="heure")
async def heure(ctx):
    """Affiche l'heure actuelle."""
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    await ctx.send(f"Il est actuellement {current_time}.")

# Commande pour lancer des dés (entrées : nombre de dés et nombre de faces)
@bot.command(name="lancer_des")
async def lancer_des(ctx, nombre_de_des: int = 1, nombre_de_faces: int = 6):
    """Lance un certain nombre de dés avec un nombre de faces spécifié. 
    Par défaut, lance 1 dé à 6 faces. 
    Usage : !lancer_des <nombre_de_des> <nombre_de_faces>"""
    if nombre_de_des < 1:
        await ctx.send("Veuillez entrer un nombre valide de dés (>= 1)")
        return
    if nombre_de_faces < 2:
        await ctx.send("Veuillez entrer un nombre valide de faces (>= 2)")
        return

    resultats = [random.randint(1, nombre_de_faces) for _ in range(nombre_de_des)]
    await ctx.send(f"Résultats du lancer de {nombre_de_des} dé{"s" if nombre_de_des>1 else ""} à {nombre_de_faces} faces : {sum(resultats)}")

@bot.command(name="rizz")
async def rizz(ctx, *, user: discord.Member = None):
    """Fait un compliment à un utilisateur ou à soi-même.
    Si aucun utilisateur n'est mentionné, le compliment est fait à l'auteur du message.
    Usage : !rizz @utilisateur"""
    if user is None:
        user = ctx.author
    
    compliments = [
        "Ton père est un voleur, il a volé toutes les étoiles du ciel pour faire briller tes yeux.",
        "Si la beauté était un crime, tu serais en prison à vie.",
        "Excuse-moi, tu n'aurais pas l'heure ? Parce que quand je te vois, j'arrête le temps.",
        "Tes parents sont des as du jardinage, pas vrai ? Parce qu'ils ont réussi à faire pousser une fleur comme toi.",
        "Si j'avais un euro pour chaque fois que je pense à toi... bah j'aurais un euro, parce que je ne pense qu'à toi."
    ]

    compliment = random.choice(compliments)
    await ctx.send(f"{user.mention}, {compliment}")

@bot.command(name="anti_rizz")
async def anti_rizz(ctx, *, user: discord.Member = None):
    """Fait une blague à un utilisateur ou à soi-même.
    Si aucun utilisateur n'est mentionné, la blague est faite à l'auteur du message.
    Usage : !anti_rizz @utilisateur"""
    if user is None:
        user = ctx.author
    
    blagues = [
        "J'ai cru qu'il y avait un tremblement de terre, mais en fait c'était juste toi qui marchais.",
        "Ton père c'est pas un voleur ? Parce qu'il me doit 20 balles c't'enculé.",
        "Si la beauté était un crime, tu serais en prison. Mais pas à cause de ta beauté, juste parce que t'as attouché des mineures.",
        "Si j'avais un euro pour chaque fois que je pense à toi... bah je serai endetté."
    ]

    blague = random.choice(blagues)
    await ctx.send(f"{user.mention}, {blague}")

@bot.command(name="ta_mere")
async def ta_mere(ctx, *, user: discord.Member = None):
    """Fait une blague sur la mère d'un utilisateur ou à soi-même.
    Si aucun utilisateur n'est mentionné, la blague est faite à l'auteur du message.
    Usage : !ta_mere @utilisateur"""
    if user is None:
        user = ctx.author
    
    blagues_mere = [
        "Ta mère elle est tellement grosse qu'il y a un décalage horaire entre ses deux fesses.",
        "Ta mère elle est tellement grosse que quand elle se pèse il y a son numéro de téléphone qui s'affiche.",
        'Ta mère elle est tellement grosse que quand elle laisse traîner son string on demande "Qui a laissé traîner sa corde à sauter ?".',
        "Ta mère elle est tellement conne qu'elle croit que cunnilingus c'est un nuage.",
        "Ta mère c'est comme un caddie, une pièce est c'est reparti.",
        "Ta mère c'est comme la tour Eiffel, elle attire les touristes.",
        "Ta mère c'est comme un barbecue, on y met tous sa saucisse.",
        "Ta mère c'est comme un vampire, le jour elle dort, la nuit elle suce."
    ]

    blague_mere = random.choice(blagues_mere)
    await ctx.send(f"{user.mention}, {blague_mere}")

@bot.command(name="troll")
async def troll(ctx):
    """Envoie un GIF troll"""
    gifs_troll = [
        "https://tenor.com/6IPU.gif",
        "https://cdn.discordapp.com/attachments/1117046520487886898/1224384641407123548/IMG_1169.gif?ex=6835de8e&is=68348d0e&hm=e0b74d817f02b9e99410c6ab3af29477bf58eb691178a8c2210a923e1e17246b",
        "https://tenor.com/bXTQx.gif",
        "https://tenor.com/rRqKKcTsgmS.gif",
        "https://tenor.com/oKox3E4WHIc.gif"
    
    ]

    gif = random.choice(gifs_troll)
    await ctx.send(gif)

@bot.command(name="suggestion")
async def suggestion(ctx, *, suggestion_text: str):
    """Permet aux utilisateurs de soumettre des suggestions pour le bot.
    Usage : !suggestion <votre suggestion>"""
    if not suggestion_text:
        await ctx.send("Veuillez fournir une suggestion.")
    else:
        await ctx.send(f"Merci pour votre suggestion : `{suggestion_text}`\nNous l'examinerons bientôt !")

# Commande pour afficher les informations du bot
@bot.command(name="info")
async def info(ctx):
    """Affiche des informations sur le bot."""
    embed = discord.Embed(title="Informations sur le Bot", description="Voici quelques informations sur ce bot.", color=discord.Color.blue())
    embed.add_field(name="Nom", value=bot.user.name, inline=True)
    embed.add_field(name="ID", value=bot.user.id, inline=True)
    embed.add_field(name="Version", value="1.0.0", inline=False)
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else "")
    await ctx.send(embed=embed)

# Commande pour afficher la liste des commandes disponibles
@bot.command(name="aide")
async def aide(ctx):
    """Affiche la liste des commandes disponibles."""
    embed = discord.Embed(title="Aide du Bot", description="Voici la liste des commandes disponibles :", color=discord.Color.green())
    commands_list = [f"{bot.command_prefix}{command.name} - {command.help}\n" for command in bot.commands if not command.hidden]
    embed.add_field(name="Commandes", value="\n".join(commands_list), inline=False)
    await ctx.send("\n".join(commands_list))

@bot.command(name="sendto", help="[ADMIN] Envoie un message dans un salon spécifique par son ID. Usage: !sendto <ID_SALON> <message>", hidden=True)
@commands.is_owner() # CLÉ : Seul le propriétaire du bot peut utiliser cette commande
async def send_message_to_channel(ctx, channel_id: int, *, message_content: str):
    """
    Permet d'envoyer un message à un salon spécifique par son ID.
    Seul le propriétaire du bot peut l'utiliser.
    """
    try:
        # Récupère le salon par son ID
        # bot.get_channel est rapide mais ne trouve que les salons en cache.
        # bot.fetch_channel ferait une requête API mais est plus lent.
        # Pour une commande admin, get_channel est souvent suffisant ou on peut le combiner.
        target_channel = bot.get_channel(channel_id)

        if not target_channel:
            # Tente de fetch le canal s'il n'est pas en cache
            target_channel = await bot.fetch_channel(channel_id)
            
        if not target_channel:
            await ctx.send(f"Erreur : Salon avec l'ID {channel_id} introuvable.")
            return

        # Vérifie que c'est un salon textuel
        if not isinstance(target_channel, discord.TextChannel):
            await ctx.send(f"Erreur : Le salon {target_channel.mention} (ID: {channel_id}) n'est pas un salon textuel.")
            return

        # Envoie le message
        await target_channel.send(message_content)
        await ctx.send(f"Message envoyé dans le salon {target_channel.mention} du serveur '{target_channel.guild.name}' !")

    except discord.NotFound:
        await ctx.send(f"Erreur : Le salon avec l'ID {channel_id} n'a pas été trouvé (il peut être supprimé ou je n'y ai pas accès).")
    except discord.Forbidden:
        await ctx.send(f"Erreur de permissions : Je n'ai pas les droits suffisants pour voir ou accéder au salon avec l'ID {channel_id}.")
    except Exception as e:
        await ctx.send(f"Une erreur inattendue est survenue : {e}")

@bot.command(name="respondto", help="[ADMIN] Répond à un message spécifique dans un salon donné. Usage: !respondto <ID_MESSAGE> <message>", hidden=True)
@commands.is_owner() # CLÉ : Seul le propriétaire du bot peut utiliser cette commande
async def respond_to_message(ctx, message_id: int, *, response_content: str):
    """
    Permet de répondre à un message spécifique par son ID.
    Seul le propriétaire du bot peut l'utiliser.
    """
    try:
        # Récupère le message par son ID
        target_message = None
        for guild in bot.guilds:
            for channel in guild.text_channels:
                try:
                    target_message = await channel.fetch_message(message_id)
                    if target_message:
                        break
                except discord.NotFound:
                    continue
            if target_message:
                break

        if not target_message:
            await ctx.send(f"Erreur : Message avec l'ID {message_id} introuvable.")
            return

        # Répond au message
        await target_message.reply(response_content, mention_author=False)
        await ctx.send(f"Réponse envoyée au message ID {message_id} dans le salon {target_message.channel.mention} du serveur '{target_message.guild.name}' !")

    except discord.NotFound:
        await ctx.send(f"Erreur : Le message avec l'ID {message_id} n'a pas été trouvé (il peut être supprimé ou je n'y ai pas accès).")
    except discord.Forbidden:
        await ctx.send(f"Erreur de permissions : Je n'ai pas les droits suffisants pour voir ou accéder au message avec l'ID {message_id}.")
    except Exception as e:
        await ctx.send(f"Une erreur inattendue est survenue : {e}")

@bot.command(name="scrap", help="[ADMIN] scrappe l'intégralité des messages d'une personne spécifique sur un salon spécifique et stocke tous les messages dans un fichier texte", hidden=True)
@commands.is_owner() # CLÉ : Seul le propriétaire du bot peut utiliser cette commande
async def scrap_messages(ctx, channel_id: int, user_id: int):
    """
    Scrappe tous les messages d'un utilisateur spécifique dans un salon donné et les stocke dans un fichier texte.
    Seul le propriétaire du bot peut l'utiliser.
    """
    try:
        target_channel = bot.get_channel(channel_id)

        if not target_channel:
            target_channel = await bot.fetch_channel(channel_id)
            
        if not target_channel:
            await ctx.send(f"Erreur : Salon avec l'ID {channel_id} introuvable.")
            return

        if not isinstance(target_channel, discord.TextChannel):
            await ctx.send(f"Erreur : Le salon {target_channel.mention} (ID: {channel_id}) n'est pas un salon textuel.")
            return

        target_user = await bot.fetch_user(user_id)
        if not target_user:
            await ctx.send(f"Erreur : Utilisateur avec l'ID {user_id} introuvable.")
            return

        messages = []
        async for message in target_channel.history(limit=None):
            if message.author.id == user_id:
                messages.append(f"[{message.created_at}] {message.author.name}: {message.content}")

        if not messages:
            await ctx.send(f"Aucun message trouvé de {target_user.name} dans le salon {target_channel.mention}.")
            return

        filename = f"messages_{target_user.name}_{channel_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(messages))

        await ctx.send(f"Scrapping terminé ! {len(messages)} messages de {target_user.name} ont été sauvegardés dans le fichier '{filename}'.")

    except discord.NotFound:
        await ctx.send(f"Erreur : Le salon ou l'utilisateur spécifié n'a pas été trouvé.")
    except discord.Forbidden:
        await ctx.send(f"Erreur de permissions : Je n'ai pas les droits suffisants pour accéder au salon ou aux messages.")
    except Exception as e:
        await ctx.send(f"Une erreur inattendue est survenue : {e}")

@bot.command(name="scrap_full", help="[ADMIN] scrappe l'intégralité des messages de tout le monde sur un salon spécifique et stocke tous les messages dans un fichier texte", hidden=True)
@commands.is_owner() # CLÉ : Seul le propriétaire du bot peut utiliser cette commande
async def scrap_full_channel(ctx, channel_id: int):
    """
    Scrappe tous les messages dans un salon donné et les stocke dans un fichier texte.
    Seul le propriétaire du bot peut l'utiliser.
    """
    try:
        target_channel = bot.get_channel(channel_id)

        if not target_channel:
            target_channel = await bot.fetch_channel(channel_id)
            
        if not target_channel:
            await ctx.send(f"Erreur : Salon avec l'ID {channel_id} introuvable.")
            return

        if not isinstance(target_channel, discord.TextChannel):
            await ctx.send(f"Erreur : Le salon {target_channel.mention} (ID: {channel_id}) n'est pas un salon textuel.")
            return

        messages = []
        async for message in target_channel.history(limit=None):
            messages.append(f"[{message.created_at}] {message.author.name}: {message.content}")

        if not messages:
            await ctx.send(f"Aucun message trouvé dans le salon {target_channel.mention}.")
            return

        filename = f"full_messages_channel_{channel_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(messages))

        await ctx.send(f"Scrapping terminé ! {len(messages)} messages ont été sauvegardés dans le fichier '{filename}'.")

    except discord.NotFound:
        await ctx.send(f"Erreur : Le salon spécifié n'a pas été trouvé.")
    except discord.Forbidden:
        await ctx.send(f"Erreur de permissions : Je n'ai pas les droits suffisants pour accéder au salon ou aux messages.")
    except Exception as e:
        await ctx.send(f"Une erreur inattendue est survenue : {e}")

# Exécute le bot avec le token
if TOKEN:
    bot.run(TOKEN)
else:
    print("Erreur: Le token Discord n'a pas été trouvé. Assurez-vous que le fichier .env est configuré correctement.")