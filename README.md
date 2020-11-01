Idea is to create a pipeline via commands for different usecases using services. Having decoupled services increases it's usability more as then single services can also be called individually and can be plugges into pipeline also to fulfill the other usecases. 

There are 3 different kinds of services which are supported as of now:

1. Cloud Services
2. Storage Services
3. Target Services

To create pipeline using these services 'command_paths' can be used.


1. Cloud Service: All cloud related services can be used from these services.

      Currently it has support for 'aws cloud'. Details of supported services can be found in settings.py

      Usage Example: Get all ec2 instances details:

      1. Configuration:

          a. Configuration via file: Location can be configured in configuration.py of each cloud service

              aws_obj = AWSClient(load_via='file')

          b. Configuration via object: Creds can be specified in configuration.py

              aws_obj = AWSClient(load_via='config_obj')

          Creds will be loaded on boto3 from code itself.


      2. Provide resource to be used for service: It can be done in 2 ways:
          1. With constructor:

              aws_obj = AWSClient(load_via='file', resource='ec2')

          2. Setting the resource property

              aws_obj = AWSClient(load_via='file')
              aws_obj.resource = 'ec2'

              with this approach internal boto3 client will send a new client with this resource. No need to call boto3 client again.


      3. Get details of all ec2 instances:

              aws_obj = AWSClient(load_via='file')
              result = awsobj.get_ec2_instances_details()


2. Storage Services: All sort of data storage can be placed and used from these services.
                     Currently it has support for 'sqlite_engine' falling into database kind of storage. Details of supported services can be found in settings.py
                     Usage Example: 

                                   

