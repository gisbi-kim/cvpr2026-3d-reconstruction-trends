import csv
import html
import json
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path


SOURCE_URL = "https://gisbi-kim.github.io/cvpr2026-explorer/output/cvpr2026_explorer.html"
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "output"


GROUPS = {
    "vggt_lineage": {
        "label": "VGGT / feed-forward geometry",
        "weight": 28,
        "terms": [
            r"\bVGGT\b",
            r"visual geometry grounded transformer",
            r"visual geometric transformer",
            r"visual geometry",
            r"feed[- ]forward reconstruction",
            r"point map",
            r"\bDUSt3R\b",
            r"\bMASt3R\b",
            r"\bCroCo\b",
        ],
    },
    "general_reconstruction": {
        "label": "General 3D reconstruction / multiview",
        "weight": 22,
        "terms": [
            r"3d reconstruction",
            r"scene reconstruction",
            r"surface reconstruction",
            r"multi[- ]view",
            r"\bmultiview\b",
            r"structure from motion",
            r"\bSfM\b",
            r"\bMVS\b",
            r"bundle adjustment",
            r"triangulation",
            r"3d registration",
        ],
    },
    "gaussian_radiance": {
        "label": "Gaussian / radiance field / view synthesis",
        "weight": 20,
        "terms": [
            r"\bGaussian\b",
            r"\b3DGS\b",
            r"splatting",
            r"radiance field",
            r"\bNeRF\b",
            r"novel view",
            r"view synthesis",
            r"differentiable rendering",
        ],
    },
    "pose_calibration_localization": {
        "label": "Pose / calibration / localization",
        "weight": 15,
        "terms": [
            r"camera pose",
            r"pose estimation",
            r"pose alignment",
            r"calibration",
            r"localization",
            r"relocalization",
            r"registration",
            r"pose graph",
            r"\bSLAM\b",
        ],
    },
    "depth_correspondence": {
        "label": "Depth / stereo / dense correspondence",
        "weight": 11,
        "terms": [
            r"\bdepth\b",
            r"monocular depth",
            r"\bstereo\b",
            r"surface normal",
            r"normal estimation",
            r"correspondence",
            r"\bmatching\b",
            r"keypoint",
        ],
    },
    "dynamic_4d": {
        "label": "Dynamic / 4D reconstruction",
        "weight": 16,
        "terms": [
            r"\b4D\b",
            r"dynamic 3d",
            r"dynamic scene",
            r"deformable",
            r"streaming 3d",
            r"temporal",
            r"video[- ]to[- ]3d",
        ],
    },
    "surface_occupancy": {
        "label": "Mesh / surface / implicit / occupancy",
        "weight": 13,
        "terms": [
            r"\bmesh\b",
            r"\bsurface\b",
            r"\bimplicit\b",
            r"\boccupancy\b",
            r"\bSDF\b",
            r"\bvoxel\b",
            r"point cloud",
        ],
    },
    "robotics_mapping": {
        "label": "Mapping / autonomous / embodied",
        "weight": 12,
        "terms": [
            r"\bmapping\b",
            r"active mapping",
            r"autonomous driving",
            r"\bBEV\b",
            r"world model",
            r"embodied",
            r"navigation",
            r"occupancy prediction",
        ],
    },
    "generation_editing": {
        "label": "3D generation / editing bridge",
        "weight": 8,
        "terms": [
            r"3d generation",
            r"scene generation",
            r"3d editing",
            r"editing",
            r"text[- ]to[- ]3d",
            r"image[- ]to[- ]3d",
            r"video generation",
        ],
    },
    "data_benchmark": {
        "label": "Dataset / benchmark / evaluation",
        "weight": 8,
        "terms": [
            r"\bdataset\b",
            r"\bbenchmark\b",
            r"evaluation",
            r"large[- ]scale",
            r"real[- ]world",
        ],
    },
}


