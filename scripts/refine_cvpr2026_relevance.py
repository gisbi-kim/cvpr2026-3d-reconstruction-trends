import csv
import html
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "output"
STRICT_CSV = OUT_DIR / "cvpr2026_3d_recon_strict_reading_list.csv"


CORE_GENUS = {"3D Reconstruction", "3D Gaussian Splatting"}
POSE_BRIDGE_GENUS = {"Pose Estimation"}
ADJACENT_GENUS = {
    "Video Generation",
    "Image Editing",
    "VLM / MLLM",
    "Grounding",
    "Detection",
    "Segmentation",
    "Efficient Models",
    "Self-supervised",
    "Benchmark",
    "Human Motion",
    "Medical Imaging",
    "Computational Imaging",
    "Diffusion",
    "Retrieval",
    "IQA",
    "Classification",
}


CORE_PATTERNS = [
    r"\b3d reconstruction\b",
    r"\bscene reconstruction\b",
    r"\bsurface reconstruction\b",
    r"\b4d reconstruction\b",
    r"\breconstruct(?:ion|ing)?\b",
    r"\bcompletion\b",
    r"\bfeed[- ]forward .*3d\b",
    r"\bpoint map",
    r"\bvisual geometry\b",
    r"\bVGGT\b",
    r"\bDUSt3R\b",
    r"\bMASt3R\b",
    r"\bSfM[- ]free\b",
    r"\bMVS\b",
    r"\bstructure from motion\b",
    r"\bneural surface\b",
    r"\bGaussian Splatting\b",
    r"\b3DGS\b",
]

DIRECT_TITLE_CORE_PATTERNS = [
    r"\breconstruct(?:ion|ing)?\b",
    r"\bcompletion\b",
    r"\bGaussian Splatting\b",
    r"\b3DGS\b",
    r"\bpoint map",
    r"\bvisual geometry\b",
    r"\bVGGT\b",
    r"\bSfM[- ]free\b",
    r"\bpose[- ]free\b",
    r"\bunposed\b",
    r"\bSLAM\b",
    r"\bmapping\b",
    r"\boccupancy\b",
]

BRIDGE_PATTERNS = [
    r"\bSLAM\b",
    r"\bmapping\b",
    r"\blocalization\b",
    r"\brelocalization\b",
    r"\bcalibration\b",
    r"\bcamera pose\b",
    r"\bpose[- ]free\b",
    r"\bunposed\b",
    r"\bmetric[- ]scale\b",
    r"\bmetric\b",
    r"\bbackend\b",
    r"\buncertainty\b",
    r"\bworld model\b",
    r"\bspatial memory\b",
    r"\boccupancy\b",
    r"\bautonomous driving\b",
    r"\bembodied\b",
    r"\bactive mapping\b",
]

NOISE_PATTERNS = [
    r"\bsign language\b",
    r"\baudio[- ]video\b",
    r"\bwatermark\b",
    r"\bcompression\b",
    r"\bimage quality\b",
    r"\bclassification\b",
]


def has_any(text, patterns):
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def count_hits(text, patterns):
    return sum(1 for pattern in patterns if re.search(pattern, text, re.I))


