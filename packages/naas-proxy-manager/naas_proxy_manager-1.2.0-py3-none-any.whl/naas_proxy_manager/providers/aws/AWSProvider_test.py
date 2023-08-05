import pytest

@pytest.mark.e2e
def test_AWSProvider(aws_access_key_id, aws_secret_access_key):
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType

    pxm = ProxyManager()
    pxm.configure_provider('aws-us-east-1', AWSProvider(aws_access_key_id, aws_secret_access_key, aws_region_name='us-east-1'))

def test_AWSProvider_no_infrastructure():
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType

    pxm = ProxyManager()
    pxm.configure_provider('aws-us-east-1', AWSProvider('hello', 'world', aws_region_name='us-east-1', ensure_infrastructure=False, verify_credentials=False))
