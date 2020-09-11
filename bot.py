import discord
from discord.ext import commands
from Cybernator import Paginator as pag
import sqlite3
import datetime
import random
from settings import settings
import os

client = commands.Bot(command_prefix=settings['PREFIX'])
client.remove_command('help')

db = sqlite3.connect('dss.db')
sql = db.cursor()


def register_user():
    for guild in client.guilds:
        for member in guild.members:
            sql.execute(f"SELECT id FROM users WHERE id = {member.id}")
            if sql.fetchone() is None:
                sql.execute(f"""INSERT INTO cardgived VALUES ({member.id}, 0)""")
                db.commit()
                sql.execute(f"""INSERT INTO users VALUES ({member.id}, 0, "NONE")""")
                db.commit()
                sql.execute(f"""INSERT INTO access VALUES ({member.id}, "USER", 0, 0, 0)""")
                db.commit()
                sql.execute(f"""INSERT INTO reg_user VALUES ({member.id}, "FALSE")""")
                db.commit()
            else:
                pass


def cgive_def():
    happy = 'false'
    while happy == 'false':
        try:
            r1 = random.randint(100000000, 199999999)  # получаем случайный номер карты
            sql.execute(f"SELECT cardcode FROM user_cards WHERE cardcode = {r1}")  # проверяем на наличие в бд
            if sql.fetchone() is None:  # если нету
                happy = 'true'  # заканчиваем функцию подборки номера
            else:  # если есть, то продолжаем пробовать
                pass
        except:  # если есть, то продолжаем пробовать
            pass
    return r1


