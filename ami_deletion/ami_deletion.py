import boto3

def deregister_ami_and_delete_snapshots(ami_id, session):
    ec2 = session.client('ec2')
    
    # Describe the AMI to obtain the associated snapshots
    response = ec2.describe_images(ImageIds=[ami_id])
    
    if not response['Images']:
        print(f'AMI {ami_id} not found.')
        return
    
    image = response['Images'][0]
    block_mappings = image.get('BlockDeviceMappings', [])
    
    snapshot_ids = []
    
    # Get the associated snapshots
    for block in block_mappings:
        if 'Ebs' in block and 'SnapshotId' in block['Ebs']:
            snapshot_ids.append(block['Ebs']['SnapshotId'])

    # Deregistrer the AMI
    print(f'Deregistering AMI {ami_id}...')
    ec2.deregister_image(ImageId=ami_id)
    
    # Delete the associated snapshots
    for snapshot_id in snapshot_ids:
        print(f'Deleting snapshot {snapshot_id} associated with the AMI {ami_id}...')
        ec2.delete_snapshot(SnapshotId=snapshot_id)

def read_ami_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == "__main__":
    ami_file = 'amis.txt'
    
    aws_profile = 'default'  

    session = boto3.Session(profile_name=aws_profile)
    
    ami_ids = read_ami_ids_from_file(ami_file)
    
    for ami_id in ami_ids:
        deregister_ami_and_delete_snapshots(ami_id, session)

