"""Грузим туеву хучу рандомных модулей"""
import msvcrt
import youtube_dl
import subprocess
import os

"""Некоторые переменный надо объявить заранее, до взода в цикл"""
order = 0       #Номер последнего скачанного трека
play_order = 1  #Номер текущего трека
done = None     #Условие выхода из цикла
query = ''      #Текст запроса
playing = False #Играет ли музыка? А? А? Хуй на!

"""Загрузка видео"""
def download_video(order, query):
    ydl_opts = {
        'default_search': 'ytsearch1',
        'format': 'bestaudio/best',
        'audio_format': 'mp3',
        'quiet': True,
        'get_title': True,
        'outtmpl': '{0}.tmp'.format(order),
        }       #Опции загрузчика YoutubeDL, очевидно. А вот и сам загрузчик:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

"""Главный цикл"""
while not done:
    
    """Неблокирующий ввод с клавиатуры"""
    
    if msvcrt.kbhit():#Если кнопка нажата,
        button = msvcrt.getch()#то какая это кнопка
        letter = button.decode('cp866')#и что она вообще значит?
        if letter == '\r':#Если это Enter,
            order += 1#то у нас на одну песню больше в плейлисте,
            print('\r')#у нас новая строка,
            download_video(order, query)#и пора бы уже скачать саму песню,
            query = ''#забыть всё, что было,
            continue#и идти дальше, пропустив всё что там идёт потом в цикле.
        
        if button == b'\x08':#А если это Backspace,
            query = query[:-1]#то последняя буква нам уже не нужна.
            print(letter, sep=' ', end='', flush=True)#В строке тоже. Шаг назад.
            print(' ', sep=' ', end='', flush=True)#Закрыть пробелом.
            print(letter, sep=' ', end='', flush=True)#Ещё шаг назад.
            continue#Отпустить и забыть.
        
        #А если всё, что было выше, и не происходило вовсе?
        query += letter#Тогда мы просто добавляем букву к запросу
        print(letter, sep=' ', end='', flush=True)#и печатаем её.

    """Переключение на следующий трек и остановка воспроизведения"""
    if playing:#Если говорят, что музыка играет,
        poll = music.poll()#то стоит в этом убедиться,
        if poll != None:#ведь если уже не играет,
            os.remove('{0}.tmp'.format(play_order))#то и песня нам уже не нужна,
            play_order += 1#мы просто включим следующую.
            if play_order > order:#А если следующей нет,
                print('Конец плейлиста')#то мы прямо об этом заявим
                break#и вырвемся из этого долгого цикла. I want to break free!
            playing = False#Ну и надо предупредить, что песня-то кончилась!
            
    if not playing and not order == 0:#А если говорят, что музыка не играет,
        music = subprocess.Popen('ffplay {0}.tmp -autoexit -loglevel warning'\
                                 .format(play_order))#то включаем
        #какая там сейчас должна быть песня.
        playing = True#И громко всем об этом заявим!
