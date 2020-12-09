import json
import random
from time import sleep

from boto import kinesis as boto_kinesis
from faker import Faker


def generate_data(faker):
    return {'name': faker.name(),
            'age': random.randint(10, 20),
            'gender': random.choice(['M', 'F']),
            'score': random.choice(range(40, 70, 5)),
            'data': {'id': random.randint(0, 10000),
                     'type': random.choice(['a', 'b', 'c'])}}


def main():
    faker = Faker()
    kinesis = boto_kinesis.connect_to_region('us-east-2')
    print('Connected')

    if 'AndersonStream' not in kinesis.list_streams()['StreamNames']:
        kinesis.create_stream('AndersonStream', 1)
        print('AndersonStream Stream has been created')

        while True:
            sleep(1)
            print(kinesis.list_streams())
            if 'AndersonStream' in kinesis.list_streams()['StreamNames']:
                kinesis = boto_kinesis.connect_to_region('us-east-2')
                break
    i = 0
    while True:
        i += 1
        data = generate_data(faker)
        data['i'] = i
        res = kinesis.put_record('AndersonStream', json.dumps(data), 'partitionkey' + str(random.randint(0, 10)))
        print(f'{i:2}', data)
        print('   ', res, '\n')

    # kinesis.delete_stream('AndersonStream')


if __name__ == '__main__':
    main()
