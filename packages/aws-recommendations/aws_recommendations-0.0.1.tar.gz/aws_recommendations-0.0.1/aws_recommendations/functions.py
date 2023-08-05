from dateutil.relativedelta import relativedelta
import datetime as dt
import pytz


# Enters details to recommendations
def insert_to_rec(self, service_name: str, Id: str, recommendation: str, desc=''):
    if desc == '':
        desc = None
    self.recommendation.setdefault('Service Name', []).append(service_name)
    self.recommendation.setdefault('Id', []).append(Id)
    self.recommendation.setdefault('Recommendation', []).append(recommendation)
    self.recommendation.setdefault('Description', []).append(desc)


# returns the list of instances
def list_instances(self) -> list:
    client = self.session.client('ec2')
    instance_lst = []
    marker = ''
    while True:
        response = client.describe_instances(
            MaxResults=1000,
            NextToken=marker
        )
        for i in response['Reservations']:
            for instance in i['Instances']:
                state = instance['State']['Name']
                if not state == 'terminated':
                    instance_lst.append(instance['InstanceId'])

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break

    return instance_lst


# returns the list of rds instances
def list_rds_instances(self) -> list:
    client = self.session.client('rds')

    rds_instance_lst = []
    marker = ''
    while True:
        response = client.describe_db_instances(
            MaxRecords=100,
            Marker=marker
        )
        for instance in response['DBInstances']:
            rds_instance_lst.append(instance['DBInstanceIdentifier'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break
    return rds_instance_lst


# returns the metrics data
def get_metrics_stats(self, namespace: str, dimensions: list,
                      metric_name='CPUUtilization', start_time=dt.datetime.utcnow() - relativedelta(days=7),
                      end_time=dt.datetime.utcnow(), period=86400, stats=None, unit='Percent'):
    if stats is None:
        stats = ["Average"]

    client = self.session.client('cloudwatch')
    response_cpu = client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=stats,
        Unit=unit,
        Dimensions=dimensions
    )
    return response_cpu


# Generates recommendation to delete idle instances
def del_idle_instance_recommendation(self) -> list:
    recommendation = []
    cpu_stats = {}
    # mem_stats = {}
    # netin_stats = {}
    # netout_stats = {}

    instance_lst = list_instances(self)

    for instance in instance_lst:
        response_cpu = get_metrics_stats(self, "AWS/EC2", [{'Name': 'InstanceId', 'Value': instance}])
        # response_mem = get_metics_stats(session, region, "AWS/EC2", {'Name': 'InstanceId', 'Value': instance},
        # metric_name=) response_net_in = get_metrics_stats(region, "AWS/EC2", [{'Name': 'InstanceId',
        # 'Value': instance}], metric_name='NetworkIn') response_net_out = get_metrics_stats(region, "AWS/EC2",
        # [{'Name': 'InstanceId', 'Value': instance}], metric_name='NetworkOut') # print(response_net_in) print(
        # response_net_out) for r in response_net_in['Datapoints']: print(r['Average'])

        tmp_lst_cpu = []

        for r in response_cpu['Datapoints']:
            tmp_lst_cpu.append(r['Average'])

        cpu_stats[instance] = tmp_lst_cpu

    for key, value in cpu_stats.items():
        if len(value) < 7:
            # temp = {
            #     'Service Name': 'EC2 Instance',
            #     'Id': key,
            #     'Recommendation': 'Insufficient Data'
            # }
            # recommendation.append(temp)
            continue
        if max(value) < 3:
            insert_to_rec(self, 'EC2 Instance', key, 'Delete idle compute instance', '')
            # temp = {
            #     'Service Name': 'EC2 Instance',
            #     'Id': key,
            #     'Recommendation': 'Delete idle compute instance',
            #     'Description': ''
            # }
            # recommendation.append(temp)

        else:
            avg = 0
            for v in value:
                avg = avg + v
            avg = avg / len(value)

            if avg < 5:
                insert_to_rec(self, 'EC2 Instance', key, 'Downsize underutilized compute instances', '')
                # temp = {
                #     'Service Name': 'EC2 Instance',
                #     'Id': key,
                #     'Recommendation': 'Downsize underutilized compute instances',
                #     'Description': ''
                # }
                # recommendation.append(temp)

    # return recommendation


# generates the recommendation to delete unattached volumes
def purge_unattached_vol_recommendation(self) -> list:
    vol_data = {}
    # recommendation = []
    client = self.session.client('ec2')
    marker = ''
    while True:
        response = client.describe_volumes(
            MaxResults=500,
            NextToken=marker
        )
        for item in response['Volumes']:
            create_time = item['CreateTime']
            datetime_4_weeks_ago = dt.datetime.now() - dt.timedelta(weeks=4)
            timezone = pytz.timezone("UTC")
            datetime_4_weeks_ago = timezone.localize(datetime_4_weeks_ago)

            older = create_time <= datetime_4_weeks_ago
            if older:
                vol_data[item['VolumeId']] = item['Attachments']

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break

    for key, value in vol_data.items():
        if len(value) == 0:
            insert_to_rec(self, 'Volume', key, 'Purge unattached volume', '')
            # temp = {
            #     'Service Name': 'Volume',
            #     'Id': key,
            #     'Recommendation': 'Purge unattached volume',
            #     'Description': ''
            # }
            # recommendation.append(temp)
        # else:
        # temp = {
        #     'Service Name': 'Volume',
        #     'Id': key,
        #     'Recommendation': None
        # }
        # recommendation.append(temp)
    # return recommendation


# Generates the recommendation to downsize underutilized rds instance
def downsize_underutilized_rds_recommendation(self) -> list:
    # recommendation = []
    rds_instance_lst = list_rds_instances(self)

    for instance in rds_instance_lst:
        cpu_stats = get_metrics_stats(
            self, namespace='AWS/RDS',
            dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': instance}]
        )

        if len(cpu_stats['Datapoints']) < 7:
            # temp = {
            #     'Service Name': 'RDS Instance',
            #     'Id': instance,
            #     'Recommendation': 'Insufficient Data'
            # }
            # recommendation.append(temp)
            continue

        flag = True
        for points in cpu_stats['Datapoints']:
            if points['Average'] > 30:
                flag = False
                break

        if flag:
            insert_to_rec(self, 'RDS', instance, 'Downsize underutilized rds instance', '')
            # temp = {
            #     'Service Name': 'RDS Instance',
            #     'Id': instance,
            #     'Recommendation': 'Downsize underutilized rds instance',
            #     'Description': ''
            # }
            # recommendation.append(temp)
        # else:
        # temp = {
        #     'Service Name': 'RDS Instance',
        #     'Id': instance,
        #     'Recommendation': None
        # }
        # recommendation.append(temp)

    # return recommendation


# Generates the recommendation to purge the snapshots which are older than 8 weeks
def purge_8_weeks_older_snapshots(self) -> list:
    recommendation = []
    datetime_8_weeks_ago = dt.datetime.now() - dt.timedelta(weeks=8)
    timezone = pytz.timezone("UTC")
    datetime_8_weeks_ago = timezone.localize(datetime_8_weeks_ago)
    client = self.session.client('ec2')
    marker = ''
    while True:
        response = client.describe_snapshots(
            MaxResults=1000,
            OwnerIds=['self'],
            NextToken=marker
        )
        for snapshot in response['Snapshots']:
            start_time = snapshot['StartTime']
            older = start_time <= datetime_8_weeks_ago

            if older:
                insert_to_rec(self, 'Snapshot', snapshot['SnapshotId'], 'Purge 8 week older snapshot', '')
                # temp = {
                #     'Service Name': 'Snanshot',
                #     'Id': snapshot['SnapshotId'],
                #     'Recommendation': 'Purge 8 week older snapshot',
                #     'Description': ''
                # }
                # recommendation.append(temp)

        try:
            marker = response['NextToken']
            if marker == '':
                break
        except KeyError:
            break
    # return recommendation


# Generic Suggestions
def get_generic_suggestions(self):
    insert_to_rec(self, 'Volume', 'Generic', 'Move GP2 volumes to GP3')
    insert_to_rec(self, 'EC2', 'Generic', 'Use m5 or t3 rather than m3', 'Consider using m5 or t3 family instead of m3 '
                                                                         'as m3 is older generation '
                                                                         'and expensive as compared to latest '
                                                                         'generation')


# Merge the recommendations and return the list
def get_recommendations(self) -> list:
    del_idle_instance_recommendation(self)
    purge_unattached_vol_recommendation(self)
    downsize_underutilized_rds_recommendation(self)
    purge_8_weeks_older_snapshots(self)
    get_generic_suggestions(self)

    return self.recommendation
