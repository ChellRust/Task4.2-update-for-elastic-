from elasticsearch import Elasticsearch

#Elasticsearch quaries
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="

#Initializization of the database
client = Elasticsearch(url, api_key=api_key)

#Creating new index or not if exist
def mydb():
        response = client.indices.create(index="mydb") 
        if response.meta.status == 200:  
            print('Index created')
        else:
            print('Index possible exists:')


if __name__ == '__main__': #This part gives opportunity to execute automatically in the same time with main code
    mydb()
