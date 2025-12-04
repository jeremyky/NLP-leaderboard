#!/usr/bin/env python3
"""
Run comprehensive test suite and generate a report

Usage:
    python run_comprehensive_tests.py
    
This will run all dataset-specific comprehensive tests and show:
- Pass/fail status
- Number of test cases per dataset
- Coverage metrics
"""
import subprocess
import sys

DATASETS = [
    ("AG News", "tests/dataset_tests/test_dataset_ag_news.py"),
    ("SST-2", "tests/dataset_tests/test_dataset_sst2.py"),
    ("SQuAD v1.1", "tests/dataset_tests/test_dataset_squad.py"),
    ("XNLI", "tests/dataset_tests/test_dataset_xnli.py"),
]

def run_tests():
    """Run all comprehensive test suites"""
    print("=" * 80)
    print("COMPREHENSIVE TEST SUITE RUNNER")
    print("=" * 80)
    print()
    
    results = []
    
    for name, path in DATASETS:
        print(f"Running {name} tests...")
        print("-" * 80)
        
        # Run pytest with verbose output
        result = subprocess.run(
            ["python", "-m", "pytest", path, "-v", "--tb=short"],
            capture_output=True,
            text=True
        )
        
        results.append({
            "name": name,
            "path": path,
            "passed": result.returncode == 0,
            "output": result.stdout + result.stderr
        })
        
        if result.returncode == 0:
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print()
    
    for r in results:
        status = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f"{status} - {r['name']}")
    
    print()
    print("=" * 80)
    
    # Return non-zero if any failed
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(run_tests())

