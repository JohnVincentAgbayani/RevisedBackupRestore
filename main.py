import boto3
import json
import os

from create_volume import create_vol
from attach_volume import attach_vol
from rename_drive import rename_os_drive

attach_type = "ami"
target_action = "attach"

target_instance_id = os.environ["Instance ID"]
target_snapshot_id = os.environ["Snapshot ID"]
target_region = os.environ["Region"]
sctask_number = os.environ["SCTASK Number"].lower().replace('sctask','')


if target_action == 'attach':
	attach_type = attach_type

	if attach_type == 'ami':
		target_volume_id = create_vol(target_instance_id, target_snapshot_id, target_region)
		print(f'\nNew volume {target_volume_id} has been created from {target_snapshot_id}\n')

		attachment_response = attach_vol(target_instance_id, target_volume_id, target_region)
		if attachment_response:
			rename_os_drive(target_instance_id, target_volume_id, sctask_number, target_region)
			print(f'\nAttached drive name is: {sctask_number} ({target_volume_id})\n')
		else:
			print(f'\nERROR: Devices from xvdf to xvdp are already occupied. No more slots are available on the server.\n')