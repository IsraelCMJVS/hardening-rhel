#!/usr/bin/env python3
import json
import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    print(json.dumps({
        "error": "Usage: parse_oscap_results.py <xml_file>"
    }))
    sys.exit(1)

xml_file = sys.argv[1]

NS = {
    "cdf": "http://checklists.nist.gov/xccdf/1.2",
}

result_counters = {
    "pass": 0,
    "fail": 0,
    "error": 0,
    "unknown": 0,
    "notchecked": 0,
    "notselected": 0,
    "informational": 0,
    "fixed": 0,
    "manual": 0,
    "notapplicable": 0,
}

output = {
    "score": 0.0,
    "benchmark_id": "",
    "benchmark_title": "",
    "profile_id": "",
    "profile_title": "",
    "test_result_id": "",
    "start_time": "",
    "end_time": "",
    "rules": [],
    "counts": result_counters.copy()
}

try:
    tree = ET.parse(xml_file)
    root = tree.getroot()

    output["benchmark_id"] = root.attrib.get("id", "")
    title_elem = root.find("cdf:title", NS)
    if title_elem is not None and title_elem.text:
        output["benchmark_title"] = title_elem.text.strip()

    test_result = root.find("cdf:TestResult", NS)
    if test_result is None:
        raise ValueError("No se encontró el nodo TestResult en el XML")

    output["test_result_id"] = test_result.attrib.get("id", "")
    output["start_time"] = test_result.attrib.get("start-time", "")
    output["end_time"] = test_result.attrib.get("end-time", "")

    profile_elem = test_result.find("cdf:profile", NS)
    if profile_elem is not None and profile_elem.text:
        output["profile_id"] = profile_elem.text.strip()

    score_elem = test_result.find("cdf:score", NS)
    if score_elem is not None and score_elem.text:
        try:
            output["score"] = float(score_elem.text.strip())
        except ValueError:
            output["score"] = 0.0

    if output["profile_id"]:
        for profile in root.findall("cdf:Profile", NS):
            if profile.attrib.get("id") == output["profile_id"]:
                ptitle = profile.find("cdf:title", NS)
                if ptitle is not None and ptitle.text:
                    output["profile_title"] = ptitle.text.strip()
                break

    rule_map = {}
    for rule in root.findall(".//cdf:Rule", NS):
        rule_id = rule.attrib.get("id", "")
        rule_title_elem = rule.find("cdf:title", NS)
        severity = rule.attrib.get("severity", "")
        rule_map[rule_id] = {
            "title": rule_title_elem.text.strip() if rule_title_elem is not None and rule_title_elem.text else "",
            "severity": severity
        }

    for rule_result in test_result.findall("cdf:rule-result", NS):
        rule_id = rule_result.attrib.get("idref", "")
        result_elem = rule_result.find("cdf:result", NS)
        result_value = result_elem.text.strip().lower() if result_elem is not None and result_elem.text else "unknown"

        if result_value not in output["counts"]:
            output["counts"][result_value] = 0

        output["counts"][result_value] += 1

        output["rules"].append({
            "id": rule_id,
            "result": result_value,
            "severity": rule_map.get(rule_id, {}).get("severity", ""),
            "title": rule_map.get(rule_id, {}).get("title", "")
        })

    print(json.dumps(output, indent=2))

except Exception as exc:
    print(json.dumps({
        "error": str(exc)
    }))
    sys.exit(1)