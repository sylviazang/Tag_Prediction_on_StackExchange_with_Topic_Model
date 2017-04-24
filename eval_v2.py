import os
import csv
from collections import OrderedDict
from nltk.stem.porter import PorterStemmer

n_topics = [1,3]
n_iters = [100,500,1000,1500,2000]
n_filter = ['all', 'cleaned']
# fields = ['biology', 'cooking', 'crypto', 'diy', 'robotics', 'travel']
fields = ['biology', 'crypto', 'diy', 'robotics', 'travel']

data = os.path.join(os.getcwd(), 'lda_result')
data_gt = os.path.join(os.getcwd(), 'lda_result', 'ground_truth')

def lemm(s):
	porter_stemmer = PorterStemmer()
	words_lemma = [porter_stemmer.stem(word) for word in s.split()]
	return words_lemma

def metric_accuracy(gt, pred):
	l_gt = lemm(gt)
	l_pred = lemm(pred)

	l_count = [1 if e in l_pred else 0 for e in l_gt]
	# print("gt: {} {} pred: {} {} l_count: {}".format(gt, l_gt, pred, l_pred,l_count))

	# if(len(l_count)==0):
	# 	accuracy = 0
	# else:
	# 	accuracy = l_count.count(1)/len(l_count)

	accuracy = l_count.count(1)/len(l_count)

	return accuracy

def get_d(file_gt, file_pred):
	# construct a dictionary, key being id, value being {'gt':gt[id], 'pred':pred[id]}
	with open(file_gt, 'r', encoding='utf-8') as i:
		gt_reader = csv.DictReader(i)

		# counter = 0
		# gt_d = OrderedDict()
		# for row in gt_reader:
		# 	# if(counter > 1999):
		# 	# 	break
		# 	print(row)
		# 	gt_d[row['id']] = row['tags']
			# counter += 1


		gt_d = {row['id']:row['tags'] for row in gt_reader}
		n_entries = len(gt_d)

	# with open(file_pred, 'r') as i:
	with open(file_pred, 'r', encoding='utf-8') as j:
		pred_reader = csv.DictReader(j)

		pred_d = OrderedDict()
		for row in pred_reader:
			if('topic_words' in row):
				pred_d[row['doc']] = row['topic_words']
			else:
				pred_d[row['doc']] = row['cleaned_topic_words']

		# pred_d = {row['doc']:row['topic_words'] for row in pred_reader}

		if(len(pred_d)!=n_entries):
			print("{} doesn't have the same number of files as {}".format(file_gt, file_pred))

	# print(len(gt_d), len(pred_d))


	compare_d = {}
	for ID in gt_d.keys():
		compare_d[ID] = {'gt':gt_d[ID], 'pred':pred_d[ID]}

	return compare_d

def compare(compare_d, metric):
	accuracy = []
	for ID in compare_d.keys():
		accuracy.append(metric(compare_d[ID]['gt'], compare_d[ID]['pred']))
	avg_accuracy = sum(accuracy)/len(accuracy)
	return avg_accuracy

def output(i,j,k,l,result):
	# print("topic {} - iters {} - filter - {} field - {} 's evaluation result: {}".format(i,j,k,l,result))
	with open('eval_result.csv', 'a') as o:
		writer = csv.DictWriter(o, fieldnames=['topic', 'iters', 'filter', 'field', 'result'])
		writer.writerow({'topic':i, 'iters':j, 'filter':k, 'field':l, 'result':result})

def run_evaluation():
	with open('eval_result.csv', 'w') as o:
		writer = csv.DictWriter(o, fieldnames=['topic', 'iters', 'filter', 'field', 'result'])
		writer.writeheader()	
	for i in n_topics:
		for j in n_iters:
			for k in n_filter:
				for l in fields:
					file_gt = os.path.join(data_gt, "{}.csv".format(l))
					file_pred = os.path.join(data, "iter{}_topic{}".format(j,i), "{}_{}.csv".format(l, k))
					
					print("topic {} - iters {} - filter - {} field - {}".format(i,j,k,l))

					compare_d = get_d(file_gt, file_pred)
					result = compare(compare_d, metric_accuracy)
					output(i,j,k,l,result)


if __name__ == '__main__':
	run_evaluation()