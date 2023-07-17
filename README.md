Python version 3.11.3
Перед тем как запускать скрипт,все положить в одну папку и нужно в терминале перейти в директорию этой папки и от туда запускать
После в терминале прописать комманду python main.py -c 'config.ini'
Entert command "Currency"



todo:
- почитай про python virtual environment
- https://github.com/Stepafn/Currence/blob/main/main.py#L16 почитай про parse known args
- из init объекта вынеси код конфигурации во внешний модуль и импортируй его, а не делай вот так: https://github.com/Stepafn/Currence/blob/main/main.py#L25
- https://github.com/Stepafn/Currence/blob/main/main.py#L26 вынеси в конфиг. никакого hardcode внутри code
- https://github.com/Stepafn/Currence/blob/main/main.py#L46 название лог файла, параметры логгирования - в конфиг.
- напиши всем функциям в их definitions тип данных, что они возвращают
  

https://github.com/Stepafn/Currence/blob/main/config.ini#L1
какой смысл в этом комментарии?
напиши комментарии у каждого параметра в конфиге

никакого русского языка пока от тебя это не начнут требовать специально
https://github.com/Stepafn/Currence/blob/main/main.py#L14


parser.add_argument('--dollar_rub', help='ruble exchange rate')
глядя на это я ожидаю там увидеть цифру
а там линк
переименуй переменную

parser.add_argument('--sleep', help='Пауза')
что за пауза?
почему sleep, а не delay
пауза в часах или днях? в чём?

https://github.com/Stepafn/Currence/blob/main/main.py#L15
ничо не понятно из названия и комментария
сделай так, чтобы было понятно тому, кто запустит help или посмотрит код конфигурации

https://github.com/Stepafn/Currence/blob/main/main.py#L50
почему преобразование не внутри функции?

float(self.parse.tracking_point):
у тебя в коде дважды такие преобразования. что-то не так - преобразуй один раз, затем используй переменную

logging.info(f"Current rate: 1 dollar = {str(currency)}")
зачем тут str? почитай документацию еще раз про модификатор f

https://github.com/Stepafn/Currence/blob/main/main.py#L56
основной код не должен делать преобразования конфиг переменных в процессе исполнения- подними их в то место, где читается конфиг
посмотри - может быть конфигураицонный модуль уже умеет делать преобразования сам 


https://github.com/Stepafn/Currence/blob/main/main.py#L51
https://github.com/Stepafn/Currence/blob/main/main.py#L53

я писал замечания по поводу сравнения - ты не исправил. ищи и исправляй

https://github.com/Stepafn/Currence/blob/main/main.py#L65
применение исключений для этой проверки избыточно. перепиши без них

https://github.com/Stepafn/Currence/blob/main/main.py#L67
дай пояснения - почему возникла ошибка в отладочном сообщении










            

