import boto3
import json

from create_volume import create_vol
from attach_volume import attach_vol
from rename_drive import rename_os_drive

sample_data = {"action":"attach", "snapshot_id":"snap-09d8559257f009973", "instance_id":"i-0e0ef4b5f42929f4e"}
attach_type = "ami"

target_instance_id = sample_data['instance_id']
target_snapshot_id = sample_data['snapshot_id']
target_action = sample_data['action']

if target_action == 'attach':
	attach_type = attach_type

	if attach_type == 'ami':
		target_volume_id = create_vol(target_instance_id, target_snapshot_id)
		print(f'New volume {target_volume_id} has been created from {target_snapshot_id}')

		attachment_response = attach_vol(target_instance_id, target_volume_id)
		print(attachment_response)

		rename_os_drive(target_instance_id, target_volume_id)