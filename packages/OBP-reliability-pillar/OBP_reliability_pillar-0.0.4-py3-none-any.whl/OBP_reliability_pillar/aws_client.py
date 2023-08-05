from OBP_reliability_pillar import compliance_functions as comp
from boto3 import session


class aws_client:
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.session = session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    get_compliance = comp.get_compliance
    get_autoscaling_compliance = comp.autoscaling_compliance
    get_s3_compliance = comp.s3_compliance
    get_rds_compliance = comp.rds_compliance
    get_ec2_compliance = comp.ec2_compliance



