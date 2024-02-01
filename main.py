import boto3
import json
import os

from create_volume import create_vol
from attach_volume import attach_vol
from rename_drive import rename_os_drive

region_lookup = {
					"USEA":"us-east-1",
					"USWE":"us-west-1",
					"CACE":"ca-central-1",
					"EUWE":"eu-west-1",
					"EUCE":"eu-central-1",
					"APSP":"ap-southeast-1",
					"APAU":"ap-southeast-2"
				}

target_action = "attach"

target_snapshot_id = os.environ["Snapshot ID"]
sctask_number = os.environ["SCTASK Number"].lower().replace('sctask','')
target_instance = os.environ["Instance Name"].strip()
target_region = region_lookup[target_instance[:4].upper()]

ec2_client = boto3.client("ec2", region_name = target_region)
target_instance_id = ec2_client.describe_instances(Filters=[{'Name':'tag:Name', 'Values':[target_instance]}])['Reservations'][0]['Instances'][0]['InstanceId']


if target_action == 'attach':
	target_volume_id = create_vol(target_instance_id, target_snapshot_id, sctask_number, target_region)
	attachment_response = attach_vol(target_instance_id, target_volume_id, target_region)

	if attachment_response[0]:
		target_drive_letter = rename_os_drive(target_instance_id, target_volume_id, sctask_number, target_region).replace('\n','')
		target_device_name = attachment_response[1]['Device']

		print("\n========================================")
		print("ATTACHMENT INFORMATION SUMMARY")
		print("========================================")
		print(f'Volume ID: {target_volume_id}')
		print(f'Device Name: {target_device_name}')
		print(f'Drive Letter: {target_drive_letter}')
		print(f'Drive Name: {sctask_number} ({target_volume_id})')
		print('\nIMPORTANT! Please provide the information specified above in the ServiceNow case\n')
	else:
		print(f'\nERROR: Devices from xvdf to xvdp are already occupied. No more slots are available on the server.\n')

elif target_action == "detach":
	print('workflow to detach volume')