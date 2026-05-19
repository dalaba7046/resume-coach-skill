#!/usr/bin/env python3
"""
yaml_helpers.py -- RenderCV YAML toolkit for the resume-coach skill.

Three subcommands:
  validate <file>           Validate structure against the RenderCV schema
  diff <a> <b>              Resume-aware diff between a master and JD-customized YAML
  check <file> [--profile]  Hallucination guard -- flags suspicious tech and, optionally,
                            companies/projects not in a user-context profile

Usage:
  python scripts/yaml_helpers.py validate my_cv.yaml
  python scripts/yaml_helpers.py diff master.yaml jd_custom.yaml
  python scripts/yaml_helpers.py check my_cv.yaml
  python scripts/yaml_helpers.py check my_cv.yaml --profile references/user-context.md

Dependencies:
  pip install pyyaml
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def _c(code, text):
    if not sys.stdout.isatty():
        return text
    return "\033[" + code + "m" + text + "\033[0m"

def OK(t):   return _c("32", t)
def WARN(t): return _c("33", t)
def ERR(t):  return _c("31", t)
def BOLD(t): return _c("1",  t)
def DIM(t):  return _c("2",  t)
def CYAN(t): return _c("36", t)

# ---------------------------------------------------------------------------
# Generic blocklist -- companies / tech the model commonly hallucinates
# (not user-specific; applies to everyone)
# ---------------------------------------------------------------------------

# Big-tech names that should never appear as a user's *employer*
# unless the user has explicitly listed them in their profile.
SUSPICIOUS_COMPANY_TOKENS = [
    "meta", "facebook", "amazon web services", "microsoft", "apple",
    "netflix", "uber", "airbnb", "twitter", "x corp", "openai",
    "alibaba", "tencent", "bytedance", "shopee", "grab",
    "line corp", "rakuten", "samsung", "huawei",
]

# Technologies the model often adds that are not in the user's stack.
# Extend this list in your own fork as needed.
SUSPICIOUS_TECH_TOKENS = [
    "kubernetes", "k8s",
    "react", "next.js", "nextjs", "vue.js", "vuejs", "angular",
    "typescript",
    "node.js", "nodejs",
    "django", "fastapi", "spring boot", "spring",
    "golang", "go lang",
    "rust lang",
    "scala",
    "apache spark", "pyspark", "hadoop", "kafka", "airflow",
    "terraform", "ansible", "jenkins", "circleci",
    "graphql",
    "redis", "mongodb", "postgresql", "postgres",
    "c++", "c#", ".net", "dotnet", "ruby on rails",
    "flutter", "objective-c",
    "langchain", "openai api", "gpt-4", "chatgpt",
]

DATE_RE = re.compile(r"^\d{4}-\d{2}$")

# ---------------------------------------------------------------------------
# Profile loader -- reads user-context.md to extract allowed employers/projects
# ---------------------------------------------------------------------------

def load_profile(profile_path):
    """
    Parse a user-context.md file and extract:
      - allowed_companies: strings found under the Career Timeline table
      - canonical_projects: strings found under Key Projects headings

    Returns a dict with keys 'companies' and 'projects' (both lists of lowercase strings).
    Returns None if the file cannot be parsed meaningfully.
    """
    try:
        text = Path(profile_path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return None

    companies = []
    projects  = []

    for line in text.splitlines():
        # Career Timeline table rows: | period | Company — Title | stack |
        if "|" in line and ("–" in line or "-" in line or "present" in line.lower()):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                cell = parts[2].lower()  # "Company / Role" column
                # Pull the company name (before the em-dash)
                company_part = re.split(r"—|-{2}", cell)[0].strip()
                if company_part and len(company_part) > 2:
                    companies.append(company_part)

        # Key Projects headings: ### Project Name — context
        m = re.match(r"^###\s+(.+?)(?:\s*—.*)?$", line)
        if m:
            name = m.group(1).strip().lower()
            if name and not name.startswith("["):  # skip unfilled placeholders
                projects.append(name)

    return {"companies": companies, "projects": projects}

# ---------------------------------------------------------------------------
# YAML loader
# ---------------------------------------------------------------------------

def load_yaml(path):
    try:
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(ERR("File not found: " + str(path)), file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(ERR("YAML parse error:\n" + str(exc)), file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print(ERR(str(path) + " does not contain a top-level YAML mapping."), file=sys.stderr)
        sys.exit(1)
    return data

# ---------------------------------------------------------------------------
# VALIDATE
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.errors   = []
        self.warnings = []
    def err(self, msg):  self.errors.append(msg)
    def warn(self, msg): self.warnings.append(msg)
    def ok(self):        return not self.errors


def check_date(value, field, report):
    if not isinstance(value, str):
        report.err(field + ": expected string date, got " + type(value).__name__)
        return
    if value == "present":
        return
    if not DATE_RE.match(value):
        report.err(field + ": " + repr(value) + " invalid -- use YYYY-MM or 'present'")


def validate_experience(entries, report):
    if not isinstance(entries, list):
        report.err("cv.sections.experience: expected a list"); return
    for i, e in enumerate(entries):
        p = "cv.sections.experience[" + str(i) + "]"
        if not isinstance(e, dict):
            report.err(p + ": expected a mapping"); continue
        for req in ("company", "position", "start_date", "highlights"):
            if req not in e:
                report.err(p + ": missing '" + req + "'")
        if "start_date" in e: check_date(e["start_date"], p + ".start_date", report)
        if "end_date"   in e: check_date(e["end_date"],   p + ".end_date",   report)
        hi = e.get("highlights")
        if hi is not None and (not isinstance(hi, list) or not hi):
            report.err(p + ".highlights: must be a non-empty list")


def validate_skills(entries, report):
    if not isinstance(entries, list):
        report.err("cv.sections.skills: expected a list"); return
    for i, e in enumerate(entries):
        p = "cv.sections.skills[" + str(i) + "]"
        if not isinstance(e, dict):
            report.err(p + ": expected a mapping"); continue
        if "label"   not in e: report.err(p + ": missing 'label' (grouped structure required)")
        if "details" not in e: report.err(p + ": missing 'details' (grouped structure required)")


def validate_key_projects(entries, report):
    if not isinstance(entries, list):
        report.err("cv.sections.key_projects: expected a list"); return
    for i, e in enumerate(entries):
        p = "cv.sections.key_projects[" + str(i) + "]"
        if not isinstance(e, dict):
            report.err(p + ": expected a mapping"); continue
        for req in ("name", "highlights"):
            if req not in e: report.err(p + ": missing '" + req + "'")


def print_report(report):
    for e in report.errors:
        print("  " + ERR("x") + " " + e)
    for w in report.warnings:
        print("  " + WARN("!") + " " + w)
    if not report.errors and not report.warnings:
        print("  " + OK("OK") + " All checks passed.")
    elif not report.errors:
        print("\n  " + OK("OK") + " No errors. " + str(len(report.warnings)) + " warning(s) above.")
    else:
        print("\n  " + ERR("FAIL") + " " + str(len(report.errors)) + " error(s), " +
              str(len(report.warnings)) + " warning(s).")
    print()


def cmd_validate(args):
    path = Path(args.file)
    data = load_yaml(path)
    report = Report()
    print(BOLD("\n--- validate: " + path.name + " ---\n"))

    if "cv" not in data:
        report.err("Top-level 'cv' key missing")
        print_report(report); return 1

    cv = data["cv"]
    for f in ("name", "headline", "sections"):
        if f not in cv: report.err("cv." + f + ": missing required field")

    sections = cv.get("sections") or {}
    if not isinstance(sections, dict):
        report.err("cv.sections: expected a mapping")
    else:
        for sec in ("summary", "experience", "key_projects", "skills"):
            if sec not in sections:
                report.warn("cv.sections." + sec + ": section missing")
        s = sections.get("summary")
        if s is not None and (not isinstance(s, list) or not s):
            report.err("cv.sections.summary: must be a non-empty list")
        if "experience"   in sections: validate_experience(sections["experience"],     report)
        if "skills"       in sections: validate_skills(sections["skills"],             report)
        if "key_projects" in sections: validate_key_projects(sections["key_projects"], report)

    settings = data.get("settings") or {}
    bk = settings.get("bold_keywords")
    if bk is None:
        report.warn("settings.bold_keywords: not found -- auto-bolding won't work")
    elif not isinstance(bk, list):
        report.err("settings.bold_keywords: expected a list")
    elif len(bk) > 12:
        report.warn("settings.bold_keywords: " + str(len(bk)) + " entries (recommended <=12)")

    print_report(report)
    return 0 if report.ok() else 1

# ---------------------------------------------------------------------------
# DIFF
# ---------------------------------------------------------------------------

def exp_key(e):   return str(e.get("company","?")) + " | " + str(e.get("position","?"))
def proj_key(e):  return str(e.get("name","?"))
def skill_key(e): return str(e.get("label","?"))


def diff_highlights(ea, eb):
    ha = ea.get("highlights", []) if ea else []
    hb = eb.get("highlights", [])
    sa, sb = set(ha), set(hb)
    for line in ha:
        if line not in sb:
            s = (line[:88] + "...") if len(line) > 88 else line
            print("      " + ERR("-") + " " + DIM(s))
    for line in hb:
        if line not in sa:
            s = (line[:88] + "...") if len(line) > 88 else line
            print("      " + OK("+") + " " + s)


def diff_skill_details(ea, eb):
    if ea is None:
        print("      details: " + str(eb.get("details", ""))); return
    da = {s.strip() for s in (ea.get("details") or "").split(",")}
    db = {s.strip() for s in (eb.get("details") or "").split(",")}
    for r in sorted(da - db): print("      " + ERR("-") + " " + r)
    for r in sorted(db - da): print("      " + OK("+") + " " + r)


def diff_section(al, bl, key_fn, detail_fn=None):
    am = {key_fn(e): e for e in (al or []) if isinstance(e, dict)}
    bm = {key_fn(e): e for e in (bl or []) if isinstance(e, dict)}
    keys = list(am) + [k for k in bm if k not in am]
    changed = False
    for key in keys:
        ia, ib = key in am, key in bm
        if ia and not ib:
            print("  " + ERR("- removed") + " " + BOLD(key)); changed = True
        elif not ia and ib:
            print("  " + OK("+ added") + "  " + BOLD(key))
            if detail_fn: detail_fn(None, bm[key])
            changed = True
        elif am[key] != bm[key]:
            print("  " + WARN("~ changed") + " " + BOLD(key))
            if detail_fn: detail_fn(am[key], bm[key])
            changed = True
    if not changed:
        print("  " + DIM("(no changes)"))


def cmd_diff(args):
    pa, pb = Path(args.file_a), Path(args.file_b)
    a, b = load_yaml(pa), load_yaml(pb)
    print(BOLD("\n--- diff: " + pa.name + "  ->  " + pb.name + " ---\n"))
    print("  " + ERR("-") + " removed   " + OK("+") + " added   " + WARN("~") + " changed\n")

    ca, cb = a.get("cv") or {}, b.get("cv") or {}
    for f in ("name", "headline"):
        va, vb = ca.get(f), cb.get(f)
        if va != vb:
            print(CYAN("[cv." + f + "]"))
            print("  " + ERR("-") + " " + str(va))
            print("  " + OK("+") + " " + str(vb))
            print()

    sa, sb = ca.get("sections") or {}, cb.get("sections") or {}

    summa, summb = sa.get("summary") or [], sb.get("summary") or []
    if summa != summb:
        print(CYAN("[cv.sections.summary]"))
        set_a, set_b = set(summa), set(summb)
        for line in summa:
            if line not in set_b:
                s = (line[:100] + "...") if len(line) > 100 else line
                print("  " + ERR("-") + " " + DIM(s))
        for line in summb:
            if line not in set_a:
                s = (line[:100] + "...") if len(line) > 100 else line
                print("  " + OK("+") + " " + s)
        print()

    print(CYAN("[cv.sections.experience]"))
    diff_section(sa.get("experience"), sb.get("experience"), exp_key, diff_highlights)
    print()

    print(CYAN("[cv.sections.key_projects]"))
    diff_section(sa.get("key_projects"), sb.get("key_projects"), proj_key, diff_highlights)
    print()

    print(CYAN("[cv.sections.skills]"))
    diff_section(sa.get("skills"), sb.get("skills"), skill_key, diff_skill_details)
    print()

    bka = set((a.get("settings") or {}).get("bold_keywords") or [])
    bkb = set((b.get("settings") or {}).get("bold_keywords") or [])
    if bka != bkb:
        print(CYAN("[settings.bold_keywords]"))
        for r in sorted(bka - bkb): print("  " + ERR("-") + " " + r)
        for r in sorted(bkb - bka): print("  " + OK("+") + " " + r)
        print()

    return 0

# ---------------------------------------------------------------------------
# CHECK
# ---------------------------------------------------------------------------

def all_strings(data):
    result = []
    def walk(node):
        if isinstance(node, str):    result.append(node)
        elif isinstance(node, list): [walk(i) for i in node]
        elif isinstance(node, dict): [walk(v) for v in node.values()]
    walk(data)
    return result


def cmd_check(args):
    path = Path(args.file)
    data = load_yaml(path)
    strings    = all_strings(data)
    text_lower = " ".join(strings).lower()

    total_err  = 0
    total_warn = 0

    print(BOLD("\n--- check: " + path.name + " ---\n"))

    # Load user profile (optional)
    profile = None
    if args.profile:
        profile = load_profile(args.profile)
        if profile:
            print(DIM("  Profile loaded: " + str(len(profile["companies"])) +
                      " companies, " + str(len(profile["projects"])) + " projects\n"))
        else:
            print(WARN("!") + " Could not parse profile at " + args.profile +
                  " -- skipping company/project checks\n")

    # 1. Experience companies ---------------------------------------------------
    print(CYAN("1. Experience companies"))
    sections   = (data.get("cv") or {}).get("sections") or {}
    experience = sections.get("experience") or []

    for i, entry in enumerate(experience):
        if not isinstance(entry, dict): continue
        company = str(entry.get("company", "")).lower()
        raw     = entry.get("company", "")

        bad = next((t for t in SUSPICIOUS_COMPANY_TOKENS if t in company), None)
        if bad:
            print("  " + ERR("FAIL") + " experience[" + str(i) + "].company: '" + raw +
                  "' -- '" + bad + "' looks hallucinated")
            total_err += 1
        elif profile and profile["companies"]:
            allowed = any(token in company for token in profile["companies"])
            if allowed:
                print("  " + OK("OK") + "   experience[" + str(i) + "].company: " + raw)
            else:
                print("  " + WARN("WARN") + " experience[" + str(i) + "].company: '" + raw +
                      "' -- not in profile. Verify.")
                total_warn += 1
        else:
            print("  " + DIM("  ?  ") + " experience[" + str(i) + "].company: " + raw +
                  " (no profile loaded -- skipping allowlist check)")

    if not experience:
        print("  " + WARN("WARN") + " No experience entries found.")
        total_warn += 1
    print()

    # 2. Key project names ------------------------------------------------------
    print(CYAN("2. Key project names"))
    projects = sections.get("key_projects") or []

    for i, entry in enumerate(projects):
        if not isinstance(entry, dict): continue
        name = str(entry.get("name", "")).lower()
        raw  = entry.get("name", "")

        if profile and profile["projects"]:
            if any(p in name or name in p for p in profile["projects"]):
                print("  " + OK("OK") + "   key_projects[" + str(i) + "]: " + raw)
            else:
                print("  " + WARN("WARN") + " key_projects[" + str(i) + "]: '" + raw +
                      "' -- not in profile project list")
                total_warn += 1
        else:
            print("  " + DIM("  ?  ") + " key_projects[" + str(i) + "]: " + raw +
                  " (no profile -- skipping check)")

    if not projects:
        print("  " + DIM("(no key_projects section)"))
    print()

    # 3. Suspicious tech --------------------------------------------------------
    print(CYAN("3. Technology stack"))
    hits = []
    for tech in SUSPICIOUS_TECH_TOKENS:
        pat = re.compile(r"(?<![a-zA-Z0-9])" + re.escape(tech) + r"(?![a-zA-Z0-9])", re.IGNORECASE)
        if pat.search(text_lower):
            hits.append(tech)
    if hits:
        for tech in hits:
            print("  " + WARN("WARN") + " '" + tech +
                  "' found -- not in the default allowed stack. Confirm before publishing.")
            total_warn += 1
    else:
        print("  " + OK("OK") + "   No flagged technologies detected.")
    print()

    # Summary -------------------------------------------------------------------
    print(BOLD("--- Summary ---"))
    if total_err == 0 and total_warn == 0:
        print(OK("OK") + " Clean -- no issues detected.\n")
        return 0
    if total_err:
        print(ERR("FAIL " + str(total_err) + " error(s)") + " -- likely fabricated content.")
    if total_warn:
        print(WARN("WARN " + str(total_warn) + " warning(s)") + " -- review before publishing.")
    print()
    return 1 if total_err else 0

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="yaml_helpers.py",
        description="RenderCV YAML toolkit -- validate, diff, hallucination-check.",
        epilog=(
            "examples:\n"
            "  python scripts/yaml_helpers.py validate my_cv.yaml\n"
            "  python scripts/yaml_helpers.py diff master.yaml jd_custom.yaml\n"
            "  python scripts/yaml_helpers.py check my_cv.yaml\n"
            "  python scripts/yaml_helpers.py check my_cv.yaml --profile references/user-context.md"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("validate", help="Validate YAML structure")
    pv.add_argument("file")

    pd = sub.add_parser("diff", help="Resume-aware diff between two YAMLs")
    pd.add_argument("file_a")
    pd.add_argument("file_b")

    pc = sub.add_parser("check", help="Hallucination guard")
    pc.add_argument("file")
    pc.add_argument("--profile", default=None,
                    help="Path to user-context.md for company/project allowlist checks")

    args = parser.parse_args()
    if args.cmd == "validate": sys.exit(cmd_validate(args))
    elif args.cmd == "diff":   sys.exit(cmd_diff(args))
    elif args.cmd == "check":  sys.exit(cmd_check(args))


if __name__ == "__main__":
    main()
