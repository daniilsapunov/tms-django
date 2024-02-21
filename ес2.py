import boto3

# Создание клиента EC2
ec2 = boto3.client('ec2')


def create_instance():
    # Создание экземпляра EC2
    response = ec2.run_instances(
        ImageId='ami-0014ce3e52359afbd',  # ID образа AMI
        InstanceType='t3.micro',  # Тип инстанса
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=['sg-01eac038c7783b187'],  # Список ID групп безопасности, default
        KeyName='drill',  # SSH
        BlockDeviceMappings=[
            {
                'DeviceName': '/dev/xvda',  # основной том
                'Ebs': {
                    'VolumeSize': 8  # Объем памяти в гигабайтах
                }
            }
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'PY93-Sapunov-EC2'  # Имя вашей виртуальной машины
                    },
                ]
            },
        ]
    )

    # Получение ID созданного экземпляра
    instance_id = response['Instances'][0]['InstanceId']

    print(f"Создан экземпляр EC2 с ID: {instance_id}")


def stop_vm():
    response = ec2.stop_instances(
        InstanceIds=[
            'i-030253c6f3661bf6b',
        ]
    )


def start_work_vm():

    # Идентификатор остановленного инстанса
    instance_id = 'i-030253c6f3661bf6b'

    # Запустите инстанс
    response = ec2.start_instances(InstanceIds=[instance_id])

    print(response)
stop_vm()
