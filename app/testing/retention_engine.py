import json

# CLUSTER NAMES
CLUSTER_NAMES = {

    0: "Dormant Customers",

    1: "Premium Frequent Flyers",

    2: "Rising High-Value Customers",

    3: "Value Seekers",

    4: "Regular Travelers"

}

SEGMENT_DESCRIPTIONS = {

    0:
    "Inactive customers with extremely low engagement, long inactivity periods, and high reactivation potential.",

    1:
    "Premium frequent flyers with the highest lifetime value and strong historical loyalty.",

    2:
    "Rapidly growing high-value customers with the highest flight frequency and points accumulation.",

    3:
    "Average-value customers with moderate travel activity and limited loyalty engagement.",

    4:
    "Regular travelers with stable activity patterns but lower loyalty program participation."

}

# VALUE SCORE
def calculate_value_score(

    clv,
    future_flights,
    future_distance,
    future_points

):

    print("\n[DEBUG] Calculating Value Score")

    clv_score = min(
        clv / 15000,
        1.0
    )

    flights_score = min(
        future_flights / 50,
        1.0
    )

    distance_score = min(
        future_distance / 80000,
        1.0
    )

    points_score = min(
        future_points / 120000,
        1.0
    )

    print(
        f"CLV Score      : {clv_score:.3f}"
    )

    print(
        f"Flights Score  : {flights_score:.3f}"
    )

    print(
        f"Distance Score : {distance_score:.3f}"
    )

    print(
        f"Points Score   : {points_score:.3f}"
    )

    value_score = (

        0.40 * clv_score +

        0.10 * flights_score +

        0.25 * distance_score +

        0.25 * points_score

    )

    value_score *= 100

    print(
        f"Value Score: {value_score:.2f}"
    )

    return round(
        value_score,
        2
    )

# CUSTOMER VALUE
def get_customer_value(

    value_score

):

    if value_score >= 80:

        return "VERY HIGH"

    elif value_score >= 60:

        return "HIGH"

    elif value_score >= 40:

        return "MEDIUM"

    else:

        return "LOW"

# PRIORITY
def calculate_priority(

    churn_probability,
    value_score

):

    print("\n[DEBUG] Calculating Priority")

    print(
        f"Churn: {churn_probability:.4f}"
    )

    print(
        f"Value Score: {value_score}"
    )

    if (

        churn_probability >= 0.80

        and

        value_score >= 80

    ):

        return "CRITICAL"

    elif (

        churn_probability >= 0.60

        and

        value_score >= 60

    ):

        return "HIGH"

    elif churn_probability >= 0.40:

        return "MEDIUM"

    else:

        return "LOW"

# ESTIMATED LOSS
def estimate_loss(

    churn_probability,
    clv

):

    loss = churn_probability * clv

    print(
        f"\n[DEBUG] Estimated Loss: {loss:.2f}"
    )

    return round(
        loss,
        2
    )

# ACTIONS
def recommend_actions(

    cluster,

    churn_probability,

    priority,

    value_score

):

    print(
        f"\n[DEBUG] Cluster {cluster}"
    )

    print(
        f"[DEBUG] Priority {priority}"
    )

    actions = []

    # ==========================
    # LOW RISK
    # ==========================

    if priority == "LOW":

        return [

            "No Immediate Action",

            "Monitor Customer",

            "Standard Marketing Campaign"

        ]

    # ==========================
    # MEDIUM RISK
    # ==========================

    if priority == "MEDIUM":

        return [

            "Personalized Email",

            "Small Bonus Points Offer",

            "Targeted Promotion"

        ]

    # ==========================
    # HIGH RISK
    # ==========================

    if priority == "HIGH":

        if cluster in [1, 2]:

            return [

                "Offer 10000 Bonus Points",

                "Priority Customer Outreach",

                "Loyalty Tier Review"

            ]

        return [

            "Retention Discount",

            "Reward Promotion",

            "Personalized Offer"

        ]

    # ==========================
    # CRITICAL
    # ==========================

    if priority == "CRITICAL":

        if cluster == 1:

            return [

                "Offer 15000 Bonus Points",

                "Provide Complimentary Lounge Access",

                "Assign Personal Account Manager"

            ]

        elif cluster == 2:

            return [

                "Fast Track Tier Upgrade",

                "Offer 10000 Bonus Points",

                "Executive Retention Outreach"

            ]

        elif cluster == 4:

            return [

                "Large Loyalty Bonus",

                "Exclusive Travel Offer",

                "Personalized Retention Campaign"

            ]

        else:

            return [

                "Aggressive Win-back Campaign",

                "Special Discount Offer",

                "Dedicated Customer Outreach"

            ]

    return [

        "Monitor Customer"
    ]

# MAIN PROFILE
def generate_retention_profile(

    cluster,

    churn_probability,

    future_flights,

    future_distance,

    future_points,

    clv,

    salary,

    loyalty_card

):

    print("\n" + "=" * 60)
    print("RETENTION ENGINE")
    print("=" * 60)

    cluster_name = CLUSTER_NAMES.get(
        cluster,
        "Unknown"
    )

    segment_description = SEGMENT_DESCRIPTIONS.get(
        cluster,
        "Unknown Segment"
    )

    value_score = calculate_value_score(

        clv,

        future_flights,

        future_distance,

        future_points

    )

    customer_value = get_customer_value(

        value_score

    )

    priority = calculate_priority(

        churn_probability,

        value_score

    )

    estimated_loss = estimate_loss(

        churn_probability,

        clv

    )

    actions = recommend_actions(
        
        cluster,
        
        churn_probability,
        
        priority,
        
        value_score
        
    )
    
    confidence = round(
        abs(
            churn_probability - 0.5
        ) * 200,
        2
    )
    
    profile = {

        "cluster": cluster,

        "cluster_name": cluster_name,

        "churn_probability": round(
            churn_probability,
            4
        ),

        "future_flights": round(
            future_flights,
            2
        ),

        "future_distance": round(
            future_distance,
            2
        ),

        "future_points": round(
            future_points,
            2
        ),

        "clv": round(
            clv,
            2
        ),

        "salary": round(
            salary,
            2
        ),

        "loyalty_card": loyalty_card,

        "customer_value":
        customer_value,

        "value_score":
        value_score,

        "priority":
        priority,

        "estimated_loss":
        estimated_loss,

        "recommended_actions":
        actions,
        
        "profile_segment_description":
        segment_description,
        
        "confidence":
        confidence

    }

    print("\nPROFILE GENERATED")

    print(
        json.dumps(
            profile,
            indent=4
        )
    )

    return profile
"""
# TEST
if __name__ == "__main__":

    profile = generate_retention_profile(

        cluster=2,

        churn_probability=0.87,

        future_flights=22,

        future_distance=41000,

        future_points=45000,

        clv=18000,

        salary=95000,

        loyalty_card="Star"

    )
"""