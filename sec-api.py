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

def full_text_search(api_key, query, start_date=None, end_date=None, page=1):
    url = "https://api.sec-api.io/full-text-search"
    headers = {"Authorization": api_key}
    data = {
        "query": query,
        "startDate": start_date,
        "endDate": end_date,
        "page": page
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to perform full text search", "statusCode": response.status_code}

def main():
    parser = argparse.ArgumentParser(description="CLI for querying sec-api.io")
    parser.add_argument("api_key", help="Your API key for sec-api.io")
    subparsers = parser.add_subparsers(dest='command', help='commands')
    
    # Parser for the "query" command
    query_parser = subparsers.add_parser('query', help='Query general SEC data')
    query_parser.add_argument("query", help="Your query for the SEC data")

    # Parser for the "subsidiaries" command
    subs_parser = subparsers.add_parser('subsidiaries', help='Query SEC subsidiaries data')
    subs_parser.add_argument("query", help="Query for subsidiary details")
    subs_parser.add_argument("--from_index", type=int, default=0, help="Start position for subsidiary results")
    subs_parser.add_argument("--size", type=int, default=50, help="Number of results to return for subsidiaries")

    # Parser for the "full-text-search" command
    ft_parser = subparsers.add_parser('full-text-search', help='Full text search on filings')
    ft_parser.add_argument("query", help="Query for full text search on filings")
    ft_parser.add_argument("--start_date", help="Start date for filings search (yyyy-mm-dd)")
    ft_parser.add_argument("--end_date", help="End date for filings search (yyyy-mm-dd)")
    ft_parser.add_argument("--page", type=int, default=1, help="Page number for search results")

    args = parser.parse_args()

    if args.command == 'query':
        result = query_sec_api(args.api_key, args.query)
    elif args.command == 'subsidiaries':
        result = get_subsidiaries(args.api_key, args.query, args.from_index, args.size)
    elif args.command == 'full-text-search':
        result = full_text_search(args.api_key, args.query, args.start_date, args.end_date, args.page)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
