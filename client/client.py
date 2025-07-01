import httpx
import time
import random

API_BASE = "http://localhost:8000"

def get_product_info():
    try:
        response = httpx.get(f"{API_BASE}/product-info", timeout=3)
        return response.json()
    except Exception as e:
        return {"error": "Product info not available", "details": str(e)}

def get_reviews():
    try:
        response = httpx.get(f"{API_BASE}/reviews", timeout=3)
        return response.json()
    except:
        # Fallback to static cached reviews
        return {
            "fallback": True,
            "reviews": ["Cached Review 1", "Cached Review 2"]
        }

def get_recommendations():
    try:
        response = httpx.get(f"{API_BASE}/recommendations", timeout=3)
        return response.json()
    except:
        return {
            "disabled": True,
            "message": "Recommendations temporarily disabled due to high load"
        }

def simulate_load_shedding():
    try:
        load_response = httpx.get(f"{API_BASE}/system-load")
        load = load_response.json()["cpu_load_percent"]
        print(f"\n[System Load: {load}%]")

        if load > 80:
            print("[HIGH LOAD] High load! Serving Tier 1 only.\n")
            print("Product Info:", get_product_info())
        elif load > 60:
            print("[MEDIUM LOAD] Medium load. Serving Tier 1 and Tier 2.\n")
            print("Product Info:", get_product_info())
            print("Reviews:", get_reviews())
        else:
            print("[LOW LOAD] Low load. Serving all tiers.\n")
            print("Product Info:", get_product_info())
            print("Reviews:", get_reviews())
            print("Recommendations:", get_recommendations())

    except Exception as e:
        print("Error checking system load:", e)

if __name__ == "__main__":
    for _ in range(5):
        simulate_load_shedding()
        time.sleep(2)