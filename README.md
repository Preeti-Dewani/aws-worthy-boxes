Idea is to create a pipeline via commands for different usecases using services. Having decoupled services increases it's usability more as then single services can also be called individually and can be plugges into pipeline also to fulfill the other usecases. 

There are 3 different kinds of services which are supported as of now:

1. Cloud Services
2. Storage Services
3. Target Services

To create pipeline using these services `command_paths` can be used.


## Cloud Services: All cloud related services can be used from these services.

   Currently it has support for `aws cloud`. Details of supported services can be found in `settings.py`

   ### Usage: Get all ec2 instances details:

   1. Configuration:

      a. Configuration via file: Location can be configured in configuration.py of each cloud service

          from cloud_services.aws_cloud.client import AWSClient
          aws_obj = AWSClient(load_via='file')

      b. Configuration via object: Creds can be specified in configuration.py

          aws_obj = AWSClient(load_via='config_obj')

      Creds will be loaded on boto3 from code itself.


   2. Provide resource to be used for service: It can be done in 2 ways:
   
      a. With constructor:

          aws_obj = AWSClient(load_via='file', resource='ec2')

      b. Setting the resource property

          aws_obj = AWSClient(load_via='file')
          aws_obj.resource = 'ec2'

       with this approach internal boto3 client will send a new client with this resource. No need to call boto3 client again.


   3. Get details of all ec2 instances:

          aws_obj = AWSClient(load_via='file')
          result = aws_obj.get_ec2_instances_details()
              
   ### Hightlights:
      
   - Configuration loading can also be done dynamically.

   - Resource client can be changed dynamically.

   - Service exceptions are handled throught botocore



## Storage Services: All sort of data storage can be placed and used from these services.

   Currently it has support for `sqlite_engine` falling into database kind of storage. Details of supported services can be found in `settings.py`
   
   ### Usage Example: 
   
   i. Run any prerequisite SQL file: Configure prerequisite.sql file in configuration.py
   
       from storage_services.databases.sqlite_engine.client import SqliteClient
       sqlite_obj = SqliteClient(database='instances.db')
       sqlite_obj.run_prerequisites()
       
   ii. Run a query using the interface
   
       sqlite_obj = SqliteClient(database='instances.db')
       result = sqlite_obj.query_result("select * from servers where state='running';", records_count=10)
       
   ### Hightlights:
   
   - Atomicity can also be added to query by passing atomic=True/False as a parameter to call. 

   - Connection open and close will be handled internally by context manager itself.
      
      
## Target Services: All sort of write services can be placed and used from these services.

   Currently it has support for `ssh_config_service`. Details of supported services can be found in `settings.py`
   
   ### Usage Example:
   
   i. Write data in ssh file: Location can be passed on as param in client constructor or can be configured.
   
    from target_services.ssh_config_service.target import SSHConfigClient
    config_obj = SSHConfigClient(file_path='/home/preeti/.ssh/aws_demo.config')
    config_obj.write_config_entry(data)
         
         
 
 ## Creating Pipeline Via Commands:
 
    Pipeline: AWS(cloud) -> get ec2 instances -> SQLITE(storage) -> create db and insert data -> SSH CONFIG(target) -> write in config file
 
 ### Steps:
 
 1. Create action definition in `action_definitions.py` file as per pipeline.
 
 2. If commands and facade are supported for those action then it can be used directly else new command and facade class needs to be created.
 
 3. Usage via commands:
 
         from command_paths.execute import Controller
         ctrl = Controller(action_name='AWS_SQLITE_SSH_CONFIG')
         result = ctrl.executor()
      
       
   
 Things pending to cover:
 1. Type handling
 2. Better error handing
 3. Ansible dynamic inventory

