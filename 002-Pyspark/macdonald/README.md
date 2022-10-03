# 1. Tutorial

## 1.1 Preparation 

S3 Bucket 하나 만들고, mcdonalds_dataset.csv 업로드 합니다.<br>
예제에서의 S3 Bucket 이름은 data-emr-tutorial입니다. 

```bash
$ aws s3 cp mcdonalds_dataset.csv s3://data-emr-tutorial/data/
$ aws s3 ls data-emr-tutorial/data/
```

## 1.2 Run Script 

