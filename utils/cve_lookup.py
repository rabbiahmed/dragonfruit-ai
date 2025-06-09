# utils/cve_lookup.py
# NVD API
# Without a key: 5 requests every 30 seconds
# With a key: 50 requests every 30 seconds
# Get a key here: https://nvd.nist.gov/developers/request-an-api-key

import re
import requests


def lookup_cve(keyword, results_per_page=5):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "keywordSearch": keyword,
        "resultsPerPage": results_per_page,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        cve_items = data.get("vulnerabilities", [])
        if not cve_items:
            return f"No CVEs found for keyword: {keyword}"

        results = []
        for item in cve_items:
            cve = item.get("cve", {})
            cve_id = cve.get("id", "N/A")
            description = next(
                (d.get("value") for d in cve.get("descriptions", []) if d.get("lang") == "en"),
                "No description available."
            )

            # Try CVSS v3.1 first, then fallback to v2 if needed
            metrics = cve.get("metrics", {})
            cvss_data = None
            severity = "N/A"
            score = "N/A"

            if "cvssMetricV31" in metrics:
                cvss_data = metrics["cvssMetricV31"][0]["cvssData"]
            elif "cvssMetricV2" in metrics:
                cvss_data = metrics["cvssMetricV2"][0]["cvssData"]

            if cvss_data:
                score = cvss_data.get("baseScore", "N/A")
                severity = cvss_data.get("baseSeverity", "N/A")

            published = cve.get("published", "N/A")
            last_modified = cve.get("lastModified", "N/A")

            # Check for duplicate mention in description
            match = re.search(r'duplicate of (CVE-\d{4}-\d+)', description, re.IGNORECASE)
            duplicate_of = match.group(1) if match else None

            if duplicate_of:
                results.append(
                    f"🔁 **{cve_id}** is a duplicate of **{duplicate_of}**\n"
                    f"📝 {description}"
                )
            else:
                results.append(
                    f"  **{cve_id}**\n"
                    f"📅 Published: {published}, Last Modified: {last_modified}\n"
                    f"📊 Severity: **{severity}** | CVSS Score: **{score}**\n"
                    f"📝 {description}\n"
                )

        return "\n\n".join(results)

    except requests.RequestException as e:
        return f"Error querying NVD: {str(e)}"


# Local testing block
if __name__ == "__main__":
    test_cases = [
        "CVE-2023-4863",
        "nginx",
        "windows 11 vulnerability",
        "invalid-cve-id"
    ]

    for query in test_cases:
        print(f"\n🔎 Testing query: {query}")
        print(lookup_cve(query))


