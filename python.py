# with open('data.json', 'rb') as file:
#     content = file.read()

# # Reinterpretar el contenido como UTF-8 y eliminar cualquier BOM si está presente
# content = content.decode('utf-16').encode('utf-8')

# with open('data_utf8.json', 'wb') as file:
#     file.write(content)
from google.cloud import storage

client = storage.Client.from_service_account_json('credenciales/orquideas-432422-e8f2f67257bb.json')
buckets = list(client.list_buckets())
print(buckets)
## FUNCIONO