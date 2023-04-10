import discord
from discord.ext import commands
from config import settings
import random
import requests
import games
import tic_tac_toe
import operations
from operations import *

client = commands.Bot(command_prefix=settings['prefix'], intents=discord.Intents.all())
client.remove_command('help')
mentions = {}
marry_Event = False


@client.event
async def on_ready():
    print('Bot connected')
    print('Logs:', end='\n')
    server = client.guilds[1].members
    # role = discord.utils.get(client.guilds[0].roles, id=713358507478351902)
    for member in server:
        if member.id not in mentions.items():
            mentions[member.mention] = member.id
        else:
            if member.mention not in mentions.keys():
                for mention_member in mentions.keys():
                    if mention_member[mention_member] == member.id:
                        mentions.pop(mention_member)
                        mentions[member.mention] = member.id
        # if len(member.roles) == 1:
        # await member.add_roles(role)
        recording(member.id, member.display_name)


# for ser in client.guilds:
# operations.transfer(ser.name)
# for user in ser.members:
# operations.transfer(ser.name, user.mention, user.name, name_key=True)


'''@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None:
        a_id = after.channel.id
        b_channel = discord.utils.get(member.guild.channels, id=a_id)
        await b_channel.edit(name=(b_channel.name + ' ' + str(len(b_channel.members))))
    if before.channel is not None:
        a_id = before.channel.id
        b_channel = discord.utils.get(member.guild.channels, id=a_id)
        if b_channel.name[-1] in '123456789':
            await b_channel.edit(name=' '.join(b_channel.name.split()[:-1]))'''


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Такой команды нет, дурашка...')


@client.event
async def on_member_join(member):
    recording(member.id, member.display_name)

    # operations.transfer(member.guild.name, member.mention, member.name, name_key=True)

    #role = discord.utils.get(member.guild.roles, id=713358507478351902)
    #await member.add_roles(role)

    emb = discord.Embed(title='❤Добро пожаловать!❤', colour=0x00faff)
    emb.add_field(name='Приветствуем на нашем сервере!', value='Желаем хорошо провести время👍')
    await member.send(embed=emb)


@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if not msg.author.bot:

        counting(msg.author.id)
        count = operations.check(msg.author.id)
        if count >= 0:
            emb = discord.Embed(title='{} у вас новый уровень!'.format(msg.author.name), colour=0x00bfff)
            emb.add_field(name='Теперь ваш уровень:', value=count)
            emb.set_thumbnail(url=msg.author.avatar_url)
            await msg.channel.send(embed=emb)


@client.event
async def on_member_remove(member):
    operations.del_acc(member.id)

    emb = discord.Embed(title='❤Всего хорошего!❤', colour=0x00faff)
    emb.add_field(name='Спасибо, что посетил наш сервер!', value='🐳Я буду ждать твоего возвращения🐳')
    await member.send(embed=emb)


@client.event
async def on_member_update(before, after):
    operations.recording(before.id, after.display_name)


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author == client.user and reaction.emoji[0] == '❤':
        user_2 = (reaction.message.content.split()[1])[2:-1]
        user_1 = (reaction.message.content.split()[0][:-3])[2:-1]
        name_1 = operations.mycard(user_1)[0]
        name_2 = operations.mycard(user_2)[0]
        if user.display_name == operations.mycard(user_1)[0]:
            operations.waif(user_1, user_2)
            await reaction.message.channel.send(
                'Теперь {0} и {1} состоят в браке! Поздравим же их! Ваши карточки обновлены'.format(name_1, name_2))
        elif user == client.user:
            pass
        else:
            await reaction.message.channel.send('Ты кто? Предложение делают не тебе, так что сиди смирно и смотри!')


@client.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Hello, {author.mention}!')


@client.command()
async def clear(ctx, amount=100):
    if amount > 100:
        amount = 1
    emb = discord.Embed()
    if str(amount)[-1] == '1':
        emb.add_field(name='Очистка', value=('✅' + ' Удалено ' + str(amount) + ' сообщение'))
    elif str(amount)[-1] in '234':
        emb.add_field(name='Очистка', value=('✅' + ' Удалено ' + str(amount) + ' сообщения'))
    else:
        emb.add_field(name='Очистка', value=('✅' + ' Удалено ' + str(amount) + ' сообщений'))

    await ctx.channel.purge(limit=(amount + 1))
    await ctx.send(embed=emb)