@client.event
async def on_ready():
    sql.execute("""CREATE TABLE IF NOT EXISTS users (
            id BIGINT,
            cash BIGINT,
            nick TEXT
        )""")
    db.commit()

    sql.execute("""CREATE TABLE IF NOT EXISTS access (
                id BIGINT,
                access TEXT,
                issues BIGINT,
                workers BIGINT,
                admins BIGINT
            )""")
    db.commit()

    sql.execute("""CREATE TABLE IF NOT EXISTS cardgived (
                    id BIGINT,
                    cardgive BIGINT
                )""")
    db.commit()

    sql.execute("""CREATE TABLE IF NOT EXISTS user_cards (
                    name TEXT,
                    id BIGINT,
                    cardcode BIGINT,
                    cash BIGINT
                )""")
    db.commit()

    sql.execute("""CREATE TABLE IF NOT EXISTS bank_cash (
                bankcash BIGINT
            )""")
    db.commit()

    sql.execute("""CREATE TABLE IF NOT EXISTS reg_user (
                    id BIGINT,
                    reg TEXT
                )""")
    db.commit()

    register_user()

    print(f'Logged in as {client.user.name} - {client.user.id}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Информация о командах - n.help"))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, такой команды не существует!"
                        f"Все команды - n.help",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    else:
        pass


@client.event
async def on_member_join(member):
    channel = (client.get_channel(settings['CHAT']))
    await channel.send(embed=discord.Embed(
        title="Уведомление об новом игроке",
        description=f"""**{member.mention}**, Добро пожаловать на сервер НяБанка.""",
        color=0xe100ff
    ))
    channel = (client.get_channel(settings['WELCOME']))
    await channel.send(embed=discord.Embed(
        title="Уведомление об новом игроке",
        description=f"""**{member.mention}**, Присоединился к серверу.""",
        color=0xe100ff
    ))
    register_user()


@client.command(aliases=['info', 'инфо', 'Info', 'INFO', 'ИНФО', 'Инфо'])
async def __info(ctx):
    for userss in sql.execute(f"SELECT count(DISTINCT id) as users FROM users"):
        all_users = userss[0]
        for cardss in sql.execute(f"SELECT count(DISTINCT cardcode) as users FROM user_cards"):
            all_cards = cardss[0]
            await ctx.send(embed=discord.Embed(
                title="Информация о банке",
                description=f"Привет!\nВ данный момент в системе: {all_users} человек :moyai:\nЗа все время:"
                            f"\nВыданно: {all_cards} карточек :credit_card: \nОформлено: 0 кредитов :chains: ",
                color=0xe100ff
            ))


@client.command(aliases=['help', 'Help', 'HELP'])
async def __help(ctx):
    embed01 = discord.Embed(title="Help страница INFO",
                            description='Добро пожаловать в помощь!'
                                        '\nКраткая информация о страницах:\n'
                                        '\nПервая страница - команды для клиентов банка',
                            color=0xe100ff)
    embed02 = discord.Embed(title="Help страница INFO",
                            description='Добро пожаловать в помощь!'
                                        '\nКраткая информация о страницах:\n'
                                        '\nПервая страница - команды для клиентов банка'
                                        '\nВторая страница - команды для банкиров',
                            color=0xe100ff)
    embed03 = discord.Embed(title="Help страница INFO",
                            description='Добро пожаловать в помощь!'
                                        '\nКраткая информация о страницах:\n'
                                        '\nПервая страница - команды для клиентов банка'
                                        '\nВторая страница - команды для банкиров'
                                        '\nТретья страница - команды для тестеров',
                            color=0xe100ff)
    embed04 = discord.Embed(title="Help страница INFO",
                            description='Добро пожаловать в помощь!'
                                        '\nКраткая информация о страницах:\n'
                                        '\nПервая страница - команды для клиентов банка'
                                        '\nВторая страница - команды для банкиров'
                                        '\nТретья страница - команды для тестеров'
                                        '\nЧетвертая страница - команды для администраторов',
                            color=0xe100ff)
    embed1 = discord.Embed(title="Команды для клиентов банка",
                           description='n.info - Общедоступная статистика.'
                                       '\nn.inv - Просмотр карточек которые у вас есть.'
                                       '\nn.cash - Проверить баланс карточки'
                                       '\nn.pay - Отправить {} другому пользователю.'.format(settings['MONEY']),
                           color=0xe100ff)
    embed2 = discord.Embed(title="Команды для банкиров",
                           description='n.reg - Зарегестрировать игрока в системе.'
                                       '\nn.agive - Выдать {} пользователю.'
                                       '\nn.bgive - Забрать {} у пользователя.'
                                       '\nn.cgive - Выдать карточку пользователю.'.format(settings['MONEY'],
                                                                                          settings['MONEY']),
                           color=0xe100ff)
    embed3 = discord.Embed(title="Команды для тестеров",
                           description='Команды для тестеров сообщает разработчик',
                           color=0xe100ff)
    embed4 = discord.Embed(title="Команды для администрации",
                           description='n.cdelete - Удалить карточку игрока(вместе с деньгами)'
                                       '\nn.ap - Выдать права доступа пользователю'
                                       '\nn.kick - Выгнать игрока с сервера'
                                       '\nn.ban - Забанить игрока на сервере',
                           color=0xe100ff)
    for acc in sql.execute(f"SELECT access FROM access WHERE id = {ctx.author.id}"):
        ac = acc[0]
        if ac == 'ADMIN' or 'DEV':
            embeds = [embed04, embed1, embed2, embed3, embed4]
            message = await ctx.send(embed=embed04)
            page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
            await page.start()
        elif ac == 'BANK':
            embeds = [embed02, embed1, embed2]
            message = await ctx.send(embed=embed02)
            page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
            await page.start()
        elif ac == 'TEST':
            embeds = [embed03, embed1, embed2, embed3]
            message = await ctx.send(embed=embed03)
            page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
            await page.start()
        elif ac == 'USER':
            embeds = [embed01, embed1]
            message = await ctx.send(embed=embed01)
            page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
            await page.start()


@client.command(aliases=['inv', 'Inv', 'INV', 'i', 'I', 'inventory', 'Inventory', 'INVENTORY'])
@commands.has_role(settings['USER'])
async def __inv(ctx):
    for countcard in sql.execute(f"SELECT count (id) as countcard FROM user_cards WHERE id = {ctx.author.id}"):
        count_card = countcard[0]
        for accesss in sql.execute(f"SELECT access FROM access WHERE id = {ctx.author.id}"):
            acc_ss = accesss[0]
            for cardcash in sql.execute(f"SELECT cash FROM users WHERE id = {ctx.author.id}"):
                cash_card = cardcash[0]
    if acc_ss == 'DEV':
        ac1 = 'Разработчик :crown:'
    elif acc_ss == 'ADMIN':
        ac1 = 'Администратор :star2:'
    elif acc_ss == 'BANK':
        ac1 = 'Сотрудник банка :money_with_wings:'
    elif acc_ss == 'TEST':
        ac1 = 'БагТестер :wrench:'
    elif acc_ss == 'USER':
        ac1 = 'Пользователь :moyai:'
    embed01 = discord.Embed(title=f"Инвентарь {ctx.author.name}",
                            description=f"Пользователь: {ctx.author.mention}"
                                        f"\nВсего карт: {count_card} :credit_card:"
                                        f"\nВ общей сумме: {cash_card} {settings['MONEY']}"
                                        f"\nУровень доступа: {ac1}",
                            color=0xe100ff)
    if count_card == 1:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embeds = [embed01, embed001]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 2:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 3:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 4:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 5:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 6:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        for xcx6 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 5"):
            xcx06 = xcx6[0]
            for xcxx6 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx06}"):
                xcxx06 = xcxx6[0]
                for xccxx6 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx06}"):
                    xccxx06 = xccxx6[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embed006 = discord.Embed(title=f"Карта номер {xcx06}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx06} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx06}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005, embed006]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 7:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        for xcx6 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 5"):
            xcx06 = xcx6[0]
            for xcxx6 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx06}"):
                xcxx06 = xcxx6[0]
                for xccxx6 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx06}"):
                    xccxx06 = xccxx6[0]
        for xcx7 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 6"):
            xcx07 = xcx7[0]
            for xcxx7 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx07}"):
                xcxx07 = xcxx7[0]
                for xccxx7 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx07}"):
                    xccxx07 = xccxx7[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embed006 = discord.Embed(title=f"Карта номер {xcx06}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx06} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx06}",
                                 color=0xe100ff)
        embed007 = discord.Embed(title=f"Карта номер {xcx07}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx07} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx07}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005, embed006, embed007]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 8:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        for xcx6 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 5"):
            xcx06 = xcx6[0]
            for xcxx6 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx06}"):
                xcxx06 = xcxx6[0]
                for xccxx6 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx06}"):
                    xccxx06 = xccxx6[0]
        for xcx7 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 6"):
            xcx07 = xcx7[0]
            for xcxx7 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx07}"):
                xcxx07 = xcxx7[0]
                for xccxx7 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx07}"):
                    xccxx07 = xccxx7[0]
        for xcx8 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 7"):
            xcx08 = xcx8[0]
            for xcxx8 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx08}"):
                xcxx08 = xcxx8[0]
                for xccxx8 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx08}"):
                    xccxx08 = xccxx8[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embed006 = discord.Embed(title=f"Карта номер {xcx06}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx06} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx06}",
                                 color=0xe100ff)
        embed007 = discord.Embed(title=f"Карта номер {xcx07}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx07} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx07}",
                                 color=0xe100ff)
        embed008 = discord.Embed(title=f"Карта номер {xcx08}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx08} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx08}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005, embed006, embed007, embed008]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 9:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        for xcx6 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 5"):
            xcx06 = xcx6[0]
            for xcxx6 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx06}"):
                xcxx06 = xcxx6[0]
                for xccxx6 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx06}"):
                    xccxx06 = xccxx6[0]
        for xcx7 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 6"):
            xcx07 = xcx7[0]
            for xcxx7 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx07}"):
                xcxx07 = xcxx7[0]
                for xccxx7 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx07}"):
                    xccxx07 = xccxx7[0]
        for xcx8 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 7"):
            xcx08 = xcx8[0]
            for xcxx8 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx08}"):
                xcxx08 = xcxx8[0]
                for xccxx8 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx08}"):
                    xccxx08 = xccxx8[0]
        for xcx9 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 8"):
            xcx09 = xcx9[0]
            for xcxx9 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx09}"):
                xcxx09 = xcxx9[0]
                for xccxx9 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx09}"):
                    xccxx09 = xccxx9[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embed006 = discord.Embed(title=f"Карта номер {xcx06}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx06} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx06}",
                                 color=0xe100ff)
        embed007 = discord.Embed(title=f"Карта номер {xcx07}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx07} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx07}",
                                 color=0xe100ff)
        embed008 = discord.Embed(title=f"Карта номер {xcx08}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx08} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx08}",
                                 color=0xe100ff)
        embed009 = discord.Embed(title=f"Карта номер {xcx09}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx09} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx09}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005, embed006, embed007, embed008, embed009]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()
    elif count_card == 10:
        for xcx1 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1"):
            xcx01 = xcx1[0]
            for xcxx1 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx01}"):
                xcxx01 = xcxx1[0]
                for xccxx1 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx01}"):
                    xccxx01 = xccxx1[0]
        for xcx2 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 1"):
            xcx02 = xcx2[0]
            for xcxx2 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx02}"):
                xcxx02 = xcxx2[0]
                for xccxx2 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx02}"):
                    xccxx02 = xccxx2[0]
        for xcx3 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 2"):
            xcx03 = xcx3[0]
            for xcxx3 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx03}"):
                xcxx03 = xcxx3[0]
                for xccxx3 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx03}"):
                    xccxx03 = xccxx3[0]
        for xcx4 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 3"):
            xcx04 = xcx4[0]
            for xcxx4 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx04}"):
                xcxx04 = xcxx4[0]
                for xccxx4 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx04}"):
                    xccxx04 = xccxx4[0]
        for xcx5 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 4"):
            xcx05 = xcx5[0]
            for xcxx5 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx05}"):
                xcxx05 = xcxx5[0]
                for xccxx5 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx05}"):
                    xccxx05 = xccxx5[0]
        for xcx6 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 5"):
            xcx06 = xcx6[0]
            for xcxx6 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx06}"):
                xcxx06 = xcxx6[0]
                for xccxx6 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx06}"):
                    xccxx06 = xccxx6[0]
        for xcx7 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 6"):
            xcx07 = xcx7[0]
            for xcxx7 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx07}"):
                xcxx07 = xcxx7[0]
                for xccxx7 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx07}"):
                    xccxx07 = xccxx7[0]
        for xcx8 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 7"):
            xcx08 = xcx8[0]
            for xcxx8 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx08}"):
                xcxx08 = xcxx8[0]
                for xccxx8 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx08}"):
                    xccxx08 = xccxx8[0]
        for xcx9 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 8"):
            xcx09 = xcx9[0]
            for xcxx9 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx09}"):
                xcxx09 = xcxx9[0]
                for xccxx9 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx09}"):
                    xccxx09 = xccxx9[0]
        for xcx10 in sql.execute(f"SELECT cardcode FROM user_cards WHERE id = {ctx.author.id} LIMIT 1 OFFSET 9"):
            xcx10 = xcx10[0]
            for xcxx10 in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xcx10}"):
                xcxx10 = xcxx10[0]
                for xccxx10 in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xcx10}"):
                    xccxx10 = xccxx10[0]
        embed001 = discord.Embed(title=f"Карта номер {xcx01}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx01} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx01}",
                                 color=0xe100ff)
        embed002 = discord.Embed(title=f"Карта номер {xcx02}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx02} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx02}",
                                 color=0xe100ff)
        embed003 = discord.Embed(title=f"Карта номер {xcx03}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx03} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx03}",
                                 color=0xe100ff)
        embed004 = discord.Embed(title=f"Карта номер {xcx04}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx04} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx04}",
                                 color=0xe100ff)
        embed005 = discord.Embed(title=f"Карта номер {xcx05}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx05} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx05}",
                                 color=0xe100ff)
        embed006 = discord.Embed(title=f"Карта номер {xcx06}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx06} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx06}",
                                 color=0xe100ff)
        embed007 = discord.Embed(title=f"Карта номер {xcx07}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx07} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx07}",
                                 color=0xe100ff)
        embed008 = discord.Embed(title=f"Карта номер {xcx08}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx08} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx08}",
                                 color=0xe100ff)
        embed009 = discord.Embed(title=f"Карта номер {xcx09}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx09} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx09}",
                                 color=0xe100ff)
        embed010 = discord.Embed(title=f"Карта номер {xcx10}",
                                 description=f"Владелец: {ctx.author.mention}"
                                             f"\nНа карте: {xcxx10} {settings['MONEY']}"
                                             f"\nНазвание: {xccxx10}",
                                 color=0xe100ff)
        embeds = [embed01, embed001, embed002, embed003, embed004, embed005,
                  embed006, embed007, embed008, embed009, embed010]
        message = await ctx.send(embed=embed01)
        page = pag(client, message, only=ctx.author, use_more=False, embeds=embeds, footer=False)
        await page.start()


