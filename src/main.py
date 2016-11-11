infname='./../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv'
f = open(infname,'rb')
context=f.readlines()
# get raw data, and generate tuple
for line in context:
  line = line.replace('\n', '')
  array = line.split(',')
  if array[0]=='user_id':
    continue
  day = array[5].split(' ')[0].split('-')[2]
#user_id, item_id, day
  tupleid= (array[0], array[1], day)
  
