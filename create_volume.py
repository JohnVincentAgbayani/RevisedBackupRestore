import boto3
import string

def create_vol(target_instance_id, target_snapshot_id):
	ec2_client = boto3.client("ec2")
	ec2_resource = boto3.resource('ec2')

	temp_device_names = []
	alphabet = list(string.ascii_lowercase)

	availabilty_zone = ec2_client.describe_instances(InstanceIds=[target_instance_id])['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone']
	snapshot_volume_id = ec2_client.describe_snapshots(SnapshotIds=[target_snapshot_id])['Snapshots'][0]["VolumeId"]
	volume_type = ec2_client.describe_volumes(VolumeIds=[snapshot_volume_id])["Volumes"][0]['VolumeType']

	new_volume_id = ec2_client.create_volume(AvailabilityZone=availabilty_zone, SnapshotId=target_snapshot_id, VolumeType=volume_type)['VolumeId']

	return new_volume_id