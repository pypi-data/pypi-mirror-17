from __future__ import unicode_literals
from __future__ import print_function

import unittest

from mock import Mock, patch
from tcell_agent.appsensor.meta import AppSensorMeta
from tcell_agent.policies.appsensor import FptSensor

class FptSensorTest(unittest.TestCase):

    def create_default_sensor_test(self):
        sensor = FptSensor()
        self.assertEqual(sensor.enabled, False)
        self.assertEqual(sensor.exclude_headers, False)
        self.assertEqual(sensor.exclude_forms, False)
        self.assertEqual(sensor.exclude_cookies, False)
        self.assertEqual(sensor.dp, "fpt")
        self.assertEqual(sensor.active_pattern_ids, {})
        self.assertEqual(sensor.exclusions, {})

    def with_disabled_sensor_check_test(self):
        sensor = FptSensor({"enabled": False})

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_fpt = sensor.check("get", {}, None, None, payloads_policy)
            self.assertFalse(is_fpt)
            self.assertFalse(patched_send_event.called)
            self.assertFalse(payloads_policy.apply.called)

    def with_enabled_sensor_and_no_vuln_params_check_test(self):
        sensor = FptSensor({"enabled": True})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_fpt = sensor.check("get", meta, None, None, payloads_policy)
            self.assertFalse(is_fpt)
            self.assertFalse(patched_send_event.called)
            self.assertFalse(payloads_policy.apply.called)

    def with_enabled_sensor_and_vuln_params_check_test(self):
        sensor = FptSensor({"enabled": True, "patterns": ["1"]})
        meta = AppSensorMeta(
            "remote_addr",
            "request_method",
            "abosolute_uri",
            "23947",
            session_id="session_id",
            user_id="user_id"
        )

        payloads_policy = Mock()
        payloads_policy.apply.return_value = None
        with patch('tcell_agent.policies.appsensor.injection_sensor.sendEvent') as patched_send_event:
            is_fpt = sensor.check("get", meta, "dirty", "../../../..", payloads_policy)
            self.assertTrue(is_fpt)
            patched_send_event.assert_called_once_with(meta, "fpt",  'dirty', {"l": "query"}, None, "1")
            payloads_policy.apply.assert_called_once_with("fpt", meta, "get", "dirty", "../../../..", {"l": "query"}, "1")
