
import json
import uuid
import logging
import os
import re
from urllib.parse import unquote

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'crud_items')
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    logger.info("Event: %s", json.dumps(event))
    # HTTP API v2 format: event['requestContext']['http']['method']
    method = None
    if 'requestContext' in event and 'http' in event['requestContext']:
        method = event['requestContext']['http'].get('method')
    else:
        method = event.get('httpMethod')

    path = event.get('rawPath') or event.get('path') or '/'
    query = event.get('queryStringParameters') or {}

    # POST /items     -> Create
    if method == 'POST' and path == '/items':
        body = json.loads(event.get('body') or '{}')
        if 'id' not in body:
            body['id'] = str(uuid.uuid4())
        table.put_item(Item=body)
        return respond(201, {"message": "Created", "item": body})

    # GET /items      -> List
    if method == 'GET' and path == '/items':
        if query.get('limit'):
            try:
                limit = int(query.get('limit'))
            except ValueError:
                limit = None
            resp = table.scan(Limit=limit) if limit else table.scan()
        else:
            resp = table.scan()
        items = resp.get('Items', [])
        return respond(200, {"items": items})

    # Match /items/{id}
    m = re.match(r'^/items/([^/]+)$', path)
    if m:
        item_id = unquote(m.group(1))

        # GET /items/{id} -> Read one
        if method == 'GET':
            resp = table.get_item(Key={'id': item_id})
            item = resp.get('Item')
            if not item:
                return respond(404, {"message": "Not Found"})
            return respond(200, item)

        # PUT /items/{id} -> Update partial fields
        if method == 'PUT':
            body = json.loads(event.get('body') or '{}')
            expr_names = {}
            expr_values = {}
            set_parts = []
            for k, v in body.items():
                if k == 'id':
                    continue
                expr_names[f"#{k}"] = k
                expr_values[f":{k}"] = v
                set_parts.append(f"#{k} = :{k}")
            if not set_parts:
                return respond(400, {"message": "No updatable fields"})
            update_expr = "SET " + ", ".join(set_parts)
            resp = table.update_item(
                Key={'id': item_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_values,
                ReturnValues="ALL_NEW"
            )
            return respond(200, {"message": "Updated", "item": resp.get('Attributes')})

        # DELETE /items/{id}
        if method == 'DELETE':
            table.delete_item(Key={'id': item_id})
            return {'statusCode': 204, 'headers': {'Content-Type': 'application/json'}, 'body': ''}

    # If nothing matched
    return respond(404, {"message": "Route Not Found"})


def respond(status_code, data):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(data)
    }
