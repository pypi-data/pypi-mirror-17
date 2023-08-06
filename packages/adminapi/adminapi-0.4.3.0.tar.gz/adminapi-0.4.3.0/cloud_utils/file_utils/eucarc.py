
import operator
import os
import re
from collections import OrderedDict
from urlparse import urljoin, urlparse
from prettytable import PrettyTable
from cloud_utils.log_utils.eulogger import Eulogger
from cloud_utils.net_utils.sshconnection import CommandExitCodeException


class Eucarc(object):
    _KEY_DIR_STR = '\${EUCA_KEY_DIR}'

    def __init__(self, filepath=None, string=None, sshconnection=None, keysdir=None, logger=None,
                 loglevel='INFO'):
        """
        Will populate a Eucalyptus Runtime Configuration (eucarc) obj with values from a local
         file, remote file, or string buffer.
        The parser expect values in the following format:
        export key=value
        For example:
        export S3_URL=http://169.254.123.123:8773/services/objectstorage

        The value 'http://169.254.123.123:8773/services/objectstorage' will be assigned to an
        of the eucarc obj using the lower case version of the key, ie: eucarc.s3
        :param filepath: the local or remote filepath to the eucarc
        :param string: a string buffer containing the eucarc contents to be parsed
        :param sshconnection: an SshConnection() obj to a remote machine to read the eucarc
                              at 'filepath' from.
        :param keysdir: A value to replace _KEY_DIR_STR (${EUCA_KEY_DIR}) with, by defualt this is
                       the filepath, but when parsing from a string buffer filepath is unknown.
                       Remote files will be prefixed with an sftp://<user>@<hostname>/ before
                       the keys dir for later download.
        :param logger: logging.logger or equiv for logging output. By default a logger will
                        be created with the class name as the identifier
        """
        # init most common eucarc values to None...
        self._account_name = None
        self._account_id = None
        self._user_id = None
        self._user_name = None
        self._access_key = None
        self._secret_key = None

        self._ec2_url = None
        self._iam_url = None
        self._sts_url = None
        self._sqs_url = None
        self._token_url = None
        self._cloudwatch_url = None
        self._elb_url = None
        self._cloudformation_url = None
        self._autoscaling_url = None
        self._simpleworkflow_url = None

        self.aws_credential_file = None

        self.aws_simpleworkflow_url = None
        self.ec2_access_key = None
        self.ec2_cert = None
        self.ec2_jvm_args = None
        self.ec2_private_key = None
        self.ec2_secret_key = None
        self.eucalyptus_cert = None
        self.eustore_url = 'http://emis.eucalyptus.com/'
        self._bootstrap_url = None
        self._properties_url = None

        self.s3_url = None

        # End of init default eucarc attrs
        if not logger:
            logger = Eulogger(identifier=self.__class__.__name__, stdout_level=loglevel)
        logger.set_stdout_loglevel(loglevel)
        self._log = logger
        self._debug = self.log.debug
        self._credpath = filepath
        if keysdir is None:
            keysdir = filepath
        self._keysdir = keysdir
        self._string = string
        self._sshconnection = sshconnection
        self._unparsed_lines = None
        if string:
            self._from_string()
        elif filepath:
            self._from_filepath(filepath=filepath, sshconnection=sshconnection, keysdir=filepath)

    # Properties to accommodate all the prefixes which reference the same values...
    ##############################################################################################
    # Base values...
    ##############################################################################################
    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def account_name(self):
        return self._account_name

    @account_name.setter
    def account_name(self, value):
        self._account_name = value

    @property
    def user_id(self):
        return self._user_id or self._account_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        self._user_name = value

    @property
    def access_key(self):
        return self._access_key

    @access_key.setter
    def access_key(self, value):
        self._access_key = value

    @property
    def access_key_id(self):
        return self._access_key

    @access_key_id.setter
    def access_key_id(self, value):
        self._access_key = value

    @property
    def secret_key(self):
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    @property
    def secret_key_id(self):
        return self._secret_key

    @secret_key_id.setter
    def secret_key_id(self, value):
        self._secret_key = value


    ##############################################################################################
    # Service URLs
    ##############################################################################################
    # EC2
    @property
    def ec2_url(self):
        return self._ec2_url

    @ec2_url.setter
    def ec2_url(self, url):
        self._ec2_url = url

    # AutoScaling
    @property
    def auto_scaling_url(self):
        return self._autoscaling_url

    @auto_scaling_url.setter
    def auto_scaling_url(self, url):
        self._autoscaling_url = url

    @property
    def aws_auto_scaling_url(self):
        return self._autoscaling_url

    @aws_auto_scaling_url.setter
    def aws_auto_scaling_url(self, url):
        self._autoscaling_url = url

    # IAM
    @property
    def iam_url(self):
        return self._iam_url

    @iam_url.setter
    def iam_url(self, url):
        self._iam_url = url

    @property
    def aws_iam_url(self):
        return self._iam_url

    @aws_iam_url.setter
    def aws_iam_url(self, url):
        self._iam_url = url

    @property
    def euare_url(self):
        return self._iam_url

    @euare_url.setter
    def euare_url(self, url):
        self._iam_url = url

    # STS
    @property
    def sts_url(self):
        return self._sts_url

    @sts_url.setter
    def sts_url(self, url):
        self._sts_url = url

    @property
    def token_url(self):
        return self._sts_url

    @token_url.setter
    def token_url(self, url):
        self._sts_url = url


    # SQS
    @property
    def sqs_url(self):
        return self._sqs_url

    @sqs_url.setter
    def sqs_url(self, url):
        self._sqs_url = url


    # Cloud Formation
    @property
    def aws_cloudformation_url(self):
        return self._cloudformation_url

    @aws_cloudformation_url.setter
    def aws_cloudformation_url(self, url):
        self._cloudformation_url = url

    @property
    def cloudformation_url(self):
        return self._cloudformation_url

    @cloudformation_url.setter
    def cloudformation_url(self, url):
        self._cloudformation_url = url

    #Cloud Watch
    @property
    def aws_cloudwatch_url(self):
        return self._cloudwatch_url

    @aws_cloudwatch_url.setter
    def aws_cloudwatch_url(self, url):
        self._cloudwatch_url = url

    @property
    def cloudwatch_url(self):
        return self._cloudwatch_url

    @cloudwatch_url.setter
    def cloudwatch_url(self, url):
        self._cloudwatch_url = url

    # ELB
    @property
    def aws_elb_url(self):
        return self._elb_url

    @aws_elb_url.setter
    def aws_elb_url(self, url):
        self._elb_url = url

    @property
    def elb_url(self):
        return self._elb_url

    @elb_url.setter
    def elb_url(self, url):
        self._elb_url = url

    # Simple Work Flow
    @property
    def aws_simpleworkflow_url(self):
        return self._simpleworkflow_url

    @aws_simpleworkflow_url.setter
    def aws_simpleworkflow_url(self, url):
        self._simpleworkflow_url = url

    @property
    def simpleworkflow_url(self):
        return self._simpleworkflow_url

    @simpleworkflow_url.setter
    def simpleworkflow_url(self, url):
        self._simpleworkflow_url = url


    ##############################################################################################
    # With the EC2 prefix...
    ##############################################################################################
    @property
    def ec2_account_id(self):
        return self._account_id

    @ec2_account_id.setter
    def ec2_account_id(self, value):
        self._account_id = value

    @property
    def ec2_user_id(self):
        return self._user_id or self._account_id

    @ec2_user_id.setter
    def ec2_user_id(self, value):
        self._user_id = value

    @property
    def ec2_account_number(self):
        return self._account_id

    @ec2_account_number.setter
    def ec2_account_number(self, value):
        self._account_id = value

    @property
    def ec2_account_name(self):
        return self._account_name

    @ec2_account_name.setter
    def ec2_account_name(self, value):
        self._account_name = value

    @property
    def ec2_access_key(self):
        return self._access_key

    @ec2_access_key.setter
    def ec2_access_key(self, value):
        self._access_key = value

    @property
    def ec2_access_key_id(self):
        return self._access_key

    @ec2_access_key_id.setter
    def ec2_access_key_id(self, value):
        self._access_key = value

    @property
    def ec2_secret_key(self):
        return self._secret_key

    @ec2_secret_key.setter
    def ec2_secret_key(self, value):
        self._secret_key = value

    @property
    def ec2_secret_key_id(self):
        return self._secret_key

    @ec2_secret_key_id.setter
    def ec2_secret_key_id(self, value):
        self._secret_key = value



    ##############################################################################################
    # With the AWS prefix...
    ##############################################################################################
    @property
    def aws_account_id(self):
        return self._account_id

    @aws_account_id.setter
    def aws_account_id(self, value):
        self._account_id = value

    @property
    def aws_account_name(self):
        return self._account_name

    @aws_account_name.setter
    def aws_account_name(self, value):
        self._account_name = value

    @property
    def aws_user_name(self):
        return self._user_name

    @aws_user_name.setter
    def aws_user_name(self, value):
        self._user_name = value

    @property
    def aws_access_key(self):
        return self._access_key

    @aws_access_key.setter
    def aws_access_key(self, value):
        self._access_key = value

    @property
    def aws_access_key_id(self):
        return self._access_key

    @aws_access_key_id.setter
    def aws_access_key_id(self, value):
        self._access_key = value

    @property
    def aws_secret_key(self):
        return self._secret_key

    @aws_secret_key.setter
    def aws_secret_key(self, value):
        self._secret_key = value

    @property
    def aws_secret_key_id(self):
        return self._secret_key

    @aws_secret_key_id.setter
    def aws_secret_key_id(self, value):
        self._secret_key = value

    @property
    def aws_secret_access_key_id(self):
        return self._secret_key

    @aws_secret_access_key_id.setter
    def aws_secret_access_key_id(self, value):
        self._secret_key = value

    @property
    def aws_secret_access_key(self):
        return self._secret_key

    @aws_secret_access_key.setter
    def aws_secret_access_key(self, value):
        self._secret_key = value

    ##############################################################################################
    # Euca Specific
    ##############################################################################################
    @property
    def euca_bootstrap_url(self):
        return self._bootstrap_url

    @euca_bootstrap_url.setter
    def euca_bootstrap_url(self, value):
        self._bootstrap_url = value

    @property
    def bootstrap_url(self):
        return self._bootstrap_url

    @bootstrap_url.setter
    def bootstrap_url(self, value):
        self._bootstrap_url = value

    @property
    def euca_properties_url(self):
        return self._properties_url

    @euca_properties_url.setter
    def euca_properties_url(self, value):
        self._properties_url = value

    @property
    def properties_url(self):
        return self._properties_url

    @properties_url.setter
    def properties_url(self, value):
        self._properties_url = value

    # Hold these values as properties so the dict only returns cred info, not obj info...
    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, logger):
        self._log = logger

    @property
    def keys_dir(self):
        return self._keysdir

    @keys_dir.setter
    def keys_dir(self, value):
        self._keysdir = value
        if self._unparsed_lines:
            # see if there were any lines that were not previously parsed due to lack of keysdir
            try:
                self.log.debug('Attempting to resolve any unparsed lines with new keydir...')
                self._from_string(string=self._unparsed_lines, keysdir=self._keysdir)
            except:
                pass

    def _from_string(self, string=None, keysdir=None):
        """
        Parse the Eucarc attributes from this string buffer. Populates self with attributes.

        :param string: String buffer to parse from. By default self._string is used.
        :param keysdir: A vaule to replace _KEY_DIR_STR (${EUCA_KEY_DIR}) with, by defual this is
                       the filepath, but when parsing from a string buffer filepath is unknown
        :returns dict of attributes.
        """
        string = string or self._string
        if keysdir is None:
            keysdir = self._keysdir
        new_dict = {}
        message = ""
        if string:
            if not isinstance(string, list):
                if not isinstance(string, basestring):
                    raise TypeError('"_from_string" expected string(basestring) type, got:{0}:{1}'
                                    .format(string, type(string)))
                string = str(string)
                lines = string.splitlines()
            else:
                lines = string
            for line in lines:
                if line:
                    match = (re.search('^\s*export\s+(\w+)=\s*(\S+)$', line) or
                             re.search('^\s*(\S+)\s*=\s*(\S+)$', line))
                    if not match:
                        # This line does not match our expected format, add it to the messages
                        message += line + "\n"
                    else:
                        key = match.group(1)
                        value = match.group(2)
                        value = str(value).strip('"').strip("'")
                        if re.search(self._KEY_DIR_STR, line):
                            if keysdir:
                                value = re.sub(self._KEY_DIR_STR, keysdir, value)
                            else:
                                # Add this line to the messages since this value will not
                                # resolve without a defined 'keydir'...
                                message += line + "\n"
                                continue
                        if not (key and value):
                            raise ValueError('Fix me! Could not find key=value, in this line:"{0}"'
                                             .format(line))
                        key = key.lower().replace('-', '_')
                        self.__setattr__(key, value)
                        new_dict[key] = value
            if message:
                self._unparsed_lines = message
                new_dict['message'] = message
        return new_dict

    def _from_filepath(self, filepath=None, sshconnection=None, keysdir=None):
        """
        Read the eucarc from a provided filepath. If an sshconnection obj is provided than
        this will attempt to read from a file path via the sshconnection, otherwise the filepath
        is read from the local filesystem.
        Populated self with attributes read from eucarc.

        :param filepath: The file path to a eucarc
        :param sshconnection: An sshconnection obj, used to read from a remote machine
        :param keysdir: A vaule to replace _KEY_DIR_STR (${EUCA_KEY_DIR}) with, by defual this is
                       the filepath, but when parsing from a string buffer filepath is unknown
        :returns dict of attributes
        """
        filepath = filepath or self._credpath
        if keysdir is None:
            keysdir = self._keysdir or os.path.dirname(filepath)
        sshconnection = sshconnection or self._sshconnection
        if sshconnection:
            # Assume this is a remote file...
            sftppath = "sftp://{0}@{1}/".format(sshconnection.username, sshconnection.host)
            for remotepath in [filepath, os.path.join(filepath, 'eucarc')]:
                try:
                    sshconnection.sys('[ -f {0} ]'.format(remotepath), code=0)
                    break
                except CommandExitCodeException:
                    remotepath = None
            if not remotepath:
                raise ValueError('Remote File not found on host:"{0}" at path(s):"{1}", or "{2}"'
                                     .format(sshconnection.host, filepath,
                                             os.path.join(filepath, 'eucarc')))
            keysdir = urljoin(sftppath, keysdir)
            self._keysdir = keysdir
            string = sshconnection.sys('cat {0}'.format(remotepath), listformat=False, code=0)
        else:
            # This is a local file...
            if not re.search('\S+', filepath):
                filepath = os.path.curdir
            filepath = os.path.realpath(filepath)
            if not os.path.isfile(filepath):
                orig_file_path = filepath
                filepath = os.path.join(filepath, 'eucarc')
                if not os.path.isfile(filepath):
                    raise ValueError('File not found at path(s):"{0}", or "{1}"'
                                     .format(orig_file_path, filepath))
            f = open(filepath)
            with f:
                string = f.read()
        return self._from_string(string, keysdir=keysdir)

    def show(self, search=None, print_method=None, print_table=True):
        """
        Show the eucarc key, values in a table format
        :param print_table: bool, if true will print the table to self._debug, else returns the
                            table obj
        """
        match_op = operator.truth
        if search and str(search).startswith('!'):
            search = str(search).lstrip('!')
            match_op = operator.not_
        print_method = print_method or self.log.info
        pt = PrettyTable(['KEY', 'VALUE'])
        pt.hrules = 1
        pt.align = 'l'
        pt.header = False
        pt.max_width['VALUE'] = 85
        pt.max_width['KEY'] = 35
        attrs = OrderedDict(sorted(self.get_eucarc_attrs().items()))
        for key, value in attrs.iteritems():
            if value is None or isinstance(value, basestring):
                if not search or match_op(re.search(str(search), key) or \
                        (value and re.search(str(search), value))):
                    pt.add_row([key, value])
        if not search or (match_op(re.search(search, self._unparsed_lines))):
            pt.add_row(['UNPARSED LINES', self._unparsed_lines])
        if print_table:
            print_method("\n" + str(pt) + "\n")
        else:
            return pt

    def get_eucarc_attrs(self, excludes=['^_']):
        ret_dict = {}
        for key, value in self.__dict__.iteritems():
            if isinstance(value, basestring) or isinstance(value, type(None)):
                skip = False
                for exclude in excludes:
                    if re.search(exclude, str(key)):
                        skip = True
                        break
                if not skip:
                    ret_dict[key] = value
        for key in vars(Eucarc):
            if type(getattr(Eucarc, key)) == property:
                try:
                    ret_dict[key] = getattr(self, key)
                except Exception as PE:
                    self.log.error('Failed to get property attr:"{0}", err:"{1}"'.format(key, PE))
        return ret_dict

    def get_urls(self):
        ret = {}
        for key, value in self.__dict__.iteritems():
            if re.match('.*url$', key):
                ret[key] = value
        return ret
