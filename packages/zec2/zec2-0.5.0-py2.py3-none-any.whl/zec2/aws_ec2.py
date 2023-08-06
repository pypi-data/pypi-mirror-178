import boto3
from click import UsageError
from botocore import exceptions


class AwsClient(object):

    conn = None

    def __init__(self, session=None):
        self._session = session
        self._aws_profile = 'default'
        self._aws_region = 'us-east-1'
        self._proxy = None

    def aws_profile(self, _aws_profile, _aws_region):
        self._aws_profile = _aws_profile
        self._aws_region = _aws_region

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        self._proxy = proxy

    def connection(self):
        try:
            if not self._session:
                self._session = boto3.Session(
                    profile_name=self._aws_profile,
                    region_name=self._aws_region)
            
            return self._session.resource('ec2')

        except exceptions.ProfileNotFound as e:
            raise UsageError(str(e))
        except exceptions.ConfigParseError as e:
            raise UsageError(str(e))
        except exceptions.ConfigNotFound as e:
            raise UsageError(str(e))
        except exceptions.UnknownCredentialError as e:
            raise UsageError(str(e))
        except exceptions.NoRegionError as e:
            raise UsageError(str(e))

    @property
    def client(self):
        if self.conn is None:
            self.conn = self.connection()
        return self.conn


class AwsEc2(AwsClient):

    def list(self, _filter=None):

        if _filter is None:
            _filter = []

        try:
            instances = self.client.instances.filter(Filters=[
                {
                    'Name': name,
                    'Values': value if type(value) == list else [value]
                }
                for name, value in _filter
            ])

            def by_name(instance):
                for tag in instance.tags or []:
                    if tag['Key'] == 'Name':
                        return tag['Value']
                else:
                    return ''

            instances = sorted(instances, key=by_name)
        except exceptions.ClientError as e:
            raise UsageError(str(e))

        return [AwsEc2Instance(instance) for instance in instances]


class AwsVpc(AwsClient):

    def list(self):
        return self.client.vpcs.all()


class AwsEc2Instance(object):

    states = {
        'running': 'green',
        'stopping': 'yellow',
        'stopped': 'red',
        'pending': 'yellow',
        'shutting-down': 'red'
    }

    def __init__(self, instance):
        self._instance = instance

    def name(self):
        for tag in self._instance.tags or []:
            if tag['Key'] == 'Name':
                return tag['Value']
        else:
            return ''

    def state(self):
        state = self._instance.state['Name']
        state_fg = self.states.get(state, 'red')
        return state, state_fg

    def zone(self):
        return str(self._instance.placement['AvailabilityZone'])

    def public_ip_address(self):
        if self._instance.public_ip_address:
            return self._instance.public_ip_address
        else:
            return ''

    def ssh_ip_address(self, private=False):
        if self._instance.public_ip_address and private is False:
            return self._instance.public_ip_address
        else:
            return self._instance.private_ip_address

    @property
    def aws(self):
        return self._instance

    def ssh_command(self, user, key_path, ec2):
        if not user:
            user = 'ec2-user'
        if not key_path:
            key_path = '~/.ssh/%s.pem' % self._instance.key_name

        proxy = ''
        private = False
        if ec2.proxy:
            private = True
            proxy = '-J %s ' % (ec2.proxy,)

        params = (proxy, key_path, user, self.ssh_ip_address(private))
        return 'ssh %s-i %s %s@%s' % params

    def stop(self):
        self._instance.stop()

    def start(self):
        self._instance.start()

    def restart(self):
        self._instance.reboot()

    def terminate(self):
        self._instance.terminate()

    def disable_api_termination(self):
        self._instance.modify_attribute(DisableApiTermination={'Value': False})