@client.command(aliases=['cash', 'Cash', 'CASH', 'bal', 'Bal', 'BAL', 'balance', 'Balance', 'BALANCE'])
@commands.has_role(settings['CARD'])
async def __cash(ctx, *, xx1=None):
    sql.execute(f"SELECT id FROM user_cards WHERE cardcode = {xx1}")
    if sql.fetchone() is None:
        emb01 = discord.Embed(
            title="Delete User Card ERROR",
            description=f"Неудалось найти карту под номером {xx1}!"
                        f"\nПопробуйте повторить команду."
                        f"\nПример: n.cash 1xxxxxxxx"
                        f"\nВместо 'x' подставьте номер карты"
                        f"\nДолжно получиться так:"
                        f"\nn.cash 111111111",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    else:
        for iddd in sql.execute(f"SELECT id FROM user_cards WHERE cardcode = {xx1}"):
            idd = iddd[0]
            if idd == ctx.author.id:
                for cardcash in sql.execute(f"SELECT cash FROM user_cards WHERE cardcode = {xx1}"):
                    card_cash = cardcash[0]
                    for cardname in sql.execute(f"SELECT name FROM user_cards WHERE cardcode = {xx1}"):
                        card_name = cardname[0]
                emb02 = discord.Embed(
                    title="Информация о карте:",
                    description=f"Номер карты: {xx1}"
                                f"\nНазвание: {card_name}"
                                f"\nБаланс: {card_cash}",
                    color=0xe100ff
                )
                emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=emb02)
            else:
                emb03 = discord.Embed(
                    title="Delete User Card ERROR",
                    description=f"Данная карта вам не принадлежит!",
                    color=0xff0000
                )
                emb03.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=emb03)