INPUT_PATTERNS = [
    ("single image", [r"single image", r"single-view", r"monocular"]),
    ("sparse multi-view", [r"sparse view", r"sparse multi[- ]view", r"sparse images"]),
    ("multi-view images", [r"multi[- ]view", r"\bmultiview\b", r"posed images"]),
    ("video / temporal", [r"\bvideo\b", r"temporal", r"dynamic scene", r"streaming"]),
    ("panorama", [r"panorama", r"panoramic", r"360"]),
    ("LiDAR / driving", [r"\bLiDAR\b", r"autonomous driving", r"\bBEV\b"]),
    ("RGB-D / depth", [r"rgb[- ]d", r"\bdepth\b"]),
    ("multimodal / language", [r"language", r"text", r"multimodal", r"referring"]),
]

OUTPUT_PATTERNS = [
    ("camera pose", [r"camera pose", r"pose estimation", r"pose alignment"]),
    ("depth / normals", [r"\bdepth\b", r"surface normal", r"normal estimation"]),
    ("point map / point cloud", [r"point map", r"point cloud"]),
    ("Gaussian map", [r"\bGaussian\b", r"\b3DGS\b", r"splatting"]),
    ("mesh / surface", [r"\bmesh\b", r"surface reconstruction", r"\bsurface\b"]),
    ("occupancy / voxel", [r"\boccupancy\b", r"\bvoxel\b"]),
    ("radiance field / NVS", [r"radiance field", r"\bNeRF\b", r"novel view", r"view synthesis"]),
    ("4D scene", [r"\b4D\b", r"dynamic 3d", r"dynamic scene", r"deformable"]),
    ("editable / generative 3D", [r"editing", r"generation", r"text[- ]to[- ]3d", r"image[- ]to[- ]3d"]),
]

CLAIM_PATTERNS = [
    ("foundation/prior", [r"foundation", r"pre[- ]training", r"prior", r"generalizable", r"generalization"]),
    ("unified pipeline", [r"unified", r"end[- ]to[- ]end", r"feed[- ]forward", r"one[- ]stage"]),
    ("efficiency", [r"efficient", r"fast", r"linear[- ]time", r"real[- ]time", r"cache", r"token merging", r"compressed"]),
    ("scale", [r"large[- ]scale", r"scalable", r"long[- ]term", r"scene[- ]scale"]),
    ("robustness", [r"robust", r"outlier", r"in[- ]the[- ]wild", r"transparent", r"reflective", r"low[- ]texture"]),
    ("dynamic", [r"dynamic", r"\b4D\b", r"deformable", r"temporal", r"streaming"]),
    ("benchmark/data", [r"\bdataset\b", r"\bbenchmark\b", r"evaluation"]),
    ("editing/generation", [r"editing", r"generation", r"compositional", r"text[- ]to[- ]3d"]),
]


def norm_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(str(x) for x in value)
    return str(value)


def match_terms(text, terms):
    hits = []
    for pattern in terms:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(pattern)
    return hits


def first_matches(text, pattern_groups):
    labels = []
    for label, patterns in pattern_groups:
        if match_terms(text, patterns):
            labels.append(label)
    return labels


def classify_role(score, groups, paper):
    phylum = norm_text(paper.get("primary_phylum"))
    genus = norm_text(paper.get("primary_genus"))
    core_groups = {"vggt_lineage", "general_reconstruction", "gaussian_radiance", "dynamic_4d"}
    if score >= 92 and (core_groups & set(groups)):
        return "core trend paper"
    if score >= 68 and len(groups) >= 2:
        return "important bridge paper"
    if "3D Vision & Geometry" in phylum and score >= 45:
        return "specialized geometry paper"
    if genus in {"3D Reconstruction", "3D Gaussian Splatting", "Pose Estimation"} and score >= 40:
        return "specialized geometry paper"
    return "adjacent / inspect manually"


