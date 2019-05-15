import mock
import charms.reactive
import unit_tests.test_utils

from unittest.mock import patch, mock_open
import charms_openstack.test_utils as test_utils

# Mock out reactive decorators prior to importing reactive.kerberos_keytab
dec_mock = mock.MagicMock()
dec_mock.return_value = lambda x: x
charms.reactive.hook = dec_mock
charms.reactive.when = dec_mock
charms.reactive.when_not = dec_mock

import reactive.nfs_configurator as nfs_c

import jinja2


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        # test that the hooks actually registered the relation expressions that
        # are meaningful for this interface: this is to handle regressions.
        # The keys are the function names that the hook attaches to.
        hook_set = {
            'when': {
                'config_changed': ('config.changed', ), },
        }
        # test that the hooks were registered via the
        # reactive.kerberos_keytab
        self.registered_hooks_test_helper(nfs_c, hook_set, [])


class TestHandlers(unit_tests.test_utils.CharmTestCase):

    def setUp(self):
        super(TestHandlers, self).setUp()
        self.obj = nfs_c
        self.patches = [
            'status_set',
            'config'
        ]
        self.patch_all()

    @patch.object(nfs_c, 'Template')
    def test_config_changed(self, template):

        def config_side_effect(key):
            return {
                'nfs-common-options': 'FOO=bar,FAZ=baz'
            }[key]

        template_obj = template()
        self.config.side_effect = config_side_effect

        expected_context = {
            'nfs_options': ['FOO=bar', 'FAZ=baz']
            }
        with patch('builtins.open', mock_open()) as _mock_open:
            nfs_c.config_changed()
            template_obj.render.assert_called_with(expected_context)
