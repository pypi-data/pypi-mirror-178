import pydash
import pytest

def test_ProxyManager_delete_all_proxies(logger):
    from naas_proxy_manager import ProxyManager, AWSProvider, ProxyType
    from naas_proxy_manager.classes.IProxy import IProxy

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

    pxm = ProxyManager()
    pxm.configure_provider('us-east-1', AWSProvider('hello', 'world', 'us-east-1', ensure_infrastructure=False, verify_credentials=False))
    pxm.configure_provider('us-east-2', AWSProvider('hello', 'world', 'us-east-2', ensure_infrastructure=False, verify_credentials=False))

    provider_one = pxm.get_provider('us-east-1')
    provider_one.proxies = [FakeProxy() for i in range(0,100)]

    provider_two = pxm.get_provider('us-east-2')
    provider_two.proxies = [FakeProxy() for i in range(0,500)]

    proxies = pxm.get_all_proxies()

    assert len(proxies) == 600

    pxm.delete_all_proxies(wait=True)
    proxies = pxm.get_all_proxies()

    assert len(proxies) == 0


