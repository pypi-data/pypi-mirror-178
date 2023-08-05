from naas_proxy_manager.classes import *

import pydash
import random
from typing import List 

class ProviderNotFound(Exception):
    pass

class ProxyManager:

    providers: dict[IProxyProvider]

    def __init__(self):
        self.providers = {}

    def get_provider(self, provider_name:str) -> IProxyProvider:
        if provider_name in self.providers:
            return self.providers[provider_name]
        else:
            raise ProviderNotFound()


    def configure_provider(self, name: str, provider: IProxyProvider) -> IProxyProvider:
        self.providers[name] = provider
        return provider

    def create_proxy(self, proxy_type:IProxyType, provider: IProxyProvider = None, params:dict = {}) -> dict:
        selected_provider = provider

        if selected_provider is None:
            # Select a compatible provider randomly.

            compatible_providers = pydash.filter_(self.providers, lambda x: x.implements_proxy_type(proxy_type))
            if len(compatible_providers) == 0:
                raise NotImplementedError(f'None of the configured providers implements "{proxy_type.name}" proxy type.')
            selected_provider = compatible_providers[random.randrange(0, len(compatible_providers))]
        else:
            # Make sure the selected provider implements the requested proxy.
            if selected_provider.implements_proxy_type(proxy_type) is False:
                raise NotImplementedError(f'Provider {selected_provider.__class__.__name__} does not implements "{proxy_type.name}" proxy type.')

        proxy = selected_provider.create_proxy(proxy_type, params=params)

        return proxy
    
    def get_all_proxies(self):
        all_proxies = []
        for provider_name in self.providers:
            provider = self.providers[provider_name] 
            all_proxies = all_proxies + provider.get_proxies()

        return all_proxies

    def delete_all_proxies(self, wait:bool=False):
        all_proxies = {}
        for provider_name in self.providers:
            provider : IProxyProvider = self.providers[provider_name]
            all_proxies[provider_name] = provider.get_proxies()
            provider.delete_proxies(wait=False)
        
        if wait is True:
            for provider_name in all_proxies:
                proxies : List[IProxy] = all_proxies[provider_name]

                for proxy in proxies:
                    proxy.wait_until_deleted()