@client.command()
async def divorce(ctx):
    name = ctx.message.author.name
    if operations.mycard(ctx.message.author.id)[4] == 'нет':
        await ctx.send('Ты и так одинок...')
    else:
        name_2 = operations.mycard(operations.mycard(ctx.message.author.id)[4])[0]
        await ctx.send(
            'Как бы грутсно это не было, но {0} подал на развод... Теперь {1} и {2} свободны.'.format(name, name,
                                                                                                      name_2))
        operations.del_waif(ctx.message.author.id, operations.mycard(ctx.message.author.id)[4])


@client.command()
async def marry(ctx, mention):
    global marry_Event
    marry_Event = True
    msg = '{0}!!! {1} делает вам предложение, оно того стоит, соглашайтесь '.format(mention,
                                                                                    ctx.message.author.mention)
    msg += "\n"
    msg += 'Если вы согласны, нажмите на ❤'
    await ctx.send(msg)
    async for message in ctx.channel.history(limit=5):
        if message.author.name == client.user.name:
            await message.add_reaction(emoji='❤')
            break
    '''mention = ''.join(mention.split('!'))
    name = operations.convert(ctx.guild.name, mention)
    if operations.mycard(ctx.message.author.name)[3] != 'нет':
        if 'Изменщик' in operations.mycard(ctx.message.author.name)[2]:
            await ctx.send('Опять за старое взялся, гнида?')
        else:
            await ctx.send('ТЫ АХУЕЛ?! Ты уже в браке, кому ты там еще предлагаешь. Изменщик!')
            operations.add_point(ctx.message.author.name, 'Изменщик')
    elif operations.mycard(name)[3] != 'нет':
        await ctx.send('Извини, но у {0} уже есть пара...'.format(mention))
    else:
        msg = ''
        if mention == ctx.message.author.mention:
            if 'Самовлюбленный уебок' in operations.mycard(ctx.message.author.name)[2]:
                await ctx.send('Без коментариев...')
            else:
                msg = 'Не люблю самовлюбленных дураков, так и быть, разрешаю тебе войти в брак самими с собой, но...'
                msg += '\n'
                msg += 'Титул самовлюбленный уебок теперь твой, радуйся :)'
                operations.add_point(name, 'Самовлюбленный уебок')
        else:
            msg = '{0}!!! {1} делает вам предложение, оно того стоит, соглашайтесь '.format(mention,
                                                                                            ctx.message.author.mention)
            msg += "\n"
            msg += 'Если вы согласны, нажмите на ❤'
        await ctx.send(msg)
        async for message in ctx.channel.history(limit=5):
            if message.author.name == client.user.name:
                await message.add_reaction(emoji='❤')
                break


@client.command()
async def play(ctx):
    voice_channel = ctx.message.author.dm_channel
    client.move_to(voice_channel)
'''


@client.command()
async def sclear(ctx, amount=100):
    if amount > 100:
        amount = 1
    await ctx.channel.purge(limit=amount + 1)


@client.command()
async def fc(ctx, *predict):
    if predict == ():
        await ctx.channel.send('Открыл рот и молчит... Зачем он это делает?')
    else:
        true = random.choice(['орел', 'решка'])
        select = ''.join(predict).lower()
        if select not in ['орел', 'решка', 'орёл']:
            await ctx.channel.send('Хмм... Я уверена, что у монетки только две стороны')
        elif select == true:
            await ctx.channel.send('Ей! Вы угадали! Вам начислено 10 поинтов')
            operations.add_point(ctx.author.id, 10)
        else:
            await ctx.channel.send('Из вас хреновый экстрасенс')


