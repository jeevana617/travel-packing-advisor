from flask import Flask, jsonify, render_template, request
from math import inf

app = Flask(__name__)


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_items(items):
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "Item")).strip() or "Item"
        weight = max(0.0, safe_float(item.get("weight"), 0.0))
        volume = max(0.0, safe_float(item.get("volume"), 0.0))
        importance = max(0.0, safe_float(item.get("importance"), 0.0))
        if weight <= 0 or volume <= 0 or importance <= 0:
            continue
        normalized.append({"name": name, "weight": weight, "volume": volume, "importance": importance})
    return normalized


def knapsack_single(items, capacity):
    if capacity <= 0 or not items:
        return {"selected": [], "importance": 0.0, "weight": 0.0, "volume": 0.0}

    n = len(items)
    dp = [[0.0 for _ in range(int(capacity) + 1)] for _ in range(n + 1)]
    keep = [[False for _ in range(int(capacity) + 1)] for _ in range(n + 1)]

    max_weight = capacity
    for i in range(1, n + 1):
        item = items[i - 1]
        w = int(item["weight"] * 10)
        for c in range(max_weight * 10 + 1):
            current = c / 10.0
            if item["weight"] <= current:
                candidate = dp[i - 1][int(current * 10) - w] + item["importance"]
                if candidate > dp[i][int(current * 10)]:
                    dp[i][int(current * 10)] = candidate
                    keep[i][int(current * 10)] = True
            dp[i][int(current * 10)] = max(dp[i][int(current * 10)], dp[i - 1][int(current * 10)])

    best_weight = 0
    best_imp = 0.0
    for w in range(int(capacity * 10) + 1):
        if dp[n][w] > best_imp:
            best_imp = dp[n][w]
            best_weight = w / 10.0

    selected = []
    remaining = int(best_weight * 10)
    for i in range(n, 0, -1):
        if keep[i][remaining]:
            selected.append(i - 1)
            item = items[i - 1]
            remaining -= int(item["weight"] * 10)

    selected.reverse()
    chosen = [items[idx] for idx in selected]
    total_weight = sum(item["weight"] for item in chosen)
    total_volume = sum(item["volume"] for item in chosen)

    return {
        "selected": selected,
        "selected_items": chosen,
        "importance": round(best_imp, 2),
        "weight": round(total_weight, 2),
        "volume": round(total_volume, 2),
    }


