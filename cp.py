import msvcrt
import youtube_dl
import subprocess
import os

order = 0
play_order = 1
done = None
queue = {}
query = ''
playing = False
f = open('text.txt', 'w')

def download_video(order, query):
    ydl_opts = {
        'default_search': 'ytsearch1',
        'format': 'bestaudio/best',
        'audio_format': 'mp3',
        'quiet': True,
        'get_title': True,
        'outtmpl': '{0}.tmp'.format(order),
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

while not done:

    """Неблокирующий ввод с клавиатуры"""
    if msvcrt.kbhit():
        button = msvcrt.getch()
        letter = button.decode('cp866')
        if letter == '\r':
            order += 1
            queue[order] = query
            print('\r')
            download_video(order, query)
            query = ''
            continue
        if button == b'\x08':
            query = query[:-1]
            print(letter, sep=' ', end='', flush=True)
            print(' ', sep=' ', end='', flush=True)
            print(letter, sep=' ', end='', flush=True)
            continue
        query += letter
        print(letter, sep=' ', end='', flush=True)

    """Переключение на следующий трек и остановка воспроизведения"""
    if playing:
        poll = music.poll()
        if poll != None:
            os.remove('{0}.tmp'.format(play_order))
            play_order += 1
            if play_order > order:
                print('Конец плейлиста')
                break
            playing = False
            
    if not playing and not order == 0:
        music = subprocess.Popen('ffplay {0}.tmp -autoexit -loglevel warning'.format(play_order))
        playing = True