@client.command()
async def mycard(ctx):
    waifi = operations.mycard(ctx.author.id)[4]

    emb = discord.Embed(title='ID участника', colour=0x00bfff)
    emb.add_field(name='Уровень:', value=operations.mycard(ctx.author.id)[2], inline=False)
    emb.add_field(name='Количество поинтов:', value=operations.mycard(ctx.author.id)[1], inline=False)
    emb.add_field(name='Титулы:', value=''.join(operations.mycard(ctx.author.id)[3]), inline=False)
    if waifi == 'нет':
        emb.add_field(name='Брак:', value='нет', inline=False)
    else:
        emb.add_field(name='Брак:', value=operations.mycard(waifi)[0], inline=False)
    emb.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.send(embed=emb)


@client.command()
async def help(ctx):
    emb = discord.Embed(title='Помощь Гуры❤!', colour=0x00bfff)
    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.add_field(name='{}hello'.format(settings['prefix']), value='Приветствие')
    emb.add_field(name='{}anime'.format(settings['prefix']), value='Поиск gif')
    emb.add_field(name='{}clear'.format(settings['prefix']), value='Удаление сообщений')
    emb.add_field(name='{}slap (message)'.format(settings['prefix']), value='Шлепок')
    emb.add_field(name='{}ship'.format(settings['prefix']), value='Шипперинг')
    emb.add_field(name='{}game'.format(settings['prefix']), value='Игра в крестики-нолики')
    emb.add_field(name='{}fc'.format(settings['prefix']), value='Игра в монетку')
    emb.add_field(name='{}rps'.format(settings['prefix']), value='Игра в камень, ножницы, бумага')
    emb.add_field(name='{}mycard'.format(settings['prefix']), value='Карта участника')
    emb.add_field(name='{}say'.format(settings['prefix']), value='Сказать от имени бота')
    emb.add_field(name='{}marry (name)'.format(settings['prefix']), value='Не пашет :(')
    emb.add_field(name='{}divorce'.format(settings['prefix']), value='Подать на развод')

    await ctx.send(embed=emb)


@client.command()
async def say(ctx, *message):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(' '.join(message))


@client.command()
async def slap(ctx, *cause):
    people = ctx.channel.members
    people = people[:-1]
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(
        '{0.author.name} шлепнул {1.name} по причине: {2}'.format(ctx, random.choice(people), ' '.join(cause))
    )


@client.command()
async def anime(ctx):
    gif = random.choice(['hug', 'wink'])
    responce = 'https://some-random-api.ml/animu/' + gif
    image = requests.get(responce)
    image = image.json()

    emb = discord.Embed(title='random gif')
    emb.set_image(url=image['link'])
    await ctx.send(embed=emb)


@client.command()
async def ship(ctx):
    await ctx.channel.purge(limit=1)
    member_1 = random.choice(ctx.guild.members)
    member_2 = random.choice(ctx.guild.members)
    power_love = random.randint(1, 10)
    money = random.randint(1, 10)
    activiti = random.choice(games.activiti)
    status = random.choice(games.status)
    emb = discord.Embed(colour=0xfc0fc0)
    emb.add_field(name='Шип', value='{0.name} ❤ {1.name}'.format(member_1, member_2), inline=False)
    emb.add_field(name='Сила любви', value=('❤' * power_love + '🖤' * (10 - power_love)), inline=False)
    emb.add_field(name='Состояние', value=('💵' * money), inline=False)
    emb.add_field(name='Что было в отношениях', value=activiti, inline=False)
    emb.add_field(name='Состояние отношний', value=status, inline=False)

    await ctx.channel.send(embed=emb)


# box for admins
@client.command()
async def admin(ctx, password):
    await ctx.channel.purge(limit=1)
    if password == settings['password']:
        settings['admins'].append(ctx.message.author.name)


@client.command()
async def get_pass(ctx):
    await ctx.channel.purge(limit=1)
    if ctx.message.author.name in settings['admins']:
        await ctx.message.author.send(settings['password'])


@client.command()
async def save(ctx):
    if ctx.message.author.name in settings['admins']:
        f = discord.File('counting.txt')
        await ctx.channel.purge(limit=1)
        await ctx.message.author.send(file=f)


'''@client.command()
async def del_title(ctx, *message):
    await ctx.channel.purge(limit=1)
    if ctx.message.author.name in settings['admins']:
        if len(message) == 3:
            operations.del_lvl(message[0], int(message[2]))
        elif message[1].isdigit():
            operations.del_point(message[0], int(message[1]))
        else:
            operations.del_point(message[0], message[1])'''

