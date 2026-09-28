import sys
import json
import re

def a_or_an(word):
    if not word:
        return "a"
    return "an" if word.strip()[0].lower() in "aeiou" else "a"

def title_case(s):
    return re.sub(r"\b\w", lambda m: m.group(0).toUpperCase() if hasattr(m.group(0), 'toUpperCase') else m.group(0).upper(), s)

def lc(s):
    return str(s).lower().strip()

def capitalize(s):
    s = str(s).strip()
    if not s:
        return ""
    return s[0].upper() + s[1:]

def join_features(arr):
    a = [lc(f) for f in arr[:3] if f]
    if len(a) == 0:
        return "thoughtful design"
    if len(a) == 1:
        return a[0]
    if len(a) == 2:
        return f"{a[0]} and {a[1]}"
    return f"{a[0]}, {a[1]}, and {a[2]}"

def word_count(s):
    words = s.strip().split()
    return len(words)

def trim_to_words(s, target):
    words = s.strip().split()
    if len(words) <= target + 12:
        return s.strip()
    trimmed = " ".join(words[:target + 6])
    trimmed = re.sub(r"[,;:]$", "", trimmed)
    return trimmed + "."

def build_highlights(features, style):
    src = [f for f in features[:3] if f]
    if not src:
        src = ["Premium build quality", "Thoughtful design", "Built to last"]
    
    highlights = []
    for f in src:
        if style == "benefit":
            highlights.append(f"{capitalize(f)} that works for you")
        elif style == "story":
            highlights.append(f"Everyday {lc(f)}")
        else:
            highlights.append(capitalize(f))
    return highlights

def main():
    name = "Aurora Wireless Headphones"
    category = "Electronics"
    audience = "Remote workers"
    features = ["Active noise cancelling", "40h battery life", "Memory-foam earcups"]
    keywords = ["wireless headphones", "noise cancelling"]
    tone_name = "Professional"
    length_index = 1

    # Read CLI args
    if len(sys.argv) >= 8:
        name = sys.argv[1]
        category = sys.argv[2]
        audience = sys.argv[3]
        features = [f.strip() for f in sys.argv[4].split(",") if f.strip()]
        keywords = [k.strip() for k in sys.argv[5].split(",") if k.strip()]
        tone_name = sys.argv[6]
        try:
            length_index = int(sys.argv[7])
        except ValueError:
            length_index = 1

    # Length config
    lengths = [
        {"label": "Short", "words": "~35 words", "target": 35},
        {"label": "Medium", "words": "~60 words", "target": 60},
        {"label": "Long", "words": "~90 words", "target": 90}
    ]
    len_target = lengths[length_index]["target"]

    # Load templates and tones
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            db = json.load(f)
    except Exception:
        db = {}

    tones = db.get("tones", {})
    templates = db.get("templates", {})

    tone = tones.get(tone_name, tones.get("Professional", {
        "opener": "Engineered for performance,",
        "adj": ["reliable", "precise", "refined"],
        "closer": "Built for those who expect more."
    }))

    adj = tone["adj"]
    opener = tone["opener"]
    closer = tone["closer"]

    feat_str = join_features(features)
    f0 = lc(features[0]) if len(features) > 0 else "quality"
    f1 = lc(features[1]) if len(features) > 1 else f0
    f2 = lc(features[2]) if len(features) > 2 else f1

    # Form benefit-led description
    benefit_template = templates.get("benefit", "")
    benefit = benefit_template.format(
        opener=opener,
        name=name,
        f0=f0,
        audience=audience,
        f1=f1,
        f2=f2,
        a_or_an_adj0=a_or_an(adj[0]),
        adj0=adj[0],
        adj1=adj[1],
        closer=closer
    )

    # Form story-driven description
    story_template = templates.get("story", "")
    story = story_template.format(
        name=name,
        f0=f0,
        f1=f1,
        f2=f2,
        audience=audience,
        adj2=adj[2],
        closer=closer
    )

    # Form feature-focused description
    feature_template = templates.get("feature", "")
    feature = feature_template.format(
        name=name,
        audience=audience,
        category=category,
        featStr=feat_str,
        adj0=adj[0],
        adj1=adj[1]
    )

    variations_raw = [
        {"id": "Benefit-led", "body": benefit, "style": "benefit"},
        {"id": "Story-driven", "body": story, "style": "story"},
        {"id": "Feature-focused", "body": feature, "style": "feature"}
    ]

    variations = []
    for v in variations_raw:
        body_trimmed = trim_to_words(v["body"], len_target)
        
        # SEO Title
        kw_title = f" — {', '.join([k.title() for k in keywords[:2]])}" if keywords else f" — {v['id']}"
        seo_title = f"{name}{kw_title}"
        
        # SEO Meta
        kw_hint = f" Featuring {', '.join([k.lower() for k in keywords[:2]])}." if keywords else ""
        seo_meta = f"Discover the {name} with {feat_str} — designed for {audience}.{kw_hint}"
        if len(seo_meta) > 160:
            seo_meta = seo_meta[:157].rstrip(",;: ") + "..."

        variations.append({
            "id": v["id"],
            "body": body_trimmed,
            "wordCount": word_count(body_trimmed),
            "highlights": build_highlights(features, v["style"]),
            "seoTitle": seo_title,
            "seoMeta": seo_meta
        })

    result = {
        "success": True,
        "variations": variations
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()
