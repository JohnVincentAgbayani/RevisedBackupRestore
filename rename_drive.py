import boto3
import time

def rename_os_drive(target_instance_id, target_volume_id):
	ec2_client = boto3.client("ec2")
	target_region = ec2_client.describe_instances(InstanceIds=[target_instance_id])['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'][:-1]

	ssm_file = open("rename_drive_ssm.json")
	ssm_json = ssm_file.read()

	ssm_doc_name = 'backup-restore-rename'
	ssm_client = boto3.client('ssm', region_name=target_region)

	ssm_create_response = ssm_client.create_document(Content = ssm_json, Name = ssm_doc_name, DocumentType = 'Command', DocumentFormat = 'JSON', TargetType =  "/AWS::EC2::Instance")

	ssm_run_response = ssm_client.send_command(InstanceIds = [target_instance_id], DocumentName=ssm_doc_name, DocumentVersion="$DEFAULT", TimeoutSeconds=120,  Parameters={'VolumeID':[target_volume_id]})
	print(f'{ssm_run_response}\n')
	cmd_id = ssm_run_response['Command']['CommandId']

	time.sleep(5)
	ssm_status_response = ssm_client.get_command_invocation(CommandId=cmd_id, InstanceId=target_instance_id)
	while ssm_status_response['StatusDetails'] == 'InProgress':
		time.sleep(5)
		ssm_status_response = ssm_client.get_command_invocation(CommandId=cmd_id, InstanceId=target_instance_id)

	print(ssm_status_response)

	ssm_delete_response = ssm_client.delete_document(Name=ssm_doc_name)
	print("Drive rename completed")