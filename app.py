import streamlit as st #line:1
import requests #line:2
from datetime import datetime #line:3
import pytz #line:4
banned_users ={"Banned":{"reason":"Test Reason","unban_date":"10-12-24 10:00","moderator_note":"Test Mod note..",},"MkSeven1":{"reason":"No root Access!?!?","unban_date":"30-11-24 10:00","moderator_note":"Wrong Admin account.",},}#line:18
users ={"MkSeven1":"9872","penisbobra3":"izudoner667","Banned":"1","какой то пидор":"","root":"9872",}#line:27
def login (O0O0000000000OO0O ,OOO0O00OO0O0O0OOO ):#line:30
    return users .get (O0O0000000000OO0O )==OOO0O00OO0O0O0OOO #line:31
def check_ban (O0OOO0OOO0OO0OO00 ):#line:34
    OO0OOOO00OOOO00OO =banned_users .get (O0OOO0OOO0OO0OO00 )#line:35
    if OO0OOOO00OOOO00OO :#line:36
        OO0OO0O00O0OO0OOO =datetime .now (pytz .timezone ('America/Chicago'))#line:38
        OOO00OO0OO0OOOO00 =datetime .strptime (OO0OOOO00OOOO00OO ["unban_date"],"%d-%m-%y %H:%M")#line:39
        OOO00OO0OO0OOOO00 =pytz .timezone ('America/Chicago').localize (OOO00OO0OO0OOOO00 )#line:40
        if OO0OO0O00O0OO0OOO <OOO00OO0OO0OOOO00 :#line:41
            return OO0OOOO00OOOO00OO #line:42
    return None #line:43
def set_cookie (OOO00O0O0000O0O0O ,O00OOO000OO00OO0O ):#line:46
    st .experimental_set_query_params (**{OOO00O0O0000O0O0O :O00OOO000OO00OO0O })#line:47
def get_cookie (O0O0O0OO0O00O0OOO ):#line:49
    OOO0OOOOOOO0OO000 =st .experimental_get_query_params ()#line:50
    return OOO0OOOOOOO0OO000 .get (O0O0O0OO0O00O0OOO ,[None ])[0 ]#line:51
if 'logged_in'not in st .session_state :#line:54
    st .session_state ['logged_in']=False #line:55
if not st .session_state ['logged_in']:#line:58
    st .title ("Авторизация")#line:59
    username =st .text_input ("Логин")#line:60
    password =st .text_input ("Пароль",type ="password")#line:61
    if st .button ("Войти"):#line:63
        if login (username ,password ):#line:64
            ban_info =check_ban (username )#line:65
            if ban_info :#line:66
                st .error (f"Вы забанены до {ban_info['unban_date']}. Причина: {ban_info['reason']}.")#line:67
            else :#line:68
                st .session_state ['logged_in']=True #line:69
                set_cookie ("logged_in","true")#line:70
                st .success ("Вы успешно вошли в систему!")#line:71
                st .rerun ()#line:72
        else :#line:73
            st .error ("Неверный логин или пароль.")#line:74
    st .stop ()#line:75
st .sidebar .title ("Панель управления")#line:78
if st .sidebar .button ("Выйти"):#line:79
    st .session_state ['logged_in']=False #line:80
    set_cookie ("logged_in","false")#line:81
    st .rerun ()#line:82
    st .stop ()#line:83
st .title ("AI Фильтр текста")#line:86
user_input =st .text_area ("Введите текст для анализа:",placeholder ="Введите текст здесь... (Только на английском языке)")#line:87
api_user ="43464075"#line:89
api_secret ="vJ2XKNu732mFPqGrEvRzX5SgyLoGdPqr"#line:90
if not api_user or not api_secret :#line:92
    st .error ("Отсутствуют данные API. Добавьте их для продолжения.")#line:93
else :#line:94
    if st .button ("Анализировать текст"):#line:95
        if not user_input .strip ():#line:96
            st .warning ("Введите текст для анализа.")#line:97
        else :#line:98
            try :#line:99
                data ={'text':user_input ,'mode':'ml','lang':'en','models':'general,self-harm','api_user':api_user ,'api_secret':api_secret }#line:107
                response =requests .post ('https://api.sightengine.com/1.0/text/check.json',data =data )#line:108
                if response .status_code ==200 :#line:109
                    output =response .json ()#line:110
                    flagged_classes =[OOO0OOOO0000000OO for OOO0OOOO0000000OO ,OO0000OO0OOOOO000 in output .get ("moderation_classes",{}).items ()if isinstance (OO0000OO0OOOOO000 ,(int ,float ))and OO0000OO0OOOOO000 >0.1 ]#line:114
                    if flagged_classes :#line:115
                        st .warning (f"Обнаружены проблемные категории: {', '.join(flagged_classes)}")#line:116
                    else :#line:117
                        st .success ("Текст не содержит проблемного контента.")#line:118
                    st .json (output )#line:119
                else :#line:120
                    st .error (f"Ошибка API: {response.status_code} - {response.text}")#line:121
            except Exception as e :#line:122
                st .error (f"Произошла ошибка: {str(e)}")#line:123
