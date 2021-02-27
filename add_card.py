import requests

URL = "https://api.trello.com/1"
GET = 'GET'
POST = 'POST'

KEY = ''
TOKEN = ''
ID_BOARD = ''

query = {
   'key': KEY,
   'token': TOKEN
}

def send_request(query, url, method):

    return requests.request(
        method,
        url,
        params=query
    )
    
def create_label():
    label_name = str(input("Enter label name: "))
    label_color = str(input("Enter label color: "))
    label_query = query
    label_query['name'] = label_name
    label_query['color'] = label_color
    label_query['idBoard'] = ''
    # create label
    send_request(label_query, URL + '/labels', POST)

def create_card():
    # get columns
    response = send_request(query, URL + '/boards/' + ID_BOARD + '/lists', GET)

    card_dict = {}
    col_dict = {}
    index = 1
    for card in list(response.json()):
        card_dict[index] = card['id']
        col_dict[index] = card['name']
        print(str(index) + '. ' + card['name'])
        index += 1

    col = int(input("Enter Column Number: "))
    cardname = str(input("Enter cardname: "))
    desc = str(input("Enter Description: "))
    comment = str(input("Enter comment: "))

    response = send_request(query, URL + '/boards/' + ID_BOARD + '/labels', GET)
    label_ids = []
    label_names = []
    label_dict = {}
    label_name_dict = {}

    print('Existing Labels:')
    index = 1
    for label in list(response.json()):
        label_dict[index] = label['id']
        label_name_dict[index] = label['name']
        print(str(index) + '. ' + label['name'] + ' - ' + label['color'])
        index += 1

    labels = str(input("Enter label numbers with comma(,) separated (e.g: 1,2,3): ")).split(',')

    for label in labels:
        label_names.append(label_name_dict.get(int(label)))
        label_ids.append(label_dict.get(int(label)))

    print('Preview: ')
    print("column is: " + col_dict[col])
    print("cardname is: " + cardname)
    print("desc is: " + desc)
    print("Comment is: " + comment)
    print("label name: " + str(label_names))

    card_query = query
    card_query['idList'] = card_dict[col]
    card_query['name'] = cardname
    card_query['desc'] = desc
    card_query['idLabels'] = label_ids

    # create card
    response = send_request(card_query, URL + '/cards', POST)
    card_id = response.json()['id']
    comment_query = query
    comment_query['text'] = comment

    # comments
    response = send_request(comment_query, URL + '/cards/' + card_id + '/actions/comments', POST)

print('1. Create Card')
print('2. Create Label')

option = str(input('Enter your choice: '))
if option == '1':
    create_card()
else:
    create_label()