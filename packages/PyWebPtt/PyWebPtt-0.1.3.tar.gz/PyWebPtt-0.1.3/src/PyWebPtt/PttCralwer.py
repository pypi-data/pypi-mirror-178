import sys, getopt
sys.path.insert(0, '../') #家路徑，之前也有學過
from PttClient import PttClient, PttArticle, PttPush


argv = sys.argv[1:]
options = "l:f:"
long_option_list = ["link=", "floor="]
opt_and_args_tuples, values = getopt.getopt(argv, options, long_option_list) #很詭異，value是空的，但一定要寫，不然前者不是可以讀取的tuple
# print("opt_and_args_tuples= ", opt_and_args_tuples)

url = None
floor = None
for opt, arg in opt_and_args_tuples:
    if opt in ("-l", "--link"):
        url = arg
    elif opt in ("-f", "--floor"):
        floor = int(arg)

print("url=[", url, "], floor=[", floor, "]")
ptt_client = PttClient()
ptt_article = ptt_client.getPttArticle(url)

if floor == None:
    print(ptt_article.getHtml())
elif floor != None and url != None:
    print(ptt_article.getPttPush(floor))
