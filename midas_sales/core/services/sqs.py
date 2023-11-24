import boto3

from midas_sales.config import settings

sqs = boto3.resource(
    "sqs",
    region_name=settings.aws_region_name,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)

queue = sqs.get_queue_by_name(QueueName='sendEmail.fifo')


def add_task(tenant_id):
    return queue.send_message(MessageGroupId="2",
                              MessageDeduplicationId="2",
                              MessageBody=str(tenant_id))
