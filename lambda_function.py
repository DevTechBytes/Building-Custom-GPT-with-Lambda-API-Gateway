# Lambda function used by the API Gateway
import json, os, traceback, logging
from urllib import request
from urllib.parse import urlencode

def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    try:
        logger.debug(f"HTTP request {event}")
            
        if event['queryStringParameters'] is not None and event['queryStringParameters'].get('limit') is not None:
            limit = event['queryStringParameters']['limit']
        else:
            limit = 25
        
        query_params = {
          'q': event['queryStringParameters']["query"]
        }
        
        encoded_query_string = urlencode(query_params)
        
        api_key = f"key={os.environ["api_key"]}"
        
        query =f"{encoded_query_string}&page=1&per_page={limit}"
        
        api_call  = f"{os.environ['api_url']}?{api_key}&{query}"
        
        logger.debug(f"API Query {query}")
        
        headers = {'Content-Type': 'application/json'}
        
        req = request.Request(api_call, headers=headers)
        
        with request.urlopen(req) as response:
          response_body = response.read()
          
          response = json.loads(response_body)['hits']
          
          logger.debug(f"API Response {response}")
          
          return {
              'statusCode': 200,
              'body': json.dumps(response)
          }
    except Exception as e:
        logger.debug(traceback.print_exc())
        
        return {
            'statusCode': 500,
            'body': "There was a problem calling the API"
        }