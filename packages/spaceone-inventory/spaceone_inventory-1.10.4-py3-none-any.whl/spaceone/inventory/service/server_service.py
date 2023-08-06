import logging
from spaceone.core.service import *
from spaceone.core import utils
from spaceone.inventory.manager.region_manager import RegionManager
from spaceone.inventory.manager.identity_manager import IdentityManager
from spaceone.inventory.manager.resource_group_manager import ResourceGroupManager
from spaceone.inventory.manager.collection_data_manager import CollectionDataManager
from spaceone.inventory.manager.collection_state_manager import CollectionStateManager
from spaceone.inventory.manager.server_manager import ServerManager
from spaceone.inventory.model.server_model import Server
from spaceone.inventory.error import *

_LOGGER = logging.getLogger(__name__)
_KEYWORD_FILTER = ['server_id', 'name', 'ip_addresses', 'cloud_service_group', 'cloud_service_type',
                   'reference.resource_id']


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class ServerService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)
        self.server_mgr: ServerManager = self.locator.get_manager('ServerManager')
        self.region_mgr: RegionManager = self.locator.get_manager('RegionManager')
        self.identity_mgr: IdentityManager = self.locator.get_manager('IdentityManager')

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'authorization.require_project_id': True
    })
    @check_required(['domain_id'])
    def create(self, params):
        """
        Args:
            params (dict): {
                    'name': 'str',
                    'primary_ip_address': 'str',
                    'os_type': 'LINUX | WINDOWS',
                    'account': 'str',
                    'instance_type': 'str',
                    'provider': 'str',
                    'cloud_service_group': 'str',
                    'cloud_service_type': 'str',
                    'region_code': 'str',
                    'data': 'dict',
                    'metadata': 'dict',
                    'nics': 'list',
                    'disks': 'list',
                    'reference': 'dict',
                    'tags': 'list or dict',
                    'project_id': 'str',
                    'domain_id': 'str'
                }

        Returns:
            server_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        provider = params.get('provider', self.transaction.get_meta('secret.provider'))
        project_id = params.get('project_id')
        secret_project_id = self.transaction.get_meta('secret.project_id')

        domain_id = params['domain_id']
        nics = params.get('nics', [])
        primary_ip_address = params.get('primary_ip_address')
        cloud_service_group = params.get('cloud_service_group')
        cloud_service_type = params.get('cloud_service_type')
        region_code = params.get('region_code')

        if provider:
            params['provider'] = provider

        if region_code and provider:
            params['ref_region'] = f'{domain_id}.{provider}.{region_code}'

        if cloud_service_group and cloud_service_type and provider:
            params['ref_cloud_service_type'] = f'{params["domain_id"]}.' \
                                               f'{params["provider"]}.' \
                                               f'{params["cloud_service_group"]}.' \
                                               f'{params["cloud_service_type"]}'
        elif cloud_service_group and not cloud_service_type:
            del params['cloud_service_group']
        elif not cloud_service_group and cloud_service_type:
            del params['cloud_service_type']

        if project_id:
            self.identity_mgr.get_project(project_id, domain_id)
            params['project_id'] = project_id
        elif secret_project_id:
            params['project_id'] = secret_project_id

        params['ip_addresses'] = self._get_ip_addresses_from_nics(nics)
        params['primary_ip_address'] = self._get_primary_ip_address(
            primary_ip_address, params['ip_addresses'])

        params = data_mgr.create_new_history(params, exclude_keys=['domain_id', 'ref_region', 'ref_cloud_service_type'])
        server_vo = self.server_mgr.create_server(params)

        # Create Collection State
        state_mgr: CollectionStateManager = self.locator.get_manager('CollectionStateManager')
        state_mgr.create_collection_state(server_vo.server_id, 'inventory.Server', domain_id)

        return server_vo

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['server_id', 'domain_id'])
    def update(self, params):
        """
        Args:
            params (dict): {
                    'server_id': 'str',
                    'name': 'str',
                    'primary_ip_address': 'str',
                    'os_type': 'LINUX | WINDOWS',
                    'account': 'str',
                    'instance_type': 'str',
                    'provider': 'str',
                    'cloud_service_group': 'str',
                    'cloud_service_type': 'str',
                    'region_code': 'str',
                    'data': 'dict',
                    'metadata': 'dict',
                    'nics': 'list',
                    'disks': 'list',
                    'reference': 'dict',
                    'tags': 'list or dict',
                    'project_id': 'str',
                    'domain_id': 'str',
                    'release_project': 'bool',
                    'release_region': 'bool'
                }

        Returns:
            server_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        provider = params.get('provider', self.transaction.get_meta('secret.provider'))
        project_id = params.get('project_id')
        secret_project_id = self.transaction.get_meta('secret.project_id')

        server_id = params['server_id']
        domain_id = params['domain_id']
        release_region = params.get('release_region', False)
        release_project = params.get('release_project', False)
        primary_ip_address = params.get('primary_ip_address')
        region_code = params.get('region_code')

        server_vo: Server = self.server_mgr.get_server(server_id, domain_id)

        if provider:
            params['provider'] = provider

        if release_region:
            params.update({
                'region_code': None,
                'ref_region': None
            })
        else:
            if region_code:
                params['ref_region'] = f'{domain_id}.{provider or server_vo.provider}.{region_code}'

        if release_project:
            params['project_id'] = None
        elif project_id:
            self.identity_mgr.get_project(project_id, domain_id)
        elif secret_project_id:
            params['project_id'] = secret_project_id

        if 'nics' in params:
            params['ip_addresses'] = self._get_ip_addresses_from_nics(params['nics'])
            params['primary_ip_address'] = self._get_primary_ip_address(
                primary_ip_address, params['ip_addresses'], server_vo.primary_ip_address)

        else:
            if primary_ip_address:
                params['primary_ip_address'] = self._get_primary_ip_address(
                    primary_ip_address, server_vo.ip_addresses)

        server_data = server_vo.to_dict()
        exclude_keys = ['server_id', 'domain_id', 'release_project', 'release_region', 'ref_region']
        params = data_mgr.merge_data_by_history(params, server_data, exclude_keys=exclude_keys)

        server_vo = self.server_mgr.update_server_by_vo(params, server_vo)

        state_mgr: CollectionStateManager = self.locator.get_manager('CollectionStateManager')
        state_vo = state_mgr.get_collection_state(server_id, domain_id)

        if state_vo:
            state_mgr.reset_collection_state(state_vo)
        else:
            state_mgr.create_collection_state(server_id, 'inventory.Server', domain_id)

        return server_vo

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['server_id', 'domain_id'])
    def pin_data(self, params):
        """
        Args:
            params (dict): {
                    'server_id': 'str',
                    'keys': 'list',
                    'domain_id': 'str'
                }

        Returns:
            server_vo (object)

        """

        data_mgr: CollectionDataManager = self.locator.get_manager('CollectionDataManager')

        server_vo: Server = self.server_mgr.get_server(params['server_id'], params['domain_id'])

        params['collection_info'] = data_mgr.update_pinned_keys(params['keys'], server_vo.collection_info.to_dict())

        return self.server_mgr.update_server_by_vo(params, server_vo)

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['server_id', 'domain_id'])
    def delete(self, params: dict):
        """
        Args:
            params (dict): {
                    'server_id': 'str',
                    'domain_id': 'str'
                }

        Returns:
            None

        """

        server_id = params['server_id']
        domain_id = params['domain_id']

        self.server_mgr.delete_server(server_id, domain_id)

        # Cascade Delete Collection State
        state_mgr: CollectionStateManager = self.locator.get_manager('CollectionStateManager')
        state_mgr.delete_collection_state_by_resource_id(server_id, domain_id)

    @transaction(append_meta={'authorization.scope': 'PROJECT'})
    @check_required(['server_id', 'domain_id'])
    def get(self, params):
        """
        Args:
            params (dict): {
                    'server_id': 'str',
                    'domain_id': 'str',
                    'only': 'list'
                }

        Returns:
            server_vo (object)

        """

        return self.server_mgr.get_server(params['server_id'], params['domain_id'], params.get('only'))

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'mutation.append_parameter': {'user_projects': 'authorization.projects'}
    })
    @check_required(['domain_id'])
    @append_query_filter(['server_id', 'name', 'state', 'primary_ip_address', 'ip_addresses', 'os_type',
                          'account', 'instance_type', 'provider', 'cloud_service_group', 'cloud_service_type',
                          'region_code', 'resource_group_id', 'project_id', 'project_group_id',
                          'domain_id', 'user_projects'])
    @append_keyword_filter(_KEYWORD_FILTER)
    def list(self, params):
        """
        Args:
            params (dict): {
                    'server_id': 'str',
                    'name': 'str',
                    'state': 'str',
                    'primary_ip_address': 'str',
                    'ip_addresses': 'str',
                    'os_type': 'str',
                    'account': 'str',
                    'instance_type': 'str',
                    'provider': 'str',
                    'cloud_service_group': 'str',
                    'cloud_service_type': 'str',
                    'region_code': 'str',
                    'resource_group_id': 'str',
                    'project_id': 'str',
                    'project_group_id': 'str',
                    'domain_id': 'str',
                    'query': 'dict (spaceone.api.core.v1.Query)',
                    'user_projects': 'list', // from meta
                }

        Returns:
            results (list)
            total_count (int)

        """

        query = params.get('query', {})
        query = self._append_resource_group_filter(query, params['domain_id'])
        query = self._change_project_group_filter(query, params['domain_id'])

        server_vos, total_count = self.server_mgr.list_servers(query)

        return server_vos, total_count

    @transaction(append_meta={
        'authorization.scope': 'PROJECT',
        'mutation.append_parameter': {'user_projects': 'authorization.projects'}
    })
    @check_required(['query', 'domain_id'])
    @append_query_filter(['resource_group_id', 'domain_id', 'user_projects'])
    @append_keyword_filter(_KEYWORD_FILTER)
    def stat(self, params):
        """
        Args:
            params (dict): {
                'resource_group_id': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)',
                'user_projects': 'list', // from meta
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        query = params.get('query', {})
        query = self._append_resource_group_filter(query, params['domain_id'])
        query = self._change_project_group_filter(query, params['domain_id'])

        return self.server_mgr.stat_servers(query)

    def _append_resource_group_filter(self, query, domain_id):
        change_filter = []

        for condition in query.get('filter', []):
            key = condition.get('k', condition.get('key'))
            value = condition.get('v', condition.get('value'))
            operator = condition.get('o', condition.get('operator'))

            if key == 'resource_group_id':
                server_ids = None

                if operator in ['not', 'not_contain', 'not_in', 'not_contain_in']:
                    resource_group_operator = 'not_in'
                else:
                    resource_group_operator = 'in'

                if operator in ['eq', 'not', 'contain', 'not_contain']:
                    server_ids = self._get_server_ids_from_resource_group_id(value, domain_id)
                elif operator in ['in', 'not_in', 'contain_in', 'not_contain_in'] and isinstance(value, list):
                    server_ids = []
                    for v in value:
                        server_ids += self._get_server_ids_from_resource_group_id(v, domain_id)

                if server_ids is not None:
                    change_filter.append({
                        'k': 'server_id',
                        'v': list(set(server_ids)),
                        'o': resource_group_operator
                    })

            else:
                change_filter.append(condition)

        query['filter'] = change_filter
        return query

    def _get_server_ids_from_resource_group_id(self, resource_group_id, domain_id):
        resource_type = 'inventory.Server'
        rg_mgr: ResourceGroupManager = self.locator.get_manager('ResourceGroupManager')

        resource_group_filters = rg_mgr.get_resource_group_filter(resource_group_id, resource_type, domain_id,
                                                                  _KEYWORD_FILTER)
        server_ids = []
        for resource_group_query in resource_group_filters:
            resource_group_query['distinct'] = 'server_id'
            result = self.server_mgr.stat_servers(resource_group_query)
            server_ids += result.get('results', [])
        return server_ids

    @staticmethod
    def _get_ip_addresses_from_nics(nics: list) -> list:
        all_ip_addresses = []
        try:
            for nic in nics:
                ip_addresses = nic.get('ip_addresses', [])
                all_ip_addresses += ip_addresses

                public_ip_address = nic.get('public_ip_address')
                if public_ip_address:
                    all_ip_addresses.append(public_ip_address)

            return list(set(all_ip_addresses))

        except Exception:
            raise ERROR_INVALID_PARAMETER(key='nics', reason='nics format is invalid.')

    @staticmethod
    def _get_primary_ip_address(primary_ip_address, all_ip_addresses, old_primary_ip_address=None):
        if primary_ip_address:
            if len(all_ip_addresses) > 0:
                if primary_ip_address not in all_ip_addresses:
                    raise ERROR_INVALID_PRIMARY_IP_ADDRESS()

            return primary_ip_address

        else:
            if len(all_ip_addresses) > 0:
                if old_primary_ip_address and old_primary_ip_address in all_ip_addresses:
                    return old_primary_ip_address
                else:
                    return all_ip_addresses[0]

        return None

    def _change_project_group_filter(self, query, domain_id):
        change_filter = []

        project_group_query = {
            'filter': [],
            'only': ['project_group_id']
        }

        for condition in query.get('filter', []):
            key = condition.get('key', condition.get('k'))
            value = condition.get('value', condition.get('v'))
            operator = condition.get('operator', condition.get('o'))

            if not all([key, operator]):
                raise ERROR_DB_QUERY(reason='filter condition should have key, value and operator.')

            if key == 'project_group_id':
                project_group_query['filter'].append(condition)
            else:
                change_filter.append(condition)

        if len(project_group_query['filter']) > 0:
            identity_mgr: IdentityManager = self.locator.get_manager('IdentityManager')
            response = identity_mgr.list_project_groups(project_group_query, domain_id)
            project_group_ids = []
            project_ids = []
            for project_group_info in response.get('results', []):
                project_group_ids.append(project_group_info['project_group_id'])

            for project_group_id in project_group_ids:
                response = identity_mgr.list_projects_in_project_group(project_group_id, domain_id, True,
                                                                       {'only': ['project_id']})
                for project_info in response.get('results', []):
                    if project_info['project_id'] not in project_ids:
                        project_ids.append(project_info['project_id'])

            change_filter.append({'k': 'project_id', 'v': project_ids, 'o': 'in'})

        query['filter'] = change_filter
        return query
