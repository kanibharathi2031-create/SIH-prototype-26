from flask import Flask, render_template, request

app = Flask(__name__)

# =========================================================
# DEMO DATA
# =========================================================

SHIPMENTS = [
    {
        "id": "SR-102",
        "type": "Essential Medicines",
        "destination": "District Hospital A",
        "route": "NH-27",
        "delay": 6,
        "priority": "CRITICAL"
    },
    {
        "id": "SR-108",
        "type": "Food Supplies",
        "destination": "Relief Centre B",
        "route": "NH-27",
        "delay": 5,
        "priority": "HIGH"
    },
    {
        "id": "SR-114",
        "type": "Emergency Medicines",
        "destination": "Emergency Hospital C",
        "route": "NH-27",
        "delay": 7,
        "priority": "CRITICAL"
    },
    {
        "id": "SR-119",
        "type": "Essential Goods",
        "destination": "Relief Centre D",
        "route": "Route 12",
        "delay": 3,
        "priority": "MEDIUM"
    }
]

VEHICLES = [
    {
        "id": "VH-01",
        "driver": "Field Vehicle 01",
        "location": "NH-27 - Sector A",
        "route": "NH-27",
        "destination": "District Hospital A",
        "speed": 42,
        "eta": 3,
        "vehicle_status": "MOVING",
        "road_status": "CLEAR",
        "accessibility": "GOOD",
        "weather": "NORMAL",
        "last_updated": "2 min ago"
    },
    {
        "id": "VH-02",
        "driver": "Relief Vehicle 02",
        "location": "NH-27 - Sector B",
        "route": "NH-27",
        "destination": "Relief Centre B",
        "speed": 24,
        "eta": 5,
        "vehicle_status": "SLOW",
        "road_status": "FLOODED",
        "accessibility": "LIMITED",
        "weather": "HEAVY RAIN",
        "last_updated": "1 min ago"
    },
    {
        "id": "VH-03",
        "driver": "Emergency Vehicle 03",
        "location": "Route 12 - Sector C",
        "route": "Route 12",
        "destination": "Emergency Hospital C",
        "speed": 38,
        "eta": 4,
        "vehicle_status": "REROUTING",
        "road_status": "DAMAGED",
        "accessibility": "RESTRICTED",
        "weather": "CLOUDY",
        "last_updated": "3 min ago"
    }
]

LATEST_REPORT = {
    "report_type": "Flood",
    "location": "NH-27",
    "route": "NH-27",
    "description": "Heavy rain and flooding affecting road accessibility.",
    "risk_level": "HIGH",
    "risk_score": 87,
    "impact": "Vehicle movement slowed and shipment delays expected.",
    "risk_reason": "Flooding has reduced route accessibility.",
    "recommended_action": "REROUTE CRITICAL SHIPMENTS",
    "action_type": "REROUTE",
    "weather": "Heavy Rain",
    "photo_name": "Demo image",
    "time": "Demo"
}

ROAD_STATUS = {
    "route": "NH-27",
    "condition": "Flooded",
    "accessibility": "Limited",
    "impact": "Vehicle movement slowed",
    "risk_level": "HIGH",
    "recommended_action": "Monitor road and reroute critical vehicles",
    "last_updated": "2 min ago",
    "vehicle_impact": "Vehicle speed reduced",
    "description": "Flooding affecting vehicle movement."
}


# =========================================================
# DISRUPTION ANALYSIS
# =========================================================

