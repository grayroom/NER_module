import json
import model
import os

from kafka import KafkaConsumer, KafkaProducer
from model import DistilbertNER

from crud import CRUD


print('initializing...')
consumer = KafkaConsumer('hello.kafka', bootstrap_servers=str(os.environ['KAFKA_HOST']) + ":" + str(os.environ['KAFKA_PORT']),
                         value_deserializer=lambda x: json
                         .loads(x.decode('utf-8')))

ner_model = model.NLPmodule()
diag_database = CRUD()
print('done!')

for message in consumer:
    print(message)
    # for every element in message.value, run the get_ner_token method and
    # insert into json object
    res = {}
    for idx, paragraph in enumerate(message.value['emr']):
        tagging, pr, te, tr = ner_model.get_ner_token(paragraph)
        # insert the result into temporal json object
        res[idx] = {
            'tagging': tagging,
            'pr': pr,
            'te': te,
            'tr': tr
        }

    # # parse pr, te, tr to json
    tags = json.dumps(res)
    # tags = "\\'".join(tags.split("'"))
    diag_database.update_db(table='api_nerhistory',
                            colum='ner_result', value=str(tags),
                            targ='id', condition=message.value['uuid'])

    diag_database.update_db(table='api_nerhistory',
                            colum='updated_time', value='now()',
                            targ='id', condition=message.value['uuid'])
    print(message.value['uuid'], 'updated')
