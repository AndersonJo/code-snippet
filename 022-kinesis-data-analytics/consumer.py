from boto import kinesis as boto_kinesis


def main():
    kinesis = boto_kinesis.connect_to_region('us-east-2')

    shard_id = 'shardId-000000000000'  # Shard는 1개ch만 갖고 있음
    shard_it = kinesis.get_shard_iterator('AndersonStream', shard_id, 'LATEST')['ShardIterator']
    print('Latest Shard Iterator:', shard_it)

    while True:
        _out = kinesis.get_records(shard_it, limit=10)
        records = _out['Records']

        for r in records:
            print(r['Data'])

        shard_it = _out['NextShardIterator']
        if not records:
            break


if __name__ == '__main__':
    main()
