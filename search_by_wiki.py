import wikipedia, re

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")

def getwikisearch(s):
    result = wikipedia.search(s)
    if len(result) == 0:
        result1 = 'Ничего не нашлось\n'
        return result1
    else:
        result1 = 'Вот, что нашлось в Вики:\n'
        i = 1
        for x in result:
            result1 = result1 + str(i) + ') ' + x + '\n'
            i+=1
        return result1


    

def getstr(s, i):
    try:
        if int(i) > 0:
            i = int(i)
        s = s.split('\n')
        s = s[i : i+1]
        s = s[0]
        s = s.split(' ', 1)
        s = s[1]
        return s
    except Exception as e:
        return 'Введите заново:'

    

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext=ny.content[:1000]
        # Разделяем по переносам строки
        wikimas=wikitext.split('\n', 1)
        # Отбрасываем всё после первого абзаца
        wikimas = wikimas[0:1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                wikitext2=wikitext2+x
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\([^()]*\)', '', wikitext2)
        wikitext2=re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2+'\n'+wikipedia.page(s).url
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'Парсер дал осечку'
