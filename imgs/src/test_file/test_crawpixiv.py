from crawpixiv import Pixiv

#print(os.path.abspath('.'))
    #input()
p = Pixiv()
#p.get_mode()
#p.get_pic(83113557, ["魔法少女まどか☆マギカ","星空ドレス"])
#p.get_pic(82928832)
#print(p.db.data)
p.run_rank(date = 20200831, limit = 50)
#p.run_author(11491793)
#print(p.info)
#for pic in p.info:
#    p.info[pic].get_info()