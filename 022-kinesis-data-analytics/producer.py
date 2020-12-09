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
            'job': faker.job()}


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

    for _ in range(50):
        data = generate_data(faker)
        res = kinesis.put_record('AndersonStream', json.dumps(data), 'partitionkey' + str(random.choice([0, 1])))
        print('PUT', data)
        print('   ', res['SequenceNumber'], '\n')

    # kinesis.delete_stream('AndersonStream')


if __name__ == '__main__':
    main()
