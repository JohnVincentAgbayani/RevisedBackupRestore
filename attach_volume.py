import boto3
import string

def attach_vol(target_instance_id, target_volume_id, target_region):
	ec2_client = boto3.client("ec2", region_name = target_region)
	
	attached = False

	volume_attachment_response = ""
	device_slots = list(string.ascii_lowercase)[5:16]
	

	for item in device_slots:
		target_device_name = f'xvd{item}'

		if not attached:
			try:
				volume_attachment_response = ec2_client.attach_volume(Device=target_device_name, InstanceId=target_instance_id, VolumeId=target_volume_id)
			except Exception as e: 
				if 'is already in use' in str(e):
					continue
				else:
					print(str(e))
					
			finally:
				if volume_attachment_response:
					attached = True
		

	return attached