'''@client.command()
async def check_card(ctx, name):
    await ctx.channel.purge(limit=1)
    if ctx.message.author.name in settings['admins']:
        emb = discord.Embed(title='Карточка {}'.format(name), colour=0x00bfff)
        emb.add_field(name='Уровень:', value=operations.mycard(name)[1], inline=False)
        emb.add_field(name='Количество поинтов:', value=operations.mycard(name)[0], inline=False)
        emb.add_field(name='Титулы:', value=' '.join(operations.mycard(name)[2]), inline=False)
        await ctx.message.author.send(embed=emb)'''


@client.command()
async def rps(ctx, *predict):
    if predict == ():
        await ctx.channel.send('Открыл рот и молчит... Зачем он это делает?')
    else:
        move = ''.join(predict).lower()
        if move not in games.rps['moves']:
            await ctx.send('Хмм... Я уверена, что в это играют по-другому')
        else:
            true = random.choice(games.rps['moves'])
            await ctx.send('У меня ' + true + ' ' + games.rps['smiles'][true])
            if true == move:
                await ctx.send('Вот это да! У нас ничья!')
            elif true == 'камень':
                if move == 'ножницы':
                    await ctx.send('Ура! Я выиграла!')
                else:
                    await ctx.send('Вот незадача! Ладно, в этот раз ты выиграл, вот твоя награда...')
                    await ctx.send('Вам начислено 15 поинтов')
                    operations.add_point(ctx.author.id, 15)
            elif true == 'ножницы':
                if move == 'бумага':
                    await ctx.send('Ура! Я выиграла!')
                else:
                    await ctx.send('Вот незадача! Ладно, в этот раз ты выиграл, вот твоя награда...')
                    await ctx.send('Вам начислено 15 поинтов')
                    operations.add_point(ctx.author.id, 15)
            else:
                if move == 'камень':
                    await ctx.send('Ура! Я выиграла!')
                else:
                    await ctx.send('Вот незадача! Ладно, в этот раз ты выиграл, вот твоя награда...')
                    await ctx.send('Вам начислено 15 поинтов')
                    operations.add_point(ctx.author.id, 15)


