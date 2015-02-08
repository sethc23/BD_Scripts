from ebaysdk import finding, tag, nodeText

'''
findCompletedItems 	Retrieves items whose listings are completed and are no longer available for sale on eBay. 	view

findItemsAdvanced 	Finds items by a keyword query and/or category and allows searching within item descriptions. 	view

findItemsByCategory 	Finds items in a specific category. Results can be filtered and sorted. 	view

findItemsByImage 	Find items based on their image similarity to the specified item. 	view

findItemsByKeywords 	Finds items on eBay based upon a keyword query and returns details for matching items. 	view

findItemsByProduct 	Finds items based upon a product ID, such as an ISBN, UPC, EAN, or ePID. 	view

findItemsIneBayStores 	Finds items in eBay stores. Can search a specific store or can search all stores with a keyword query. 	view

getHistograms 	Gets category and/or aspect metadata for the specified category.

getSearchKeywordsRecommendation 	Checks specified keywords and returns correctly spelled keywords for best search results.

getVersion 	Returns the current service version.
'''
f = finding()
g = {"CategorySiteID" : '0',
"CategoryParent" : '',
"LevelLimit"  :  '',
"ViewAllNodes"  : 'True', }

f.execute('GetCategories', g)
# f.execute('findItemsAdvanced', tag('keywords', 'shoes'))        


dom = f.response_dom()
mydict = f.response_dict()

# shortcut to response data
print f.v('itemSearchURL')

# process the response via DOM
items = dom.getElementsByTagName('item')

for item in items:
  print nodeText(item.getElementsByTagName('title')[0])
  
