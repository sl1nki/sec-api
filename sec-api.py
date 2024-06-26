import requests
import argparse
import json

def query_sec_api(api_key, query):
    url = "https://api.sec-api.io"
    headers = {"Authorization": api_key}
    data = {"query": query, "format": "json"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data", "statusCode": response.status_code}

def get_subsidiaries(api_key, query, from_index=0, size=50, sort=None):
    url = "https://api.sec-api.io/subsidiaries"
    headers = {"Authorization": api_key}
    sort = sort if sort else [{"filedAt": {"order": "desc"}}]
    data = {
        "query": query,
        "from": from_index,
        "size": size,
        "sort": sort
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch subsidiary information", "statusCode": response.status_code}

def main():
    parser = argparse.ArgumentParser(description="CLI for querying sec-api.io")
    parser.add_argument("api_key", help="Your API key for sec-api.io")
    parser.add_argument("--query", help="Your query for the SEC data")
    parser.add_argument("--subsidiary-query", help="Query to get subsidiary details")
    parser.add_argument("--from-index", type=int, default=0, help="Start position for subsidiary results")
    parser.add_argument("--size", type=int, default=50, help="Number of results to return for subsidiaries")
    args = parser.parse_args()

    if args.query:
        result = query_sec_api(args.api_key, args.query)
    elif args.subsidiary_query:
        result = get_subsidiaries(args.api_key, args.subsidiary_query, args.from_index, args.size)
    else:
        result = {"error": "No action specified"}
    
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()

