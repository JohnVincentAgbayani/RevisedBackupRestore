import boto3
import string

def create_vol(target_instance_id, target_snapshot_id, sctask_number, target_region):
	ec2_client = boto3.client("ec2", region_name = target_region)
	ec2_resource = boto3.resource('ec2', region_name = target_region)

	temp_device_names = []
	alphabet = list(string.ascii_lowercase)

	availabilty_zone = ec2_client.describe_instances(InstanceIds=[target_instance_id])['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
	snapshot_volume_id = ec2_client.describe_snapshots(SnapshotIds=[target_snapshot_id])['Snapshots'][0]["VolumeId"]
	volume_type = ec2_client.describe_volumes(VolumeIds=[snapshot_volume_id])["Volumes"][0]['VolumeType']

	new_volume_id = ec2_client.create_volume(AvailabilityZone=availabilty_zone, SnapshotId=target_snapshot_id, VolumeType=volume_type)['VolumeId']
	ec2_client.create_tags(Resources=[new_volume_id], Tags=[{'Key':'AutoRestore','Value':'True'}, {'Key':'SCTASK','Value':sctask_number}])

	return new_volume_id