def knapsack_multi(items, weight_capacity, volume_capacity):
    items = normalize_items(items)
    if not items or weight_capacity <= 0 or volume_capacity <= 0:
        return {"selected": [], "selected_items": [], "importance": 0.0, "weight": 0.0, "volume": 0.0}

    max_w = max(1, int(weight_capacity * 10))
    max_v = max(1, int(volume_capacity * 10))
    n = len(items)
    dp = [[[0.0 for _ in range(max_v + 1)] for _ in range(max_w + 1)] for _ in range(n + 1)]
    take = [[[False for _ in range(max_v + 1)] for _ in range(max_w + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        item_w = int(item["weight"] * 10)
        item_v = int(item["volume"] * 10)
        for w in range(max_w + 1):
            for v in range(max_v + 1):
                dp[i][w][v] = dp[i - 1][w][v]
                take[i][w][v] = False
                if w >= item_w and v >= item_v:
                    candidate = dp[i - 1][w - item_w][v - item_v] + item["importance"]
                    if candidate > dp[i][w][v]:
                        dp[i][w][v] = candidate
                        take[i][w][v] = True

    best_w = max_w
    best_v = max_v
    best_value = dp[n][best_w][best_v]
    selected_indices = []

    w = max_w
    v = max_v
    for i in range(n, 0, -1):
        if take[i][w][v]:
            selected_indices.append(i - 1)
            item = items[i - 1]
            w -= int(item["weight"] * 10)
            v -= int(item["volume"] * 10)

    selected_indices.reverse()
    selected_items = [items[idx] for idx in selected_indices]
    total_weight = sum(item["weight"] for item in selected_items)
    total_volume = sum(item["volume"] for item in selected_items)

    return {
        "selected": selected_indices,
        "selected_items": selected_items,
        "importance": round(best_value, 2),
        "weight": round(total_weight, 2),
        "volume": round(total_volume, 2),
    }


def greedy_multi(items, weight_capacity, volume_capacity):
    normalized = normalize_items(items)
    if not normalized:
        return {"selected": [], "selected_items": [], "importance": 0.0, "weight": 0.0, "volume": 0.0}

    def score(item):
        efficiency = item["importance"] / (item["weight"] + (item["volume"] * 0.9))
        return efficiency

    ranked = sorted(normalized, key=score, reverse=True)
    selected = []
    current_w = 0.0
    current_v = 0.0

    for item in ranked:
        if current_w + item["weight"] <= weight_capacity and current_v + item["volume"] <= volume_capacity:
            selected.append(item)
            current_w += item["weight"]
            current_v += item["volume"]

    return {
        "selected": [item["name"] for item in selected],
        "selected_items": selected,
        "importance": round(sum(item["importance"] for item in selected), 2),
        "weight": round(current_w, 2),
        "volume": round(current_v, 2),
    }


def sensitivity_analysis(items, weight_capacity, volume_capacity):
    normalized = normalize_items(items)
    if not normalized:
        return []

    results = []
    weight_range = max(1, int(weight_capacity))
    volume_range = max(1, int(volume_capacity))
    w_steps = [max(5, round(weight_range * 0.6)), max(5, round(weight_range * 0.8)), weight_range, max(5, round(weight_range * 1.2))]
    v_steps = [max(5, round(volume_range * 0.6)), max(5, round(volume_range * 0.8)), volume_range, max(5, round(volume_range * 1.2))]

    unique = []
    seen = set()
    for w in sorted(set(w_steps)):
        for v in sorted(set(v_steps)):
            key = (w, v)
            if key in seen:
                continue
            seen.add(key)
            outcome = knapsack_multi(normalized, w, v)
            unique.append({
                "weight_capacity": w,
                "volume_capacity": v,
                "importance": outcome["importance"],
                "selected": [item["name"] for item in outcome["selected_items"]],
            })

    return unique


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/pack", methods=["POST"])
def solve_pack():
    data = request.get_json(silent=True) or {}
    items = normalize_items(data.get("items", []))
    weight_capacity = max(0.0, safe_float(data.get("weightCapacity"), 0.0))
    volume_capacity = max(0.0, safe_float(data.get("volumeCapacity"), 0.0))

    if not items:
        return jsonify({"error": "At least one valid item is required."}), 400

    if weight_capacity <= 0 or volume_capacity <= 0:
        return jsonify({"error": "Weight and volume limits must be greater than zero."}), 400

    optimal = knapsack_multi(items, weight_capacity, volume_capacity)
    greedy = greedy_multi(items, weight_capacity, volume_capacity)
    analysis = sensitivity_analysis(items, weight_capacity, volume_capacity)

    return jsonify({
        "optimal": {
            "selected": optimal["selected_items"],
            "importance": optimal["importance"],
            "weight": optimal["weight"],
            "volume": optimal["volume"],
            "weight_utilization": round((optimal["weight"] / weight_capacity) * 100, 2) if weight_capacity else 0,
            "volume_utilization": round((optimal["volume"] / volume_capacity) * 100, 2) if volume_capacity else 0,
        },
        "greedy": {
            "selected": greedy["selected_items"],
            "importance": greedy["importance"],
            "weight": greedy["weight"],
            "volume": greedy["volume"],
            "weight_utilization": round((greedy["weight"] / weight_capacity) * 100, 2) if weight_capacity else 0,
            "volume_utilization": round((greedy["volume"] / volume_capacity) * 100, 2) if volume_capacity else 0,
        },
        "analysis": analysis,
        "comparison": {
            "importance_gap": round(optimal["importance"] - greedy["importance"], 2),
            "relative_gain": round(((optimal["importance"] - greedy["importance"]) / greedy["importance"]) * 100, 2) if greedy["importance"] else 0,
            "dp_better": optimal["importance"] >= greedy["importance"],
        },
        "summary": {
            "total_items": len(items),
            "weight_capacity": weight_capacity,
            "volume_capacity": volume_capacity,
        },
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)






















































































































































































































































































































































































































































































































































































