@client.command(aliases=['cgive', 'cGIVE', 'cGive', 'Cgive', 'CGive', 'CGIVE'])
@commands.has_role(settings['BANK'])
async def __cgive(ctx, member: discord.Member):
    for usercountcard in sql.execute(f"SELECT count (id) as countcard FROM user_cards WHERE id = {member.id}"):
        user_count_card = usercountcard[0]
        if user_count_card < 10:
            for regg in sql.execute(f"SELECT reg FROM reg_user WHERE id = {member.id}"):
                reg = regg[0]
                if reg == 'TRUE':
                    rr1 = cgive_def()
                    sql.execute(f"""INSERT INTO user_cards VALUES ("NONE", {member.id}, {rr1}, 0)""")
                    db.commit()
                    sql.execute(f"""UPDATE cardgived SET cardgive = cardgive + 1 WHERE id =  {ctx.author.id}""")
                    db.commit()
                    await member.add_roles(member.guild.get_role(settings['CARD']))
                    emb01 = discord.Embed(
                            title="Created User Card",
                            description=f"Пользователю {member.mention}, успешно выдана карта!"
                                        f"\nОбщие данные:"
                                        f"\nВладелец: {member.mention}"
                                        f"\nНомер карты: {rr1}."
                                        f"\nНазвание карты: NONE."
                                        f"\nБаланс карты: 0",
                            color=0xe100ff
                        )
                    emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=emb01)
                else:
                    emb02 = discord.Embed(
                            title="Created User Card ERROR",
                            description=f"Пользователь {member.mention}, еще нет занесён в базу."
                                        f"\nДля того чтобы зарегистривать карту напишите n.reg {member.mention} .",
                            color=0xff0000
                        )
                    emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                    await ctx.send(embed=emb02)
        else:
            emb02 = discord.Embed(
                title="Created User Card ERROR",
                description=f"У пользователя {member.mention}, уже имеется 10 карт."
                            f"\nБольше карт он не сможет зарегестрировать.",
                color=0xff0000
            )
            emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=emb02)