def classify(row):
    title = row.get("title", "")
    abstract = row.get("abstract", "")
    genus = row.get("primary_genus", "")
    phylum = row.get("primary_phylum", "")
    groups = row.get("matched_groups", "")
    bucket = row.get("editorial_bucket", "")
    text = f"{title} {abstract}"

    core_hits = count_hits(text, CORE_PATTERNS)
    bridge_hits = count_hits(text, BRIDGE_PATTERNS)
    noise_hits = count_hits(text, NOISE_PATTERNS)

    title_core = has_any(title, DIRECT_TITLE_CORE_PATTERNS)
    title_bridge = has_any(title, BRIDGE_PATTERNS)
    is_core_genus = genus in CORE_GENUS
    is_pose_bridge = genus in POSE_BRIDGE_GENUS
    is_3d_phylum = phylum == "3D Vision & Geometry"
    is_adjacent_genus = genus in ADJACENT_GENUS

    reasons = []

    # Guard against weak abstract-only matches: many generation, editing,
    # segmentation, detection, and efficient-model papers mention VGGT/3D in
    # the abstract but are not themselves reconstruction-method papers.
    if is_adjacent_genus and not title_core and not title_bridge:
        reasons.append(f"adjacent genus={genus} with no direct reconstruction/SLAM/map signal in title")
        return "adjacent_context", "low", "; ".join(reasons)

    if is_core_genus and (title_core or core_hits >= 2):
        reasons.append(f"core genus={genus} with direct reconstruction/geometry signal")
        return "core_reconstruction", "high", "; ".join(reasons)

    if "vggt_lineage" in groups and title_core and not is_adjacent_genus:
        reasons.append("VGGT/feed-forward geometry lineage with direct geometry signal")
        return "core_reconstruction", "high", "; ".join(reasons)

    if title_core and core_hits >= 2 and (is_3d_phylum or "gaussian_radiance" in groups or "dynamic_4d" in groups):
        reasons.append("3D Vision & Geometry paper with direct reconstruction title and abstract signal")
        return "core_reconstruction", "medium", "; ".join(reasons)

    if title_core and ("gaussian_radiance" in groups or "dynamic_4d" in groups) and core_hits >= 1:
        reasons.append("direct reconstruction/3DGS/4D title linked to core representation cluster")
        return "core_reconstruction", "medium", "; ".join(reasons)

    if is_pose_bridge and (title_bridge or bridge_hits >= 2) and (
        "general_reconstruction" in groups
        or "gaussian_radiance" in groups
        or "surface_occupancy" in groups
        or core_hits >= 1
    ):
        reasons.append(f"pose/localization bridge genus={genus} with reconstruction/map signal")
        return "strong_bridge", "high", "; ".join(reasons)

    if bridge_hits >= 2 and (
        core_hits >= 1
        or "gaussian_radiance" in groups
        or "robotics_mapping" in groups
        or "surface_occupancy" in groups
    ):
        reasons.append("system bridge signal: pose/localization/mapping/world-model plus reconstruction representation")
        return "strong_bridge", "medium", "; ".join(reasons)

    if "dynamic_4d" in groups and core_hits >= 1 and (is_3d_phylum or title_core):
        reasons.append("dynamic/4D paper with direct reconstruction signal")
        return "strong_bridge", "medium", "; ".join(reasons)

    if "gaussian_radiance" in groups and bridge_hits >= 1 and core_hits >= 1:
        reasons.append("Gaussian/radiance representation linked to pose/mapping/metric bridge")
        return "strong_bridge", "medium", "; ".join(reasons)

    if is_core_genus and core_hits >= 1:
        reasons.append(f"core genus={genus}, but title/abstract signal is narrower")
        return "core_reconstruction", "medium", "; ".join(reasons)

    if is_adjacent_genus:
        reasons.append(f"adjacent genus={genus}; useful only if manually connected to reconstruction")
        return "adjacent_context", "low", "; ".join(reasons)

    if bucket.startswith("A.") or bucket.startswith("B."):
        reasons.append("editorial thesis/bridge bucket but weaker direct reconstruction signal")
        return "adjacent_context", "medium", "; ".join(reasons)

    if noise_hits and not core_hits:
        reasons.append("keyword noise pattern without direct reconstruction signal")
        return "likely_noise", "low", "; ".join(reasons)

    if is_3d_phylum and (core_hits >= 1 or bridge_hits >= 1):
        reasons.append("3D Vision & Geometry with weak but relevant signal")
        return "adjacent_context", "low", "; ".join(reasons)

    reasons.append("weak or indirect keyword match")
    return "likely_noise", "low", "; ".join(reasons)