def analyze_disruption(report_type):

    if report_type == "Flood":
        return {
            "risk_level": "HIGH",
            "risk_score": 87,
            "impact": "Vehicle movement slowed and shipment delays expected.",
            "risk_reason": "Flooding has reduced route accessibility.",
            "recommended_action": "REROUTE CRITICAL SHIPMENTS",
            "action_type": "REROUTE",
            "weather": "Heavy Rain"
        }

    if report_type == "Landslide":
        return {
            "risk_level": "CRITICAL",
            "risk_score": 95,
            "impact": "Road blockage detected. Vehicle movement may stop.",
            "risk_reason": "Landslide has blocked the affected route.",
            "recommended_action": "REROUTE + PRIORITIZE EMERGENCY SHIPMENTS",
            "action_type": "REROUTE + PRIORITIZE",
            "weather": "Heavy Rain"
        }

    if report_type == "Heavy Rain":
        return {
            "risk_level": "HIGH",
            "risk_score": 78,
            "impact": "Reduced accessibility and increased travel time.",
            "risk_reason": "Heavy rainfall may slow transportation.",
            "recommended_action": "MONITOR AND RESCHEDULE",
            "action_type": "RESCHEDULE",
            "weather": "Heavy Rain"
        }

    if report_type == "Road Damage":
        return {
            "risk_level": "MEDIUM",
            "risk_score": 61,
            "impact": "Road accessibility reduced.",
            "risk_reason": "Damaged road may reduce vehicle speed.",
            "recommended_action": "MONITOR / RESCHEDULE",
            "action_type": "RESCHEDULE",
            "weather": "Cloudy"
        }

    if report_type == "Road Block":
        return {
            "risk_level": "CRITICAL",
            "risk_score": 92,
            "impact": "Vehicle movement stopped on the affected route.",
            "risk_reason": "Road blockage prevents normal shipment movement.",
            "recommended_action": "REROUTE + ESCALATE",
            "action_type": "REROUTE + ESCALATE",
            "weather": "Unstable"
        }

    return {
        "risk_level": "LOW",
        "risk_score": 35,
        "impact": "No major disruption detected.",
        "risk_reason": "Current route condition appears normal.",
        "recommended_action": "MONITOR",
        "action_type": "MONITOR",
        "weather": "Normal"
    }


# =========================================================
# ROAD CONDITION ANALYSIS
# =========================================================

def analyze_road_condition(condition):

    condition = condition.strip().lower()

    if condition == "clear":
        return {
            "risk_level": "LOW",
            "impact": "Normal vehicle movement",
            "action": "CONTINUE ROUTE",
            "vehicle_impact": "No major impact"
        }

    if condition == "flooded":
        return {
            "risk_level": "HIGH",
            "impact": "Vehicle movement slowed",
            "action": "SLOW VEHICLE / ASSESS ALTERNATE ROUTE",
            "vehicle_impact": "Speed reduced and ETA increased"
        }

    if condition == "damaged":
        return {
            "risk_level": "MEDIUM",
            "impact": "Road accessibility reduced",
            "action": "MONITOR / RESCHEDULE",
            "vehicle_impact": "Vehicle speed reduced"
        }

    if condition == "blocked":
        return {
            "risk_level": "CRITICAL",
            "impact": "Vehicle movement stopped",
            "action": "REROUTE / ESCALATE",
            "vehicle_impact": "Vehicle cannot continue on current route"
        }

    if condition == "landslide":
        return {
            "risk_level": "CRITICAL",
            "impact": "Road blocked by landslide",
            "action": "REROUTE / PRIORITIZE",
            "vehicle_impact": "Vehicle requires alternate route"
        }

    return {
        "risk_level": "MEDIUM",
        "impact": "Route requires monitoring",
        "action": "MONITOR",
        "vehicle_impact": "Under assessment"
    }


# =========================================================
# VEHICLE REASSESSMENT
# =========================================================

def reassess_vehicles(route, condition):

    condition = condition.strip().lower()

    for vehicle in VEHICLES:

        if vehicle["route"].lower() != route.lower():
            continue

        if condition == "clear":
            vehicle["road_status"] = "CLEAR"
            vehicle["accessibility"] = "GOOD"
            vehicle["vehicle_status"] = "MOVING"
            vehicle["speed"] = 42
            vehicle["eta"] = 3
            vehicle["weather"] = "NORMAL"

        elif condition == "flooded":
            vehicle["road_status"] = "FLOODED"
            vehicle["accessibility"] = "LIMITED"
            vehicle["vehicle_status"] = "SLOW"
            vehicle["speed"] = 24
            vehicle["eta"] = 5
            vehicle["weather"] = "HEAVY RAIN"

        elif condition == "damaged":
            vehicle["road_status"] = "DAMAGED"
            vehicle["accessibility"] = "RESTRICTED"
            vehicle["vehicle_status"] = "SLOW"
            vehicle["speed"] = 18
            vehicle["eta"] = 6
            vehicle["weather"] = "CLOUDY"

        elif condition in ["blocked", "landslide"]:
            vehicle["road_status"] = "BLOCKED"
            vehicle["accessibility"] = "NOT ACCESSIBLE"
            vehicle["vehicle_status"] = "REROUTING"
            vehicle["speed"] = 0
            vehicle["eta"] = 8
            vehicle["weather"] = "UNSTABLE"

        else:
            vehicle["road_status"] = "UNDER REVIEW"
            vehicle["accessibility"] = "LIMITED"
            vehicle["vehicle_status"] = "MONITORING"
            vehicle["speed"] = 0
            vehicle["eta"] = 0
            vehicle["weather"] = "UNKNOWN"

        vehicle["last_updated"] = "Just now"


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/")
def dashboard():

    return render_template(
        "dashboard.html",
        report=LATEST_REPORT,
        vehicles=VEHICLES,
        road=ROAD_STATUS,
        shipments=SHIPMENTS
    )