@client.command()
async def game(ctx, *move):
    if games.players[1] == '' and move == ():
        emb = discord.Embed(title='Правила!')
        emb.add_field(
            name='Запомнить!',
            value='После начала игры, игрок, которому принадлежит ход, должен написать 2 числа через пробел(пример: .game 1 1): 1 число - номер строки, 2 - номер столбца. Желаем удачи!')
        await ctx.channel.send(embed=emb)

        games.players[1] = ctx.message.author.name
        await ctx.channel.send('Кто хочет сразиться с {0}, напишите ".game я"'.format(games.players[1]))

    elif move == ():
        await ctx.channel.send('Открыл рот и молчит... Зачем он это делает?')

    elif ''.join(move) == 'cls':
        if ctx.message.author.name != games.players[1] and ctx.message.author.name != games.players[2]:
            await ctx.channel.send('Ты вообще кто? У тебя нет на это прав.')
        else:
            games.players[1] = ''
            games.players[2] = ''
            games.players['board'] = ''
            games.players['move'] = ''
            await ctx.channel.send('Игра прервана...')

    elif ''.join(move).lower() == 'я' and games.players[2] == '':
        games.players[2] = ctx.message.author.name
        games.players['move'] = random.choice([1, 2])
        games.players['board'] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        msg = ''
        graphic = ['╔═══════╦═══════╦═══════╗\n', '╠═══════╬═══════╬═══════╣\n', '╠═══════╬═══════╬═══════╣\n']
        for i in range(3):
            msg += graphic[i]
            s = ''
            for j in range(3):
                s += '║                      '
            s += '║\n'
            msg += s
        msg += '╚═══════╩═══════╩═══════╝'

        await ctx.channel.send('{0} будет сражаться с...'.format(games.players[1]))
        await ctx.channel.send('{0}!!!'.format(games.players[2]))
        await ctx.channel.send('Первым ходит: {0}'.format(games.players[games.players['move']]))
        await ctx.channel.send('🦈Да начнется битва🦈')
        await ctx.channel.send(msg)

    elif games.players[1] != '' and games.players[2] != '' and move[0] != 'я':
        check = ''.join(move)
        if len(check) > 2 or not check.isdigit():
            await ctx.channel.send('Ты читать умеешь? Если нет, то соболезную... Если да, то перечитай правила')
        elif len(check) < 2:
            await ctx.channel.send('Я в шоке... Слушай, а ты уверен, что тебе хватит мозгов продолжить игру?')
        elif int(check[0]) > 3 or int(check[0]) < 1 or int(check[1]) > 3 or int(check[1]) < 1:
            await ctx.channel.send('Ха-ха, а ты смешной(сарказм). Поле три на три, научись считать...')
        elif games.players['board'][int(check[0]) - 1][int(check[1]) - 1] != 0:
            await ctx.channel.send(
                'Ты чем-то похож на картошку, вы случайно не родственники? Глаза протри, там занято...')
        elif ctx.message.author.name != games.players[1] and ctx.message.author.name != games.players[2]:
            await ctx.channel.send('Ты вообще кто? Ты не играешь...')
        elif (games.players['move'] == 1 and ctx.message.author.name != games.players[1]) or (
                games.players['move'] == 2 and ctx.message.author.name != games.players[2]):
            if 'Гавнарь' in operations.mycard(ctx.message.author.id)[3]:
                await ctx.send('Опа, ты куда полез вне очереди? Неужели одного титула тебе не достаточно?!')
            else:
                await ctx.send(
                    'Опа, ты куда полез вне очереди? Титул "Гавнарь" выдан игроку ' + ctx.message.author.mention)
                operations.add_point(ctx.message.author.id, 'Гавнарь')
        else:
            game_tic = tic_tac_toe.main(games.players['board'], ''.join(move), games.players['move'])
            if len(game_tic) == 2:
                if game_tic[1] == 'win':
                    await ctx.channel.send('У нас есть победитель! Игра закончена')
                    if games.players[1] != games.players[2]:
                        await ctx.channel.send('Игроку {} начислено 20 поинтов'.format(ctx.message.author.mention))
                        operations.add_point(ctx.message.author.id, 20)
                    else:
                        await ctx.channel.send('Молодец! Сам себя переиграл')
                else:
                    await ctx.channel.send('У нас ничья! Игра закончена')
                    if games.players[1] != games.players[2]:
                        await ctx.channel.send('Игроки получают утешительный приз в размере 5 поинтов')
                        operations.add_point(games.players[1], 5)
                        operations.add_point(games.players[2], 5)
                games.players['board'] = game_tic[0]
                games.players[1] = ''
                games.players[2] = ''
                games.players['move'] = ''
            else:
                if games.players['move'] == 1:
                    games.players['move'] = 2
                else:
                    games.players['move'] = 1

                games.players['board'] = game_tic

            msg = ''
            graphic = ['╔═══════╦═══════╦═══════╗\n', '╠═══════╬═══════╬═══════╣\n', '╠═══════╬═══════╬═══════╣\n']
            for i in range(3):
                msg += graphic[i]
                s = ''
                for j in range(3):
                    s += '║'
                    if games.players['board'][i][j] == 0:
                        s += '                      '
                    elif games.players['board'][i][j] == 1:
                        s += '        :orthodox_cross:        '
                    else:
                        s += '        :yin_yang:        '
                s += '║\n'
                msg += s
            msg += '╚═══════╩═══════╩═══════╝'

            await ctx.channel.send(msg)

    elif move != ():
        if 'Клоун' in operations.mycard(ctx.message.author.id)[3]:
            await ctx.send('Клоун')
        else:
            await ctx.send(
                'Дамы и господа! Я, Гура Великолепная Умными Людьми Созданная, присваиваю тебе титул "Гений комедии" или, если выражаться по-твоему, "Клоун"')
            operations.add_point(ctx.message.author.id, 'Клоун')


client.run(settings['token'])