def strategic_note(groups, role, inputs, outputs, claims):
    labels = [GROUPS[g]["label"] for g in groups]
    if "vggt_lineage" in groups:
        return "Use as evidence that multi-view geometry is becoming a feed-forward foundation-model problem."
    if "gaussian_radiance" in groups and "dynamic_4d" in groups:
        return "Use as evidence that Gaussian/radiance representations are moving from static NVS toward dynamic scene models."
    if "gaussian_radiance" in groups and "pose_calibration_localization" in groups:
        return "Use as a bridge between reconstruction representation and metric pose/calibration reliability."
    if "robotics_mapping" in groups and ("surface_occupancy" in groups or "pose_calibration_localization" in groups):
        return "Use for the robotics/SLAM angle: reconstruction becomes a map or world model, not just a visual asset."
    if "data_benchmark" in groups and len(groups) <= 2:
        return "Likely useful as evaluation context, but not necessarily the central technical thesis."
    if role == "core trend paper":
        return "Read early; it likely changes the framing of the 3D reconstruction cluster."
    if role == "important bridge paper":
        return "Use to connect two clusters in the blog narrative."
    if labels:
        return "Useful for a cluster subsection, but check whether the contribution is broad or narrowly incremental."
    return "Low-confidence match; inspect before using."


def get_json_payload():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        page = response.read().decode("utf-8")
    match = re.search(
        r'<script id="app-data" type="application/json">(.*?)</script>',
        page,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find app-data JSON in explorer HTML")
    # The app-data block is already valid JSON. Do not HTML-unescape it:
    # author strings can contain escaped quotes such as &quot;, and unescaping
    # before JSON parsing turns them into invalid bare quotes.
    payload = json.loads(match.group(1))
    (DATA_DIR / "cvpr2026_app_data.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return payload


def analyze_paper(paper):
    text = " ".join(
        [
            norm_text(paper.get("title")),
            norm_text(paper.get("abstract")),
            norm_text(paper.get("primary_phylum")),
            norm_text(paper.get("primary_genus")),
            norm_text(paper.get("topics")),
        ]
    )
    matched_groups = []
    matched_terms = []
    score = 0
    for group, spec in GROUPS.items():
        hits = match_terms(text, spec["terms"])
        if hits:
            matched_groups.append(group)
            matched_terms.extend(hits)
            score += spec["weight"] + min(8, len(hits) * 2)

    phylum = norm_text(paper.get("primary_phylum"))
    genus = norm_text(paper.get("primary_genus"))
    if phylum == "3D Vision & Geometry":
        score += 12
    if genus in {"3D Reconstruction", "3D Gaussian Splatting", "Pose Estimation"}:
        score += 12
    if "Learning Algorithms" in phylum and "vggt_lineage" in matched_groups:
        score += 8
    if len(matched_groups) >= 3:
        score += 8
    if len(matched_groups) >= 5:
        score += 6

    inputs = first_matches(text, INPUT_PATTERNS)
    outputs = first_matches(text, OUTPUT_PATTERNS)
    claims = first_matches(text, CLAIM_PATTERNS)

    score = min(score, 100)
    role = classify_role(score, matched_groups, paper)
    return {
        "score": score,
        "matched_groups": matched_groups,
        "matched_terms": sorted(set(matched_terms)),
        "inputs": inputs,
        "outputs": outputs,
        "claims": claims,
        "role": role,
        "strategic_note": strategic_note(matched_groups, role, inputs, outputs, claims),
    }


def should_include_broad(result, paper):
    if result["score"] >= 35:
        return True
    phylum = norm_text(paper.get("primary_phylum"))
    genus = norm_text(paper.get("primary_genus"))
    if phylum == "3D Vision & Geometry" and result["matched_groups"]:
        return True
    if genus in {"3D Reconstruction", "3D Gaussian Splatting", "Pose Estimation"}:
        return True
    return False


def should_include_strict(result, paper):
    groups = set(result["matched_groups"])
    title_abs = f"{norm_text(paper.get('title'))} {norm_text(paper.get('abstract'))}"
    phylum = norm_text(paper.get("primary_phylum"))
    genus = norm_text(paper.get("primary_genus"))

    primary_geometry = phylum == "3D Vision & Geometry" or genus in {
        "3D Reconstruction",
        "3D Gaussian Splatting",
        "Pose Estimation",
    }
    cross_recon = {
        "vggt_lineage",
        "general_reconstruction",
        "gaussian_radiance",
        "pose_calibration_localization",
        "dynamic_4d",
        "surface_occupancy",
        "robotics_mapping",
    }

    if "vggt_lineage" in groups:
        return True
    if primary_geometry and groups & cross_recon:
        return True
    if {"general_reconstruction", "gaussian_radiance"} <= groups:
        return True
    if {"general_reconstruction", "dynamic_4d"} <= groups:
        return True
    if {"gaussian_radiance", "pose_calibration_localization"} <= groups:
        return True
    if "robotics_mapping" in groups and groups & {
        "general_reconstruction",
        "gaussian_radiance",
        "pose_calibration_localization",
        "surface_occupancy",
    }:
        if re.search(r"reconstruction|mapping|slam|localization|occupancy|world model|gaussian|pose", title_abs, flags=re.I):
            return True
    return False


def editorial_bucket(result, paper):
    groups = set(result["matched_groups"])
    phylum = norm_text(paper.get("primary_phylum"))
    genus = norm_text(paper.get("primary_genus"))
    primary_geometry = phylum == "3D Vision & Geometry" or genus in {
        "3D Reconstruction",
        "3D Gaussian Splatting",
        "Pose Estimation",
    }
    if "vggt_lineage" in groups:
        return "A. thesis anchor: VGGT/feed-forward geometry"
    if primary_geometry and {"general_reconstruction", "gaussian_radiance"} <= groups:
        return "A. thesis anchor: representation shift"
    if primary_geometry and {"general_reconstruction", "dynamic_4d"} <= groups:
        return "A. thesis anchor: dynamic/4D recon"
    if primary_geometry and {"gaussian_radiance", "pose_calibration_localization"} <= groups:
        return "B. bridge: representation meets metric pose"
    if "robotics_mapping" in groups and primary_geometry:
        return "B. bridge: reconstruction becomes mapping/world model"
    if primary_geometry:
        return "C. cluster representative"
    return "D. adjacent but useful context"


def write_csv(rows, path):
    fieldnames = [
        "rank",
        "score",
        "role",
        "editorial_bucket",
        "title",
        "primary_phylum",
        "primary_genus",
        "matched_groups",
        "inputs",
        "outputs",
        "claims",
        "strategic_note",
        "paper_url",
        "paper_arxiv_id",
        "abstract",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, row in enumerate(rows, start=1):
            paper = row["paper"]
            result = row["result"]
            writer.writerow(
                {
                    "rank": idx,
                    "score": result["score"],
                    "role": result["role"],
                    "editorial_bucket": result["editorial_bucket"],
                    "title": norm_text(paper.get("title")),
                    "primary_phylum": norm_text(paper.get("primary_phylum")),
                    "primary_genus": norm_text(paper.get("primary_genus")),
                    "matched_groups": "; ".join(result["matched_groups"]),
                    "inputs": "; ".join(result["inputs"]),
                    "outputs": "; ".join(result["outputs"]),
                    "claims": "; ".join(result["claims"]),
                    "strategic_note": result["strategic_note"],
                    "paper_url": norm_text(paper.get("paper_url")),
                    "paper_arxiv_id": norm_text(paper.get("paper_arxiv_id")),
                    "abstract": norm_text(paper.get("abstract")).replace("\n", " "),
                }
            )
    return path


def write_summary_csv(rows):
    cluster_counter = Counter()
    role_counter = Counter()
    bucket_counter = Counter()
    cross_counter = Counter()
    for row in rows:
        result = row["result"]
        role_counter[result["role"]] += 1
        bucket_counter[result["editorial_bucket"]] += 1
        for group in result["matched_groups"]:
            cluster_counter[group] += 1
        groups = result["matched_groups"]
        for i, g1 in enumerate(groups):
            for g2 in groups[i + 1 :]:
                cross_counter[tuple(sorted((g1, g2)))] += 1

    path = OUT_DIR / "cvpr2026_3d_recon_cluster_summary.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["section", "name", "count", "label"])
        for group, count in cluster_counter.most_common():
            writer.writerow(["cluster", group, count, GROUPS[group]["label"]])
        for role, count in role_counter.most_common():
            writer.writerow(["role", role, count, ""])
        for bucket, count in bucket_counter.most_common():
            writer.writerow(["editorial_bucket", bucket, count, ""])
        for (g1, g2), count in cross_counter.most_common(30):
            writer.writerow(["cross_cluster", f"{g1} + {g2}", count, f"{GROUPS[g1]['label']} / {GROUPS[g2]['label']}"])
    return path, cluster_counter, role_counter, bucket_counter, cross_counter


def representative_rows(rows, group, limit=12):
    filtered = [r for r in rows if group in r["result"]["matched_groups"]]
    return sorted(filtered, key=lambda r: (-r["result"]["score"], norm_text(r["paper"].get("title"))))[:limit]


def select_seed_rows(strict_rows):
    quotas = {
        "A. thesis anchor: VGGT/feed-forward geometry": 30,
        "A. thesis anchor: representation shift": 35,
        "A. thesis anchor: dynamic/4D recon": 30,
        "B. bridge: reconstruction becomes mapping/world model": 25,
        "B. bridge: representation meets metric pose": 20,
        "C. cluster representative": 35,
        "D. adjacent but useful context": 10,
    }
    selected = []
    seen = set()

    def add(row):
        title = norm_text(row["paper"].get("title")).lower()
        if title in seen:
            return False
        seen.add(title)
        selected.append(row)
        return True

    for bucket, quota in quotas.items():
        bucket_rows = [
            row for row in strict_rows if row["result"]["editorial_bucket"] == bucket
        ]
        bucket_rows.sort(
            key=lambda r: (
                -r["result"]["score"],
                len(r["result"]["matched_groups"]) * -1,
                norm_text(r["paper"].get("title")).lower(),
            )
        )
        for row in bucket_rows[:quota]:
            add(row)

    # Guarantee coverage of each analytical cluster even if the bucket quotas
    # miss a representative title.
    for group in GROUPS:
        for row in representative_rows(strict_rows, group, limit=8):
            if len([r for r in selected if group in r["result"]["matched_groups"]]) >= 8:
                break
            add(row)

    selected.sort(
        key=lambda r: (
            r["result"]["editorial_bucket"],
            -r["result"]["score"],
            norm_text(r["paper"].get("title")).lower(),
        )
    )
    return selected


def write_markdown(rows, seed_rows, cluster_counter, role_counter, bucket_counter, cross_counter, total_papers, broad_count):
    md = []
    md.append("# CVPR 2026 3D Reconstruction Strategic Processing Brief")
    md.append("")
    md.append(f"Source: {SOURCE_URL}")
    md.append(f"Total explorer papers parsed: {total_papers}")
    md.append(f"Broad candidate papers selected: {broad_count}")
    md.append(f"Strict blog-reading candidate papers selected: {len(rows)}")
    md.append(f"Seed papers for first-pass blog reading: {len(seed_rows)}")
    md.append("")
    md.append("## Working Thesis")
    md.append("")
    md.append(
        "CVPR 2026 3D reconstruction is not one bucket. It is splitting into feed-forward geometry foundation models, Gaussian/radiance-field representations, pose-calibration-localization reliability, dynamic/4D scenes, and 3D generation/editing bridges. VGGT is useful as a lens, but too narrow as the only search term."
    )
    md.append("")
    md.append("## Cluster Counts")
    md.append("")
    for group, count in cluster_counter.most_common():
        md.append(f"- {GROUPS[group]['label']}: {count}")
    md.append("")
    md.append("## Editorial Triage")
    md.append("")
    for role, count in role_counter.most_common():
        md.append(f"- {role}: {count}")
    md.append("")
    md.append("## Blog Reading Buckets")
    md.append("")
    for bucket, count in bucket_counter.most_common():
        md.append(f"- {bucket}: {count}")
    md.append("")
    md.append("## Strong Cross-Cluster Signals")
    md.append("")
    for (g1, g2), count in cross_counter.most_common(12):
        md.append(f"- {GROUPS[g1]['label']} + {GROUPS[g2]['label']}: {count}")
    md.append("")
    md.append("## Cluster Reading Lists")
    for group in GROUPS:
        reps = representative_rows(rows, group, limit=10)
        if not reps:
            continue
        md.append("")
        md.append(f"### {GROUPS[group]['label']}")
        for item in reps:
            paper = item["paper"]
            result = item["result"]
            md.append(
                f"- [{result['score']:02d}] {norm_text(paper.get('title'))} | {result['role']} | {result['strategic_note']}"
            )
    md.append("")
    md.append("## First-Pass Seed List by Editorial Bucket")
    current_bucket = None
    for item in seed_rows:
        paper = item["paper"]
        result = item["result"]
        bucket = result["editorial_bucket"]
        if bucket != current_bucket:
            current_bucket = bucket
            md.append("")
            md.append(f"### {bucket}")
        md.append(
            f"- [{result['score']:02d}] {norm_text(paper.get('title'))} | {norm_text(paper.get('primary_phylum'))} / {norm_text(paper.get('primary_genus'))}"
        )
    md.append("")
    md.append("## Blog Structure Draft")
    md.append("")
    md.append("1. Why VGGT is the wrong but useful keyword")
    md.append("2. Feed-forward geometry as the new center of 3D reconstruction")
    md.append("3. Gaussian/radiance fields move from pretty rendering to maps, editing, and dynamic scenes")
    md.append("4. Pose, calibration, and localization become the reliability layer")
    md.append("5. Dynamic/4D reconstruction is the pressure test")
    md.append("6. What is central, what is incremental, and what is mostly application wrapping")
    md.append("7. Research wedge: metric online geometry priors for SLAM/robotics")
    md.append("")
    md.append("## Manual Review Protocol")
    md.append("")
    md.append("- Read all `core trend paper` rows first; these shape the thesis.")
    md.append("- Then read `important bridge paper` rows that connect VGGT, Gaussian maps, dynamic scenes, and pose/calibration.")
    md.append("- Use `specialized geometry paper` rows for subsection examples, not for the opening thesis unless they introduce a new evaluation axis.")
    md.append("- Treat `adjacent / inspect manually` rows as false-positive candidates until abstract-level evidence proves otherwise.")
    md.append("- For each selected paper, write one sentence for `what changed in the field` and one sentence for `what remains brittle or narrow`.")
    path = OUT_DIR / "cvpr2026_3d_recon_strategic_brief.md"
    path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return path


def write_html(rows, path, title):
    def esc(x):
        return html.escape(norm_text(x), quote=True)

    table_rows = []
    for idx, item in enumerate(rows, start=1):
        paper = item["paper"]
        result = item["result"]
        abstract = norm_text(paper.get("abstract"))[:900]
        table_rows.append(
            "<tr>"
            f"<td>{idx}</td>"
            f"<td>{result['score']}</td>"
            f"<td>{esc(result['role'])}<div class='meta'>{esc(result['editorial_bucket'])}</div></td>"
            f"<td><strong>{esc(paper.get('title'))}</strong><div class='meta'>{esc(paper.get('primary_phylum'))} / {esc(paper.get('primary_genus'))}</div></td>"
            f"<td>{esc('; '.join(result['matched_groups']))}</td>"
            f"<td>{esc('; '.join(result['inputs']))}</td>"
            f"<td>{esc('; '.join(result['outputs']))}</td>"
            f"<td>{esc('; '.join(result['claims']))}</td>"
            f"<td>{esc(result['strategic_note'])}<details><summary>abstract</summary>{esc(abstract)}</details></td>"
            "</tr>"
        )
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{esc(title)}</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; color: #151515; }}
h1 {{ font-size: 24px; }}
.summary {{ margin: 12px 0 20px; color: #444; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th, td {{ border-bottom: 1px solid #ddd; padding: 8px; vertical-align: top; }}
th {{ position: sticky; top: 0; background: #f3f5f7; text-align: left; }}
tr:nth-child(even) {{ background: #fafafa; }}
.meta {{ margin-top: 4px; color: #666; font-size: 12px; }}
details {{ margin-top: 6px; }}
summary {{ cursor: pointer; color: #235789; }}
</style>
</head>
<body>
<h1>{esc(title)}</h1>
<div class="summary">Source: <a href="{SOURCE_URL}">{SOURCE_URL}</a>. Rows are sorted by strategic score, then title.</div>
<table>
<thead><tr><th>#</th><th>Score</th><th>Role</th><th>Paper</th><th>Clusters</th><th>Input</th><th>Output</th><th>Claim</th><th>Strategic note</th></tr></thead>
<tbody>
{''.join(table_rows)}
</tbody>
</table>
</body>
</html>
"""
    path.write_text(doc, encoding="utf-8")
    return path


def main():
    payload = get_json_payload()
    papers = payload["papers"]
    broad_rows = []
    for paper in papers:
        result = analyze_paper(paper)
        result["editorial_bucket"] = editorial_bucket(result, paper)
        if should_include_broad(result, paper):
            broad_rows.append({"paper": paper, "result": result})
    broad_rows.sort(
        key=lambda r: (
            -r["result"]["score"],
            r["result"]["editorial_bucket"],
            norm_text(r["paper"].get("title")).lower(),
        )
    )
    strict_rows = [row for row in broad_rows if should_include_strict(row["result"], row["paper"])]
    strict_rows.sort(
        key=lambda r: (
            r["result"]["editorial_bucket"],
            -r["result"]["score"],
            norm_text(r["paper"].get("title")).lower(),
        )
    )
    broad_csv = write_csv(broad_rows, OUT_DIR / "cvpr2026_3d_recon_broad_candidates.csv")
    strict_csv = write_csv(strict_rows, OUT_DIR / "cvpr2026_3d_recon_strict_reading_list.csv")
    seed_rows = select_seed_rows(strict_rows)
    seed_csv = write_csv(seed_rows, OUT_DIR / "cvpr2026_3d_recon_blog_seed_list.csv")
    summary_csv, cluster_counter, role_counter, bucket_counter, cross_counter = write_summary_csv(strict_rows)
    brief = write_markdown(strict_rows, seed_rows, cluster_counter, role_counter, bucket_counter, cross_counter, len(papers), len(broad_rows))
    broad_audit = write_html(broad_rows, OUT_DIR / "cvpr2026_3d_recon_broad_audit.html", "CVPR 2026 3D Reconstruction Broad Audit")
    strict_audit = write_html(strict_rows, OUT_DIR / "cvpr2026_3d_recon_strict_audit.html", "CVPR 2026 3D Reconstruction Strict Reading List")
    seed_audit = write_html(seed_rows, OUT_DIR / "cvpr2026_3d_recon_blog_seed_audit.html", "CVPR 2026 3D Reconstruction Blog Seed List")
    print(json.dumps(
        {
            "source": SOURCE_URL,
            "total_papers": len(papers),
            "broad_candidate_papers": len(broad_rows),
            "strict_reading_papers": len(strict_rows),
            "blog_seed_papers": len(seed_rows),
            "broad_csv": str(broad_csv),
            "strict_csv": str(strict_csv),
            "seed_csv": str(seed_csv),
            "summary_csv": str(summary_csv),
            "brief": str(brief),
            "broad_audit_html": str(broad_audit),
            "strict_audit_html": str(strict_audit),
            "seed_audit_html": str(seed_audit),
            "top_clusters": cluster_counter.most_common(10),
            "buckets": bucket_counter.most_common(),
            "roles": role_counter.most_common(),
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
