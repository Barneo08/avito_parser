import pytz

def transliterate(text)->str:
  legend = {
      'а':'a',
      'б':'b',
      'в':'v',
      'г':'g',
      'д':'d',
      'е':'e',
      'ё':'e',
      'ж':'zh',
      'з':'z',
      'и':'i',
      'й':'y',
      'к':'k',
      'л':'l',
      'м':'m',
      'н':'n',
      'о':'o',
      'п':'p',
      'р':'r',
      'с':'s',
      'т':'t',
      'у':'u',
      'ф':'f',
      'х':'h',
      'ц':'ts',
      'ч':'ch',
      'ш':'sh',
      'щ':'sch',
      'ъ':'',
      'ы':'y',
      'ь':'',
      'э':'e',
      'ю':'yu',
      'я':'ya',
      '-': '-',
      ' ': '_',
  }
  text = text.lower()
  tr_text = ''
  for char in text:
    tr_text += legend[char]
  return tr_text


def utc_to_local(utc_dt, time_zone='Europe/Moscow'):
    local_tz = pytz.timezone(time_zone)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def aslocaltimestr(utc_dt, time_zone='Europe/Moscow'):
    return utc_to_local(utc_dt, time_zone).strftime('%Y-%m-%d %H:%M')