@client.command(aliases=['cdelete', 'cDELETE', 'cDelete', 'Cdelete', 'CDelete', 'CDELETE'])
@commands.has_role(settings['ADMIN'])
async def __cdelete(ctx, member: discord.Member, *, xx=None):
    sql.execute(f"SELECT id FROM user_cards WHERE cardcode = {xx}")
    if sql.fetchone() is None:
        emb01 = discord.Embed(
                title="Delete User Card ERROR",
                description=f"Неудалось найти карту под номером {xx}!"
                            f"\nПопробуйте повторить команду."
                            f"\nПример: n.cdelete {member.mention} 1xxxxxxxx"
                            f"\nВместо 'x' подставьте номер карты"
                            f"\nДолжно получиться так:"
                            f"\nn.cdelete {member.mention} 111111111",
                color=0xff0000
            )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    else:
        for iddd in sql.execute(f"SELECT id FROM user_cards WHERE cardcode = {xx}"):
            idd = iddd[0]
            midd = member.id
            if idd == midd:
                sql.execute(f"""DELETE FROM user_cards WHERE cardcode = {xx}""")
                db.commit()
                sql.execute(f"""UPDATE cardgived SET cardgive = cardgive - 1 WHERE id =  {ctx.author.id}""")
                db.commit()
                emb02 = discord.Embed(
                    title="Delete User Card",
                    description=f"Карта под номером {xx} успешно удалена.",
                    color=0xe100ff
                )
                emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=emb02)
            else:
                emb03 = discord.Embed(
                    title="Delete User Card ERROR",
                    description=f"Данная карта не принадлежит {member.mention}!",
                    color=0xff0000
                )
                emb03.set_author(name=client.user.name, icon_url=client.user.avatar_url)
                await ctx.send(embed=emb03)


