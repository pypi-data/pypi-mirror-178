import pytest
import pydash

@pytest.mark.e2e
def test_AWSProvider(aws_access_key_id, aws_secret_access_key):
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType

    pxm = ProxyManager()
    pxm.configure_provider('aws-us-east-1', AWSProvider(aws_access_key_id, aws_secret_access_key, aws_region_name='us-east-1'))

def test_AWSProvider_no_infrastructure():
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType

    pxm = ProxyManager()
    pxm.configure_provider('aws-us-east-1', AWSProvider('hello', 'world', aws_region_name='us-east-1', ensure_infrastructure=False, verify_credentials=False))


def test_AWSProvider_no_infrastructure_del_proxies(logger):
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType
    from naas_proxy_manager.classes.IProxy import IProxy

    provider = AWSProvider('hello', 'world', aws_region_name='us-east-1', ensure_infrastructure=False, verify_credentials=False)

    class FakeProxy(IProxy):

        def delete(self):
            pass

        def refresh(self):
            pass

        def wait_until_deleted(self):
            pass

        def wait_until_ready(self):
            pass

        def wait_until_running(self):
            pass


    provider.proxies = [
        FakeProxy(),
        FakeProxy(),
        FakeProxy()
    ]

    target_proxy = provider.proxies[1]
    target_proxy_id = target_proxy.id
    provider.delete_proxy(target_proxy.id, wait=True)

    assert len(provider.proxies) == 2
    assert target_proxy.id == target_proxy_id
    assert pydash.collections.find(
        provider.proxies,
        lambda x: x.id == target_proxy_id) is None


    provider.delete_proxy(provider.proxies[0].id, wait=False)
    assert len(provider.proxies) == 1

    provider.delete_proxies()
    assert len(provider.get_proxies()) == 0
