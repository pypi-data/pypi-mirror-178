# -*- coding: UTF-8 -*-
logger.info("Loading 19 objects to table aids_simpleconfirmation...")
# fields: id, created, start_date, end_date, user, company, contact_person, contact_role, printed_by, signer, state, client, granting, remark, language
loader.save(create_aids_simpleconfirmation(1,dt(2018,12,16,8,8,9),date(2014,5,25),date(2015,5,25),10,None,None,None,5,9,u'01',130,40,u'',u'de'))
loader.save(create_aids_simpleconfirmation(2,dt(2018,12,16,8,8,9),date(2014,5,25),date(2015,5,25),4,None,None,None,None,9,u'02',130,40,u'',u'de'))
loader.save(create_aids_simpleconfirmation(3,dt(2018,12,16,8,8,9),date(2014,5,25),None,6,None,None,None,None,4,u'01',132,41,u'',u'de'))
loader.save(create_aids_simpleconfirmation(4,dt(2018,12,16,8,8,9),date(2014,5,26),date(2014,5,27),9,None,None,None,None,5,u'02',133,42,u'',u'de'))
loader.save(create_aids_simpleconfirmation(5,dt(2018,12,16,8,8,9),date(2014,5,26),date(2014,5,27),5,None,None,None,None,5,u'01',133,42,u'',u'de'))
loader.save(create_aids_simpleconfirmation(6,dt(2018,12,16,8,8,9),date(2014,5,26),date(2014,5,27),10,None,None,None,None,5,u'02',137,43,u'',u'de'))
loader.save(create_aids_simpleconfirmation(7,dt(2018,12,16,8,8,9),date(2014,5,29),None,9,None,None,None,None,5,u'01',146,48,u'',u'de'))
loader.save(create_aids_simpleconfirmation(8,dt(2018,12,16,8,8,9),date(2014,5,29),None,5,None,None,None,None,5,u'02',146,48,u'',u'de'))
loader.save(create_aids_simpleconfirmation(9,dt(2018,12,16,8,8,9),date(2014,5,29),date(2014,5,30),10,None,None,None,None,4,u'01',147,49,u'',u'de'))
loader.save(create_aids_simpleconfirmation(10,dt(2018,12,16,8,8,9),date(2014,5,30),date(2014,5,31),4,None,None,None,None,6,u'02',152,50,u'',u'fr'))
loader.save(create_aids_simpleconfirmation(11,dt(2018,12,16,8,8,9),date(2014,5,30),date(2014,5,31),6,None,None,None,None,6,u'01',152,50,u'',u'fr'))
loader.save(create_aids_simpleconfirmation(12,dt(2018,12,16,8,8,9),date(2014,5,30),date(2014,6,29),9,None,None,None,None,4,u'02',153,51,u'',u'fr'))
loader.save(create_aids_simpleconfirmation(13,dt(2018,12,16,8,8,9),date(2014,5,31),date(2014,5,31),5,None,None,None,None,None,u'01',155,52,u'',u'en'))
loader.save(create_aids_simpleconfirmation(14,dt(2018,12,16,8,8,9),date(2014,5,31),date(2014,5,31),10,None,None,None,None,None,u'01',155,52,u'',u'en'))
loader.save(create_aids_simpleconfirmation(15,dt(2018,12,16,8,8,9),date(2014,5,31),None,4,None,None,None,None,None,u'01',157,53,u'',u'de'))
loader.save(create_aids_simpleconfirmation(16,dt(2018,12,16,8,8,9),date(2014,6,1),date(2015,6,1),6,None,None,None,None,4,u'01',159,54,u'',u'de'))
loader.save(create_aids_simpleconfirmation(17,dt(2018,12,16,8,8,9),date(2014,6,1),date(2015,6,1),9,None,None,None,None,4,u'02',159,54,u'',u'de'))
loader.save(create_aids_simpleconfirmation(18,dt(2018,12,16,8,8,9),date(2014,6,1),None,5,None,None,None,None,5,u'01',161,55,u'',u'de'))
loader.save(create_aids_simpleconfirmation(19,dt(2018,12,16,8,8,9),date(2014,5,22),date(2014,5,22),6,100,None,None,1,None,u'01',240,58,u'',u'de'))

loader.flush_deferred_objects()
