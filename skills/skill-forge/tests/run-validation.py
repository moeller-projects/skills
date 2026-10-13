#!/usr/bin/env python3
"""Exercise frontmatter, manifest, discovery, and optional packaging behavior.

Run only with explicit test authorization. --include-packaging additionally
requires explicit packaging authorization and creates disposable archives.
"""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_DIR / "scripts"
spec = importlib.util.spec_from_file_location("forge_validator", SCRIPTS / "validate_skill.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
INCLUDE_PACKAGING = "--include-packaging" in sys.argv


class ForgeValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "example-skill"
        self.skill.mkdir()
        self.frontmatter = {
            "name": "example-skill",
            "description": "Use when collecting a complete inventory of supported example resources.",
            "metadata": {"title": "Example", "version": "1.0.0", "summary": "Collect resources.", "invocation": "model"},
        }
        self.manifest = {"name": "example-skill", **self.frontmatter["metadata"]}
        self.save()

    def save(self, links=""):
        rows = ["---"]
        for key, value in self.frontmatter.items():
            if isinstance(value, dict):
                rows.append(key + ":")
                rows.extend("  " + child + ": " + json.dumps(item) for child, item in value.items())
            else:
                rows.append(key + ": " + json.dumps(value))
        rows.extend(["---", "# Example", links])
        (self.skill / "SKILL.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
        (self.skill / "metadata.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def report(self):
        return validator.validate_skill(self.skill)

    def test_valid_manifest_and_conditional_resources(self):
        for folder in ("rules", "tests", "evals"):
            (self.skill / folder).mkdir()
            (self.skill / folder / "resource.txt").write_text("resource", encoding="utf-8")
        self.save("\n".join(f"- `{folder}/resource.txt` — read when checking {folder}." for folder in ("rules", "tests", "evals")))
        self.assertEqual(self.report(), {"errors": [], "warnings": []})

    def test_each_manifest_identity_field_must_match(self):
        for key in ("name", "title", "version", "summary", "invocation"):
            with self.subTest(field=key):
                original = self.manifest[key]
                self.manifest[key] = "different"
                self.save()
                self.assertTrue(self.report()["errors"])
                self.manifest[key] = original

    def test_metadata_values_and_tool_types_are_checked(self):
        for metadata in ({"metadata": {"version": 7}}, {"allowed-tools": ["Read"]}):
            with self.subTest(frontmatter=metadata):
                self.assertTrue(validator.check_metadata_fields(metadata))
        self.frontmatter["metadata"]["version"] = 7
        self.save()
        self.assertTrue(self.report()["errors"])
        self.frontmatter["metadata"]["version"] = "1.0.0"
        self.frontmatter["compatibility"] = ""
        self.save()
        self.assertTrue(self.report()["errors"])

    def test_read_only_tool_declaration_must_match_manifest(self):
        self.frontmatter["allowed-tools"] = "Read Bash(git:*)"
        self.manifest["allowed_tools"] = ["Read"]
        self.save()
        self.assertTrue(self.report()["errors"])
        self.manifest["allowed_tools"].append("Bash(git:*)")
        self.save()
        self.assertFalse(self.report()["errors"])

    def test_rules_tests_and_evals_are_not_hidden_from_discovery(self):
        for folder in ("rules", "tests", "evals"):
            with self.subTest(folder=folder):
                directory = self.skill / folder
                directory.mkdir()
                resource = directory / "resource.txt"
                resource.write_text("resource", encoding="utf-8")
                self.assertTrue(self.report()["warnings"])
                resource.unlink()
                directory.rmdir()

    def test_missing_rule_and_test_links_are_reported(self):
        for folder in ("rules", "tests", "evals"):
            with self.subTest(folder=folder):
                self.save(f"Read [{folder}]({folder}/absent.txt) when checking it.")
                self.assertTrue(self.report()["warnings"])

    def test_parenthetical_prose_is_not_a_missing_link(self):
        self.save("Apply the policy (see rules/ only when it is bundled).")
        self.assertEqual(self.report(), {"errors": [], "warnings": []})

    def test_names_are_not_silently_trimmed(self):
        self.assertTrue(validator.check_name(" example-skill ", "example-skill"))

    def test_invalid_manifest_is_a_validation_error(self):
        for content in ("[]", "{broken"):
            with self.subTest(content=content):
                (self.skill / "metadata.json").write_text(content, encoding="utf-8")
                self.assertTrue(self.report()["errors"])

    @unittest.skipUnless(INCLUDE_PACKAGING, "requires separate packaging authorization")
    def test_first_and_repeat_packages_exclude_generated_archives(self):
        artifact = self.skill / "example-skill.skill"
        (self.skill / "old.skill").write_bytes(b"previous package")
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        for attempt in range(2):
            result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "package_skill.py"), str(self.skill), str(self.skill), "--strict"], capture_output=True, text=True, encoding="utf-8", env=env, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "packaged")
            with zipfile.ZipFile(artifact) as archive:
                self.assertEqual(set(archive.namelist()), {"example-skill/SKILL.md", "example-skill/metadata.json"})
                self.assertEqual(json.loads(archive.read("example-skill/metadata.json")), self.manifest)
            self.assertEqual(report["file_count"], 2)


if __name__ == "__main__":
    if "--help" in sys.argv:
        print("Usage: python tests/run-validation.py [--include-packaging]\nTests require authorization; packaging additionally requires its own authorization.")
    else:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