# =========================================================
# UPLOAD PAGE
# =========================================================

@app.route("/upload")
def upload():

    return render_template("upload.html")


# =========================================================
# SUBMIT FIELD REPORT
# =========================================================

@app.route("/submit-report", methods=["POST"])
def submit_report():

    global LATEST_REPORT

    report_type = request.form.get("report_type", "Flood")
    location = request.form.get("location", "NH-27")
    description = request.form.get(
        "description",
        "Disruption reported by field operator."
    )

    photo = request.files.get("photo")

    photo_name = "No image uploaded"

    if photo and photo.filename:
        photo_name = photo.filename

    analysis = analyze_disruption(report_type)

    LATEST_REPORT = {
        "report_type": report_type,
        "location": location,
        "route": location,
        "description": description,
        "photo_name": photo_name,
        "risk_level": analysis["risk_level"],
        "risk_score": analysis["risk_score"],
        "impact": analysis["impact"],
        "risk_reason": analysis["risk_reason"],
        "recommended_action": analysis["recommended_action"],
        "action_type": analysis["action_type"],
        "weather": analysis["weather"],
        "time": "Just now"
    }

    return render_template(
        "risk.html",
        report_type=LATEST_REPORT["report_type"],
        location=LATEST_REPORT["location"],
        photo_name=LATEST_REPORT["photo_name"],
        description=LATEST_REPORT["description"],
        impact=LATEST_REPORT["impact"],
        risk_reason=LATEST_REPORT["risk_reason"],
        risk_level=LATEST_REPORT["risk_level"],
        risk_score=LATEST_REPORT["risk_score"],
        recommended_action=LATEST_REPORT["recommended_action"],
        action_type=LATEST_REPORT["action_type"],
        time=LATEST_REPORT["time"]
    )


# =========================================================
# RISK PAGE
# =========================================================

@app.route("/risk")
def risk():

    return render_template(
        "risk.html",
        report_type=LATEST_REPORT["report_type"],
        location=LATEST_REPORT["location"],
        photo_name=LATEST_REPORT["photo_name"],
        description=LATEST_REPORT["description"],
        impact=LATEST_REPORT["impact"],
        risk_reason=LATEST_REPORT["risk_reason"],
        risk_level=LATEST_REPORT["risk_level"],
        risk_score=LATEST_REPORT["risk_score"],
        recommended_action=LATEST_REPORT["recommended_action"],
        action_type=LATEST_REPORT["action_type"],
        time=LATEST_REPORT["time"]
    )


# =========================================================
# AFFECTED SHIPMENTS
# =========================================================

@app.route("/shipments")
def shipments():

    affected_shipments = [
        s for s in SHIPMENTS
        if s["route"] == LATEST_REPORT["route"]
    ]

    return render_template(
        "shipments.html",
        shipments=affected_shipments,
        report=LATEST_REPORT
    )


# =========================================================
# SHORTAGE RISK
# =========================================================

@app.route("/shortage")
def shortage():

    shortage_data = []

    current_stock = 24
    consumption_rate = 6

    hours_of_stock = current_stock / consumption_rate

    for shipment in SHIPMENTS:

        if shipment["route"] != LATEST_REPORT["route"]:
            continue

        revised_eta = shipment["delay"] + 2

        if revised_eta > hours_of_stock:
            shortage_status = "HIGH"
            shortage_message = (
                "Shortage risk detected before shipment arrival."
            )
        else:
            shortage_status = "LOW"
            shortage_message = (
                "Current stock is expected to cover the delay."
            )

        shortage_data.append({
            "id": shipment["id"],
            "destination": shipment["destination"],
            "type": shipment["type"],
            "priority": shipment["priority"],
            "current_stock": current_stock,
            "consumption_rate": consumption_rate,
            "hours_of_stock": round(hours_of_stock, 1),
            "revised_eta": revised_eta,
            "shortage_status": shortage_status,
            "shortage_message": shortage_message
        })

    return render_template(
        "shortage.html",
        shortage_data=shortage_data,
        report=LATEST_REPORT
    )


