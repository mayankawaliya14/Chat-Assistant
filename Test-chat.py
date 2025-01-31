import requests

URL = "https://chat-assistant-csr6.onrender.com/query"

queries = [
    "show me all employees in Sales department",
    "who is the manager of Engineering department?",
    "list all employees hired after 2020-06-10",
    "what is the total salary expense for Marketing department?",
    "show me all employees in HR department",
    "who is the manager of IT department?",
    "list all employees hired after 2023-01-01",
    "what is the total salary expense for Finance department?",
    "show me all employees in Operations department",
    "who is the manager of Sales department?",
    "list all employees hired after 2019-01-01",
    "what is the total salary expense for HR department?",
    "show me all employees in IT department",
    "who is the manager of Operations department?"
]

for query in queries:
    response = requests.post(URL, json={"query": query})
    print(f"Query: {query}")
    
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    
    print("-" * 50)
