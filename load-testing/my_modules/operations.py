# █▀█ █▀█ █▀▀ █▀█ ▄▀█ ▀█▀ █ █▀█ █▄░█ █▀
# █▄█ █▀▀ ██▄ █▀▄ █▀█ ░█░ █ █▄█ █░▀█ ▄█

import subprocess, yaml, logging
import time

# Apply the YAML file to deploy the load generator
def apply_yaml_file(yaml_name):
    logging.info(f'Starting apply {yaml_name} YAML')
    subprocess.call(['kubectl', 'apply', '-f', './my_modules/'+str(yaml_name)])
    time.sleep(5)
    
#Scale Deploy with num_replicas
def scale_deploy(deploy,num_replicas):
    logging.info(f'Scale Deploy {deploy} with {num_replicas} replicas')
    subprocess.call(['kubectl', 'scale', 'deploy/'+str(deploy), '--replicas='+str(num_replicas)])
    time.sleep(20)
    
# Load YAML file into a dictionary
def load_yaml(filepath):
    with open(filepath) as f:
        data = yaml.safe_load(f)
    return data

# Edit the YAML dictionary to update the number of users
def edit_yaml(data, user_count):
    logging.info(f'Editing YAML with {user_count} users: {data}')
    containers = data['spec']['template']['spec']['containers']
    env_list = containers[0]
    env = env_list['env']
    user_env = env[1]
    user_env['value'] = str(user_count)
    env[1] = user_env
    env_list['env'] = env
    containers[0] = env_list
    data['spec']['template']['spec']['containers'] = containers
    logging.info(f'Edited YAML with {user_count} users: {data}')
    return data

# Save the updated YAML dictionary to a file
def save_yaml(data, filepath):
    with open(filepath, 'w') as f:
        yaml.safe_dump(data, f)
    logging.info(f'Saved YAML to {filepath}')

# Apply the updated YAML file to deploy the load generator
def apply_yaml():
    logging.info('Starting deployment with updated YAML')
    subprocess.call(['kubectl', 'apply', '-f', './my_modules/loadgenerator.yaml'])
    logging.info('Finished deployment with updated YAML')




