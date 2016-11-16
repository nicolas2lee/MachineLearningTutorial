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
  day = int(dday[2])
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

#================== Preprocess Data
#======= for feature
'''
for i in range(4):
  ui_dict[i]={} 
'''
#================== the same as before
ui_dict = [ {} for i in range(4)]

for line in context:
  line = line.replace('\n', '')
  array = line.split(',')
  if array[0]=='user_id':
    continue
  dday= array[5].split(' ')[0].split('-')  
  month = dday[1]
  day= int(dday[2])
  uid = (array[0], array[1], month, day)
  behavior_type=int(array[2])-1
  if uid in ui_dict[behavior_type]:
    ui_dict[behavior_type][u_id]+=1
  else:
    ui_dict[behavior_type]=1
#======== for label
ui_buy={}
for line in context:
  line = line.replace('\n', '')
  array = line.split(',')
  if array[0]=='user_id':
    continue
  dday = array[5].split(' ')[0].split('-')
  month = dday[1]
  day = int(dday[2])
  uid=(array[0], array[1], month, day)
  if array[2]==4 :
    ui_buy[uid]=1

import numpy as np
X = np.zeros((len(train_day1217),4))
y = np.zeros(len(train_day1217))

id = 0
for uid in train_day1217:
  last_uid=(uid[0], uid[1], uid[2], uid[3]-1)
  for i in range(4):
    if last_uid in ui_dict[i]:
      X[i][id]=math.log1p(ui_dict[i][last_uid])
    else:
      X[i][id]=0
  if last_uid in ui_buy:
    y[id]=1
  else:
    y[id]=0
  id+=1
#================= train and fit the logistic regression model
