"""Independent invariants and reference values for synthetic fleet exercises."""
import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))
import fleet_lab as lab

BASE = Path(__file__).parent

def fixture(name):
    return json.loads((BASE / 'fixtures' / (name + '.json')).read_text())

class ReliabilityTests(unittest.TestCase):
    def test_exposure_reverses_raw_count_comparison(self):
        result = lab.reliability(fixture('reliability'))
        a, b, c = result['cohorts']
        self.assertAlmostEqual(a['rate_per_1000h'], 2 / 3)
        self.assertEqual(b['rate_per_1000h'], 5)
        self.assertGreater(a['events'], b['events'])
        self.assertLess(a['rate_per_1000h'], b['rate_per_1000h'])
        self.assertAlmostEqual(c['one_sided_zero_event_upper_per_1000h'], -math.log(.05) / 2)
        self.assertAlmostEqual(c['two_sided_rate_interval_per_1000h'][1], -math.log(.025) / 2)

    def test_poisson_reference_quantiles(self):
        # Garwood limits for two events: 0.5 * chi-square quantiles, df 4 and 6.
        self.assertAlmostEqual(lab.invert_poisson_cdf(1, .975), .2422092785, places=8)
        self.assertAlmostEqual(lab.invert_poisson_cdf(2, .025), 7.2246876677, places=8)

    def test_base_rate(self):
        result = lab.reliability(fixture('reliability'))['alarm']
        self.assertAlmostEqual(result['positive_predictive_value'], 90 / 585)

    def test_missingness_is_not_silently_healthy(self):
        result = lab.reliability(fixture('reliability-censored'))
        self.assertEqual(len(result['cohorts'][0]['warnings']), 1)
        self.assertEqual(result['cohorts'][0]['exposure_hours'], 2100)

    def test_zero_exposure_rejected(self):
        data = fixture('reliability')
        for row in data['cohorts'][0]['observations']:
            row['exposure_hours'] = 0
        with self.assertRaises(ValueError):
            lab.reliability(data)

    def test_negative_events_rejected(self):
        data = fixture('reliability')
        data['cohorts'][0]['observations'][0]['events'] = -1
        with self.assertRaises(ValueError):
            lab.reliability(data)

class SignalTests(unittest.TestCase):
    def test_fresh_and_corrected_clock_pass(self):
        for name in ('signal-healthy', 'signal-clock-corrected'):
            self.assertEqual(lab.signal(fixture(name))['status'], 'PASS')

    def test_fresh_ingest_does_not_hide_stale_source(self):
        result = lab.signal(fixture('signal-fault'))
        self.assertEqual(result['status'], 'FAIL')
        self.assertIn('stale source event: node-a', result['issues'])
        self.assertIn('old boot: node-a', result['issues'])
        self.assertIn('missing telemetry: node-b', result['issues'])

    def test_units_fail(self):
        self.assertIn('unit mismatch: node-b', lab.signal(fixture('signal-unit-fault'))['issues'])

    def test_duplicate_and_serial_conflict(self):
        data = fixture('signal-healthy')
        data['inventory'].append(copy.deepcopy(data['inventory'][0]))
        data['readings'].append(copy.deepcopy(data['readings'][0]))
        data['readings'][1]['serial'] = 'WRONG'
        result = lab.signal(data)
        self.assertTrue(any('duplicate inventory' in item for item in result['issues']))
        self.assertIn('duplicate or reordered sequence: node-a', result['issues'])
        self.assertIn('serial mismatch: node-b', result['issues'])

    def test_uncertainty_prevents_boundary_pass(self):
        data = fixture('signal-healthy')
        data['readings'][0]['clock_uncertainty_s'] = 25
        self.assertEqual(lab.signal(data)['status'], 'FAIL')

class LifecycleTests(unittest.TestCase):
    def test_healthy_reaches_expected_generation(self):
        self.assertEqual(lab.lifecycle(fixture('lifecycle-healthy'))['final'], {'state':'available','generation':6})

    def test_duplicate_stale_and_reused_id_do_not_mutate(self):
        result = lab.lifecycle(fixture('lifecycle-contention'))
        self.assertEqual(result['status'], 'PASS')
        codes = [row['result'] for row in result['history']]
        self.assertIn('DUPLICATE', codes)
        self.assertIn('STALE_GENERATION', codes)
        self.assertIn('ID_REUSE_CONFLICT', codes)
        self.assertEqual(result['final']['generation'], 6)

    def test_failed_check_blocks_then_recovery_qualifies(self):
        fault = lab.lifecycle(fixture('lifecycle-fault'))
        self.assertEqual(fault['status'], 'BLOCKED')
        self.assertEqual(fault['final'], {'state':'qualifying','generation':4})
        self.assertIn('QUALIFICATION_FAILED', [r['result'] for r in fault['history']])
        recovered = lab.lifecycle(fixture('lifecycle-recovered'))
        self.assertEqual(recovered['status'], 'PASS')
        self.assertEqual(recovered['final']['generation'], 9)

    def test_live_workload_blocks_repair(self):
        data = fixture('lifecycle-healthy')
        data['events'][1]['workloads'] = 1
        result = lab.lifecycle(data)
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertEqual(result['final']['state'], 'draining')

    def test_old_check_generation_rejected(self):
        data = fixture('lifecycle-healthy')
        data['events'][4]['check_generation'] = 3
        self.assertEqual(lab.lifecycle(data)['status'], 'BLOCKED')

class CapacityTests(unittest.TestCase):
    def test_correlated_rack_loss_and_granularity(self):
        result = lab.capacity(fixture('capacity-fault'))
        self.assertEqual(result['total_gpus'], 128)
        self.assertEqual(result['scenarios'][0]['admissible_gpus'], 96)
        self.assertEqual(result['scenarios'][1]['admissible_gpus'], 72)
        self.assertEqual(result['worst_margin_gpus'], -8)
        self.assertEqual(result['status'], 'FAIL')

    def test_recovered_with_same_headroom(self):
        self.assertEqual(lab.capacity(fixture('capacity-recovered'))['status'], 'PASS')

    def test_more_headroom_cannot_increase_admission(self):
        data = fixture('capacity-recovered')
        original = lab.capacity(data)['scenarios'][0]['admissible_gpus']
        data['headroom_fraction'] = .3
        self.assertLessEqual(lab.capacity(data)['scenarios'][0]['admissible_gpus'], original)

    def test_invalid_domains_rejected(self):
        data = fixture('capacity-fault')
        data['domains'][1]['name'] = data['domains'][0]['name']
        with self.assertRaises(ValueError):
            lab.capacity(data)

class CLITests(unittest.TestCase):
    def test_non_object_input_rejected_without_attribute_error(self):
        with self.assertRaises(ValueError):
            lab.require_synthetic([])

    def test_fault_exit_and_recovery_exit(self):
        for name, expected in [('signal-fault',1),('signal-healthy',0)]:
            result = subprocess.run([sys.executable,str(BASE/'fleet_lab.py'),'signal',str(BASE/'fixtures'/f'{name}.json')],capture_output=True,text=True)
            self.assertEqual(result.returncode, expected)
            self.assertIn('status',json.loads(result.stdout))

if __name__ == '__main__':
    unittest.main()