# =========================================================
# RECOMMENDED ACTION
# =========================================================

@app.route("/action")
def action():

    risk_level = LATEST_REPORT["risk_level"]

    if risk_level == "CRITICAL":
        actions = [
            "REROUTE affected critical shipments",
            "PRIORITIZE emergency medical supplies",
            "ESCALATE blocked route condition",
            "CONTINUOUSLY REASSESS affected vehicles"
        ]

    elif risk_level == "HIGH":
        actions = [
            "REROUTE critical shipments",
            "MONITOR affected vehicles",
            "REASSESS road accessibility",
            "PRIORITIZE essential supplies"
        ]

    elif risk_level == "MEDIUM":
        actions = [
            "MONITOR route condition",
            "RESCHEDULE affected shipments",
            "REASSESS vehicle movement"
        ]

    else:
        actions = [
            "CONTINUE normal route",
            "MONITOR for new disruptions"
        ]

    return render_template(
        "action.html",
        actions=actions,
        risk_level=LATEST_REPORT["risk_level"],
        recommended_action=LATEST_REPORT["recommended_action"],
        report=LATEST_REPORT
    )


# =========================================================
# TRACKING
# =========================================================

@app.route("/tracking")
def tracking():

    tracking_data = {
        "shipment_id": "SR-114",
        "shipment_type": "Emergency Medicines",
        "destination": "Emergency Hospital C",
        "original_route": "NH-27",
        "alternate_route": "Route 12",
        "status": "REROUTING",
        "original_eta": 12,
        "revised_eta": 4,
        "action": "Reroute + Prioritize"
    }

    return render_template(
        "tracking.html",
        tracking=tracking_data,
        report=LATEST_REPORT
    )


# =========================================================
# VEHICLE MONITORING
# =========================================================

@app.route("/vehicle")
def vehicle():

    return render_template(
        "vehicle.html",
        vehicles=VEHICLES,
        road=ROAD_STATUS,
        report=LATEST_REPORT,
        reassessment=False,
        reassessment_message=""
    )


# =========================================================
# REPORT ROAD ISSUE
# =========================================================

@app.route("/report-road-issue", methods=["POST"])
def report_road_issue():

    global ROAD_STATUS

    route = request.form.get("route", "NH-27")
    condition = request.form.get("condition", "Flooded")
    accessibility = request.form.get(
        "accessibility",
        "Limited"
    )

    description = request.form.get(
        "description",
        "Road condition reported by field operator."
    )

    road_analysis = analyze_road_condition(condition)

    ROAD_STATUS = {
        "route": route,
        "condition": condition,
        "accessibility": accessibility,
        "impact": road_analysis["impact"],
        "risk_level": road_analysis["risk_level"],
        "recommended_action": road_analysis["action"],
        "last_updated": "Just now",
        "vehicle_impact": road_analysis["vehicle_impact"],
        "description": description
    }

    reassess_vehicles(route, condition)

    return render_template(
        "vehicle.html",
        vehicles=VEHICLES,
        road=ROAD_STATUS,
        report=LATEST_REPORT,
        reassessment=True,
        reassessment_message=(
            "New road condition detected. "
            "Affected vehicles and route accessibility "
            "have been reassessed."
        )
    )


# =========================================================
# MANUAL REASSESSMENT
# =========================================================

@app.route("/reassess")
def manual_reassessment():

    reassess_vehicles(
        ROAD_STATUS["route"],
        ROAD_STATUS["condition"]
    )

    return render_template(
        "vehicle.html",
        vehicles=VEHICLES,
        road=ROAD_STATUS,
        report=LATEST_REPORT,
        reassessment=True,
        reassessment_message=(
            "Continuous reassessment completed. "
            "Vehicle and road conditions have been updated."
        )
    )


# =========================================================
# SECURITY
# =========================================================

@app.route("/security")
def security():

    return render_template("security.html")


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print(" SafeRoute Supply - SIH 2026 Prototype")
    print("----------------------------------------")
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("----------------------------------------")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )











