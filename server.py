from flask import Flask, request
import pandas as pd
from bisect import bisect_left
import json
df1 = pd.read_csv('food_id.csv')
df2 = pd.read_csv('branded_food.csv',error_bad_lines=False, sep='delimiter', delimiter=";")




app = Flask(__name__)

@app.route('/<food>', methods=["POST"])

def index(food):
    user_input = request.args.get('food', default= "APPLE", type= str)
    print("SEEEEEE:")
    print(user_input)
    user_input=food
    print(user_input)
    upc_list=[]
    food_list=[]
    
    relevant_ingredients_list=[]
    df1['UPC']=df1['UPC'].astype(int, errors='ignore')
    for value in df1['UPC']:
        if(type(value)==int):
            upc_list.append(value)
    relevant_df=df1[df1['FoodName'].str.contains(str(user_input),na=False)]
    #upc_list=relevant_df['UPC'].to_list()
    length=len(upc_list)
   #print(type(upc_list[0]))
    
    
    if(length>6):
        length=6
    print("UPC LENGHT: "+str(length))
    gtinupc_list=[]
    food_list=relevant_df['FoodName'].to_list()
    df2['gtin_upc']=df2['gtin_upc'].astype(int, errors='ignore')
    for value in df2['gtin_upc']:
        if(type(value)==int):
            gtinupc_list.append(value)
    #gtinupc_list=df2['gtin_upc'].to_list()
    ingredients_list=df2['ingredients'].to_list()
    relevant_food_list=[]
    print(type(gtinupc_list[0]))
    
    #upc_list.str.replace('-','').astype(int)


    count=0

    for i in range(len(upc_list)):
        if(count<length):
            index=BinarySearch(gtinupc_list,upc_list[i])
            if(index!=-1):
                relevant_ingredients_list.append(ingredients_list[index])
                count+=1
                relevant_food_list.append(food_list[i])
        else:
            break
    

    
    print("hellllllooooo")
    print(count)
    
    
    if(len(relevant_food_list)==len(relevant_ingredients_list)):
        print("STUFFF")
        print(food_list)
        print(relevant_ingredients_list)
        my_dict=dict(zip(food_list,relevant_ingredients_list))
        return json.dumps(my_dict)
    else:
        print(len(food_list))
        print(food_list)
        print(len(relevant_ingredients_list))
        print(relevant_ingredients_list)
        return "no options available"
    

    
def BinarySearch(a, x):
    
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return -1

if __name__=='__main__':
    app.run(debug=True, port=1234)