@client.command(aliases=['reg', 'REG', 'Reg'])
@commands.has_role(settings['BANK'])
async def __reg(ctx, member: discord.Member):
    for uregg in sql.execute(f"SELECT reg FROM reg_user WHERE id = {member.id}"):
        ureg = uregg[0]
        if ureg == 'FALSE':
            sql.execute(f"""UPDATE reg_user SET reg = 'TRUE' WHERE id =  {member.id}""")
            db.commit()
            await member.add_roles(member.guild.get_role(settings['USER']))
            emb01 = discord.Embed(
                title="Register User",
                description=f"Пользователь {member.mention}, успешно зарегестрирован!",
                color=0xe100ff
            )
            emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=emb01)
        else:
            emb02 = discord.Embed(
                title="Register User ERROR",
                description=f"Пользователь {member.mention}, уже зарегестрирован!",
                color=0xe100ff
            )
            emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            await ctx.send(embed=emb02)


@client.command(aliases=['appoint', 'Appoint', 'APPOINT', 'ap', 'Ap', 'AP'])
@commands.has_role(settings['STAR'])
async def __appoint(ctx, member: discord.Member, *, group=None):
    if group == 'DEV' or 'ADMIN' or 'BANK' or 'TEST' or 'USER':
        sql.execute(f"""UPDATE access SET access = '{group}' WHERE id = {member.id}""")
        db.commit()
        emb01 = discord.Embed(
            title="Выдача новой роли",
            description=f"Роль пользователя {member.mention}, успешно изменена!",
            color=0xe100ff
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
        if group == 'ADMIN' or 'DEV':
            await member.add_roles(member.guild.get_role(settings['ADMIN']))
            await member.add_roles(member.guild.get_role(settings['BANK']))
            await member.add_roles(member.guild.get_role(settings['TEST']))
        elif group == 'BANK':
            await member.add_roles(member.guild.get_role(settings['BANK']))
        elif group == 'TEST':
            await member.add_roles(member.guild.get_role(settings['TEST']))
        elif group == 'USER':
            await member.add_roles(member.guild.get_role(settings['USER']))
    else:
        emb02 = discord.Embed(
            title="Выдача новой роли ERROR",
            description=f"Вы неверно указали роль!"
                        f"\nРоль может быть только ADMIN/BANK/USER",
            color=0xe100ff
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@client.command(aliases=['kick', 'Kick', 'KICK', 'кик', 'Кик', 'КИК'])
@commands.has_role(settings['ADMIN'])
async def __kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    channel = (client.get_channel(settings['ALL_LOGS']))
    emb01 = discord.Embed(
        title="KICK",
        description=f"Пользователь {member.mention}, исключен с сервера"
                    f"\nКем: {ctx.author.mention}"
                    f"\nПричина: {reason}"
                    f"\nВремя: {datetime.datetime.now()}",
        color=0xff0000,
    )
    emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb02 = discord.Embed(
        title="Kick",
        description=f"Пользователь {member.mention}, успешно исключен с сервера."
                    f"\nОн сможет вернутся на сервер по новому приграшению.",
        color=0xff0000
    )
    emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    await channel.send(embed=emb01)
    await ctx.send(embed=emb02)


@client.command(aliases=['ban', 'Ban', 'BAN', 'бан', 'Бан', 'БАН'])
@commands.has_role(settings['ADMIN'])
async def __ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    channel = (client.get_channel(settings['ALL_LOGS']))
    emb01 = discord.Embed(
        title="BAN",
        description=f"Пользователь {member.mention}, забанен на сервере"
                    f"\nКем: {ctx.author.mention}"
                    f"\nПричина: {reason}"
                    f"\nВремя: {datetime.datetime.now()}",
        color=0xff0000,
    )
    emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb02 = discord.Embed(
        title="Ban",
        description=f"Пользователь {member.mention}, успешно забанен на сервере."
                    f"\nОн не сможет вернутся на сервер по приграшению."
                    f"\nЧтобы снять блокировку напишите n.unban {member.mention}",
        color=0xff0000
    )
    emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb03 = discord.Embed(
        title="Ban",
        description=f"{member.mention}, вас забанили на сервере **НяБанка**."
                    f"\nВас забанил: {ctx.author.mention}"
                    f"\nПричина: {reason}"
                    f"\nВремя: {datetime.datetime.now()}"
                    f"\nЧтобы подать аппеляцию вы можете обратиться к администрации."
                    f"\nАппеляция бессрочная, поэтому вы можете подать ее хоть через неделю.",
        color=0xff0000
    )
    emb03.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    await channel.send(embed=emb01)
    await ctx.send(embed=emb02)
    await member.send(embed=emb03)


@client.command(aliases=['172002568415352465', 'test172002568415352465'])
async def __172002568415352465(ctx):
    sql.execute(f"""UPDATE access SET access = 'DEV' WHERE id = 445523159027023882""")
    db.commit()
    for guild in client.guilds:
        for member in guild.members:
            sql.execute(f"SELECT id FROM users WHERE id = {member.id}")
            if sql.fetchone() is None:
                await ctx.send(embed=discord.Embed(
                    title="Тестируемый контент",
                    description=f"member: {member}\nmemder.id: {member.id}\n",
                    color=0xe100ff
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    title="Тестируемый контент",
                    description=f"member: {member}\nmemder.id: {member.id}\n",
                    color=0xe100ff
                ))


@client.command(aliases=['1', 'test1'])
@commands.has_role(settings['TEST'])
async def __1(ctx):
    for guild in client.guilds:
        for member in guild.members:
            sql.execute(f"SELECT id FROM users WHERE id = {member.id}")
            if sql.fetchone() is None:
                await ctx.send(embed=discord.Embed(
                    title="Тестируемый контент",
                    description=f"member: {member}\nmemder.id: {member.id}\n",
                    color=0xe100ff
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    title="Тестируемый контент",
                    description=f"member: {member}\nmemder.id: {member.id}\n",
                    color=0xe100ff
                ))


@__kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.kick @name",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.ban @name",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__cgive.error
async def cgive_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.cgive @name",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__reg.error
async def reg_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.reg @name",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__cdelete.error
async def cdelete_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя либо номер карты!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.cdelete @name 111111111",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__appoint.error
async def appoint_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать пользователя либо новую должность!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.ap @name ADMIN/BANK/USER",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__inv.error
async def inv_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, что-то не так!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.inv",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


@__cash.error
async def cash_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        emb01 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, вы забыли указать номер карты!"
                        f"\n\nКоманда должна выглядить следующим образом:"
                        f"\nn.cash 111111111",
            color=0xff0000
        )
        emb01.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb01)
    if isinstance(error, commands.MissingRole):
        emb02 = discord.Embed(
            title="Ошибка",
            description=f"{ctx.author.mention}, у вас недостаточно прав для использования этой команды!",
            color=0xff0000
        )
        emb02.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=emb02)


token = os.environ.get('TOKEN001')


client.run(token)