import pickle

file = "./youtube2text_iccv15/dict_movieID_caption.pkl"
cnt_mov = 0
cnt_captions = 0
min_cnt = float('inf')
min_id = -1
with open(file, 'rb') as f:
    data = pickle.load(f)
    # print data
    for mov_id in data:
        # print mov_id, data[mov_id]
        cnt_mov += 1
        cnt_captions += len(data[mov_id])
        min_cnt = min(len(data[mov_id]), min_cnt)
        if len(data[mov_id]) == min_cnt:
            min_id = mov_id
        # break
    print cnt_mov
    print cnt_captions
    # print min_cnt, min_id
    # print min_id, data[min_id]
    print data['x68Djm_Q0GA_0_10']


##############################################################


# import json

# file = "./annotations/captions_train2017.json"
# data = json.load(open(file))

# print data.keys()
# # print data['annotations']
# for obj in data['annotations']:
#     if obj['image_id'] == 203564:
#         print obj
#     # break

###############################################################

# import json

# file = "./dataset/train_data.json"
# data = json.load(open(file))

# for obj in data:
#     if obj['video'] == '54322086@N00_2408598493_274c77d26a.avi':
#         print obj['description']
#         print obj['times']
#         print
#     # break