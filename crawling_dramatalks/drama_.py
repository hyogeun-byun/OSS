import drama_info as info
import drama_talks as talks

drama_list = ["이미테이션","어느+날+우리+집+현관으로+멸망이+들어왔다","오월의+청춘","로스쿨","대박부동산",
              "모범택시","다크홀","언더커버","오케이+광자매","마인","보쌈+운명을+훔치다","아모르+파티+사랑하라+지금","밥이+되어라","미스+몬테크리스토","속아도+꿈결"]
drama_list_talk = ["Imitation","myulmang","theyouthofmay","lawschool","Realestateexorcism","taxidriver","darkhole","undercover","okgwangsis","MINE","bossam","amor","agoodsupper","missmontecristo","Evenifyourefooled"]
drama_chanel = ['kbs','cjenm','kbs','jtbc','kbs','sbs','cjenm','jtbc','kbs','cjenm','mbn','sbs','mbc','kbs','kbs']
idx = 0

while idx < len(drama_list) :
    info.search_info_to_db(idx,drama_list[idx])
    talks.search_talks_into_db(idx, drama_chanel[idx], drama_list_talk[idx])
    idx = idx + 1


