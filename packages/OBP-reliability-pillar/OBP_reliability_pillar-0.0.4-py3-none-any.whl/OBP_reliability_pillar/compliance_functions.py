# Enters details to res
def insert_to_res(res, Id: str, r_type: str, c_type: str, compliance: str, description=None) -> dict:
    if compliance == '':
        compliance = None
    res.setdefault('Resource Id', []).append(Id)
    res.setdefault('Resource Type', []).append(r_type)
    res.setdefault('Compliance Type', []).append(c_type)
    res.setdefault('Compliance', []).append(compliance)
    res.setdefault('Description', []).append(description)
    return res


# extend res
def extend_res(res: dict, obj: list) -> dict:
    for ob in obj:
        if ob is None:
            continue
        res.setdefault('Resource Id', []).extend(ob['Resource Id'])
        res.setdefault('Resource Type', []).extend(ob['Resource Type'])
        res.setdefault('Compliance Type', []).extend(ob['Compliance Type'])
        res.setdefault('Compliance', []).extend(ob['Compliance'])
        res.setdefault('Description', []).extend(ob['Description'])
    return res


# EC2 compliance
def ec2_compliance(self) -> dict:
    client = self.session.client('ec2')
    res = {}
    marker = ''
    while True:
        response = client.describe_instances(
            MaxResults=1000,
            NextToken=marker
        )
        for i in response['Reservations'][0]['Instances']:
            com = i['Monitoring']['State']
            if com == 'enabled':
                res = insert_to_res(res, i['InstanceId'], 'EC2 Instance', 'Instance Detailed Monitoring Enabled',
                              'Compliant')
            else:
                res = insert_to_res(res, i['InstanceId'], 'EC2 Instance', 'Instance Detailed Monitoring Enabled',
                              'Not Compliant')

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break

    return res if res else None


# Check RDS compliance
def rds_compliance(self) -> dict:
    client = self.session.client('rds')
    res = {}

    def automatic_minor_version_enabled(i, r) -> dict:
        com = i['AutoMinorVersionUpgrade']
        if com:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Automatic Minor Version Enabled',
                          'Compliant')
        else:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Automatic Minor Version Enabled',
                          'Non Compliant')
        return r

    def instance_backup_enabled(i, r) -> dict:
        com = i['AutoMinorVersionUpgrade']
        if com:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Backup Enabled',
                          'Compliant')
        else:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Backup Enabled',
                          'Not Compliant')
        return r

    def instance_deletion_protection_enabled(i, r) -> dict:
        com = i['DeletionProtection']
        if com:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Deletion Protection Enabled',
                          'Compliant')
        else:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Deletion Protection Enabled',
                          'Not Compliant')
        return r

    def multi_az_support_enabled(i, r) -> dict:
        com = i['MultiAZ']
        if com:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Multi AZ support',
                          'Compliant')
        else:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Instance Multi AZ support',
                          'Not Compliant')
        return r

    def enhanced_monitoring_enable(i, r) -> dict:
        monitoring_interval = int(i['MonitoringInterval'])
        if monitoring_interval > 0:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Enhanced Monitoring Enabled',
                          'Compliant')
        else:
            r = insert_to_res(r, i['DBInstanceIdentifier'], 'RDS Instance', 'RDS Enhanced Monitoring Enabled',
                          'Not Compliant')
        return r

    marker = ''
    while True:
        response = client.describe_db_instances(
            MaxRecords=100,
            Marker=marker
        )
        for instance in response['DBInstances']:
            res = automatic_minor_version_enabled(instance, res)
            res = instance_backup_enabled(instance, res)
            res = instance_deletion_protection_enabled(instance, res)
            res = multi_az_support_enabled(instance, res)
            res = enhanced_monitoring_enable(instance, res)

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break
    return res if res else None


# Check S3 Compliance
def s3_compliance(self) -> dict:
    client = self.session.client('s3')
    response = client.list_buckets()
    res = {}

    def bucket_versioning(r: dict, bucket_name: str) -> dict:
        try:
            resp = client.get_bucket_versioning(
                Bucket=bucket_name,
            )
            status = resp['Status']
            if status == 'Enabled':
                r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Versioning Enabled',
                              'Compliant', 'Configuration found, status="enabled"')
            else:
                r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Versioning Enabled',
                              'Not Compliant', 'Configuration found, status="Disabled"')
        except:
            r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Versioning Enabled',
                          'Not Compliant', 'Configuration Not found')
        return r

    def bucket_replication(r: dict, bucket_name: str) -> dict:
        try:
            resp = client.get_bucket_replication(
                Bucket=bucket_name
            )

            status = resp['ReplicationConfiguration']['Rules'][0]['Status']
            if status == 'Enabled':
                r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Replication Enabled',
                                  'Compliant', 'Configuration Found, stats="Enabled"')
            else:
                r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Replication Enabled',
                                  'Not Compliant', 'Configuration found, status="Disabled"')
        except:
            r = insert_to_res(r, bucket['Name'], 'S3 Bucket', 'Bucket Replication Enabled',
                              'Not Compliant', 'Configuration Not found')
        return r

    for bucket in response['Buckets']:
        res = bucket_versioning(res, bucket['Name'])
        res = bucket_replication(res, bucket['Name'])

    return res if res else None


# combines all compliance details and return
def autoscaling_compliance(self) -> dict:
    client = self.session.client('autoscaling')
    res = {}

    def asg_elb_healthcheck_required(group, r) -> dict:
        if group['HealthCheckType'] == 'ELB':
            r = insert_to_res(r, group['AutoScalingGroupName'],
                          'Auto Scaling Group',
                          'Auto Scaling Group ELB health check required',
                          'Compliant')
        else:
            r = insert_to_res(r, group['AutoScalingGroupName'],
                          'Auto Scaling Group',
                          'Auto Scaling Group ELB health check required',
                          'Not Compliant')
        return r

    marker = ''
    while True:
        if marker == '':
            response = client.describe_auto_scaling_groups(
                MaxRecords=100
            )
        else:
            response = client.describe_auto_scaling_groups(
                NextToken=marker,
                MaxRecords=100
            )
        for asg in response['AutoScalingGroups']:
            res = asg_elb_healthcheck_required(asg, res)

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break
    return res if res else None


def get_compliance(self) -> dict:
    res = {}

    comp_lst = [
        ec2_compliance(self),
        rds_compliance(self),
        s3_compliance(self),
        autoscaling_compliance(self),
    ]
    # print(str(comp_lst))
    res = extend_res(res, comp_lst)

    return res
# end of the code
