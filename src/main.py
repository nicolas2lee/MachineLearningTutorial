#===================== init phase ====================
#=====  read file and load data, generate tuple 

#infname='./../data/fresh_comp_offline/tianchi_fresh_comp_train_user.csv'
infname='./../data/fresh_comp_offline/rawshortdata.csv'
f = open(infname,'rb')
context=f.readlines()

#===== target : day 12.19
#===== data : from 11.18 to 12.18
#===== definition of features
#=========== simple version
#=========== evaluate target based on user behavior in the last day before target day
#=================== final calculation: evaluate 12.19 -> based on 12.18
#=================== train model: evaluate 12.18 -> based on 12.17
online_evaluate_day1219=[]
offline_evaluate_day1218=[]
train_day1217=[]
#========= behavior type
# 1 browse
# 2 collect
# 3 Add shopping cart
# 4 buy 
train_day1217=[]

for line in context:
  line = line.replace('\n', '')
  array = line.split(',')
  if array[0]=='user_id':
    continue
  dday = array[5].split(' ')[0].split('-')
  month = dday[1]
  day = int(dday[0])
#user_id, item_id, month, day
  uid= (array[0], array[1], month, day+1)
  if month=='12':
    if day==16:
      train_day1217.append(uid)
    if day==17:
      offline_evaluate_day1218.append(uid)
    if day==18:
      online_evaluate_day1219.append(uid)
# input day 16 -> output 17' compare to day 17
# input day 18 -> submit    
# make all elements unique
train_day1217=list(set(train_day1217))
offline_evaluate_day1218=list(set(offline_evaluate_day1218))
online_evaluate_day1219=list(set(online_evaluate_day1219))
  