def write_csv(rows, path):
    original_keys = [
        key
        for key in rows[0].keys()
        if key not in {"relevance_tier", "relevance_confidence", "relevance_reason"}
    ]
    fieldnames = [
        "relevance_tier",
        "relevance_confidence",
        "relevance_reason",
        *original_keys,
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_html(rows, summary, path):
    def esc(value):
        return html.escape(str(value or ""), quote=True)

    table = []
    for i, row in enumerate(rows, 1):
        table.append(
            "<tr>"
            f"<td>{i}</td>"
            f"<td><strong>{esc(row['relevance_tier'])}</strong><div class='meta'>{esc(row['relevance_confidence'])}</div></td>"
            f"<td><strong>{esc(row['title'])}</strong><div class='meta'>{esc(row['primary_phylum'])} / {esc(row['primary_genus'])}</div></td>"
            f"<td>{esc(row['editorial_bucket'])}</td>"
            f"<td>{esc(row['matched_groups'])}</td>"
            f"<td>{esc(row['relevance_reason'])}</td>"
            f"<td><details><summary>abstract</summary>{esc(row['abstract'][:900])}</details></td>"
            "</tr>"
        )

    rows_html = "\n".join(
        f"<tr><td>{esc(k)}</td><td>{v}</td></tr>" for k, v in summary.items()
    )
    doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>CVPR 2026 3D Reconstruction Curated Relevance Audit</title>
<style>
body {{ font-family: Arial, "Noto Sans KR", sans-serif; margin: 24px; color: #171717; }}
h1 {{ font-size: 24px; }}
.note {{ border: 1px solid #d9dee7; background: #f6f8fb; border-radius: 8px; padding: 12px; margin: 12px 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin: 14px 0 24px; }}
th, td {{ border-bottom: 1px solid #d9dee7; padding: 8px; text-align: left; vertical-align: top; }}
th {{ position: sticky; top: 0; background: #f2f5f9; }}
.meta {{ color: #666; font-size: 12px; margin-top: 4px; }}
tr:nth-child(even) {{ background: #fafafa; }}
summary {{ color: #235789; cursor: pointer; }}
</style>
</head>
<body>
<h1>CVPR 2026 3D Reconstruction Curated Relevance Audit</h1>
<div class="note">
This is a relevance-curated pass over the earlier 864 strict candidates. It is not a quality ranking. The goal is to separate core reconstruction papers from strong system bridges, adjacent context, and likely keyword noise.
</div>
<h2>Summary</h2>
<table><tbody>{rows_html}</tbody></table>
<h2>Rows</h2>
<table>
<thead><tr><th>#</th><th>Relevance</th><th>Paper</th><th>Editorial bucket</th><th>Matched groups</th><th>Reason</th><th>Abstract</th></tr></thead>
<tbody>{''.join(table)}</tbody>
</table>
</body>
</html>
"""
    path.write_text(doc, encoding="utf-8")


def main():
    with STRICT_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            tier, confidence, reason = classify(row)
            row["relevance_tier"] = tier
            row["relevance_confidence"] = confidence
            row["relevance_reason"] = reason
            rows.append(row)

    tier_order = {
        "core_reconstruction": 0,
        "strong_bridge": 1,
        "adjacent_context": 2,
        "likely_noise": 3,
    }
    rows.sort(
        key=lambda r: (
            tier_order[r["relevance_tier"]],
            r["editorial_bucket"],
            -int(float(r["score"])),
            r["title"].lower(),
        )
    )

    summary = Counter(row["relevance_tier"] for row in rows)
    summary.update({f"{k}_high_conf": 0 for k in ["core_reconstruction", "strong_bridge", "adjacent_context", "likely_noise"]})
    for row in rows:
        if row["relevance_confidence"] == "high":
            summary[f"{row['relevance_tier']}_high_conf"] += 1

    write_csv(rows, OUT_DIR / "cvpr2026_3d_recon_curated_relevance.csv")
    write_html(rows, summary, OUT_DIR / "cvpr2026_3d_recon_curated_relevance_audit.html")

    print("Relevance summary")
    for key, value in summary.most_common():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
