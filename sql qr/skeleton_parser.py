
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            parse_category(item)
            parse_location(item)
            parse_user(item)
            parse_item(item)
            parse_bid(item)

Category = {}
Bid = []
Location = {}
User = []
Item = []
Includes = []
def parse_category(item):
    for i in item['Category']:
        if i not in Category: 
            Category[i] = len(Category) + 1

def parse_location(item):
    if  'Location' in item:
        location_helper(item)
    if item['Bids'] is None: 
        return
    for bid in item['Bids']: 
        bidder = bid['Bid']['Bidder']
        if 'Location' in bidder:
            location_helper(bidder)
def location_helper(item):
    if item['Location'] not in Location:
        country_name="NULL"
        if "Country" in item:
            country_name=item["Country"]
        Location[item['Location']] = (len(Location) + 1,country_name)

def parse_user(item): 
    item['Seller']['Location'] = item['Location']
    user_helper(item['Seller'])
    if item['Bids'] is None:
        return
    for bid in item['Bids']: 
        user_helper(bid['Bid']['Bidder'])

def user_helper(user):
    loc="NULL"
    if 'Location' in user:
        loc=str(Location[user['Location']][0])
    temp='"'+'"|"'.join([user['UserID'],user['Rating'],loc])+'"\n'
    if temp not in User:
        User.append(temp)
        
def parse_item(item):
    item_id = item['ItemID']
    name = item['Name'].replace('"', '""')
    currently = transformDollar(item['Currently'])
    buy_price='NULL'
    if "Buy_Price" in item:
        buy_price = transformDollar(item['Buy_Price'])
    first_bid = transformDollar(item['First_Bid'])
    number_of_bids = item['Number_of_Bids']
    started = transformDttm(item['Started'])
    ends = transformDttm(item['Ends'])
    seller_id=item["Seller"]["UserID"]
    description=""
    if item['Description'] is not None:
        description = item['Description'].replace('"', '""')
    Item.append('"' + '"|"'.join([item_id, name, currently, buy_price, first_bid, number_of_bids, started, ends,seller_id, description]) + '"\n')
    for i in item['Category']:
        Includes.append(item['ItemID'] + '|' + str(Category[i]) + '\n')
def parse_bid(item):
    if item['Bids'] is None:
        return
    for bid in item['Bids']: 
        bid_id  = str(len(Bid) + 1)
        i = bid['Bid']['Bidder']['UserID'] + '|'+ item['ItemID']+'|'+transformDttm(bid['Bid']['Time']) + '|'+transformDollar(bid['Bid']['Amount'])
        Bid.append(bid_id + '|' + i + '\n')
def convert_location():
    temp=""
    toreturn=[]
    for location in Location:
        temp=str(Location[location][0])+'|'+location+'|'+Location[location][1]+'\n'
        toreturn.append(temp)
    returnstr='"'+"".join(toreturn).replace('"','""').replace('|','"|"').replace('\n','"\n"')[:-1]
    return returnstr
def convert_category():
    temp=""
    toreturn=[]
    for category in Category:
        temp=str(Category[category])+'|'+category+'\n'
        toreturn.append(temp)
    return "".join(toreturn)
        
 
    
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f
    with open("Category.dat","w") as f:
        f.write(convert_category())

    with open("Location.dat","w") as f: 
        f.write(convert_location())

    with open("User.dat","w") as f: 
        f.write("".join(User))
    with open("Item.dat","w") as f: 
        f.write("".join(Item)) 
    
    Includeso=list(dict.fromkeys(Includes))
    with open("Includes.dat","w") as f: 
        f.write("".join(Includeso)) 
    
    with open("Bid.dat","w") as f: 
        f.write("".join(Bid))

if __name__ == '__main__':
    main(sys.argv)
