from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define your checklist questions
questions = [
    "Do you use secure access control for diagnostic tools?",
    "Are all software updates signed and verified?",
    "Is USB or external media access restricted in service bays?",
    "Are default passwords changed on all automotive devices?",
    "Is client vehicle data encrypted when stored or transmitted?",
    "Are vehicle telematics interfaces audited for vulnerabilities?",
    "Do technicians receive cybersecurity awareness training?",
    "Is there a procedure for reporting and handling cyber incidents?",
    "Are firmware updates done through secure OTA processes?",
    "Are aftermarket IoT devices assessed before installation?"
]

# Explanations for failed answers
explanations = {
    questions[0]: {
        "explanation": "Unauthorized access to diagnostic ports can let attackers reprogram ECUs or disable safety features.",
        "exploitation": "An attacker could plug into the OBD-II port and alter vehicle behavior.",
        "client_impact": "Risk to driver safety, liability issues, and possible regulatory noncompliance.",
        "compliance": "NHTSA Cybersecurity Best Practices – Access control.",
        "help": "I can help implement authentication and logging controls for diagnostics."
    },
    questions[1]: {
        "explanation": "Unsigned updates can be tampered with to introduce malware into ECUs or infotainment systems.",
        "exploitation": "A malicious update could compromise braking or acceleration modules.",
        "client_impact": "Severe safety risk, potential recalls, and reputational harm.",
        "compliance": "ISO/SAE 21434 – Secure update procedures.",
        "help": "I can help implement signed firmware and update validation checks."
    },
    questions[2]: {
        "explanation": "Uncontrolled USB use can allow malware to enter service systems or connect to vehicle networks.",
        "exploitation": "A technician could unintentionally install malware that spreads via CAN or Ethernet interfaces.",
        "client_impact": "Operational disruption, privacy violations, or vehicle control issues.",
        "compliance": "Automotive Cyber Best Practices – Removable media controls.",
        "help": "I can help create device policies and implement endpoint protection for service bays."
    },
    questions[3]: {
        "explanation": "Default credentials are commonly published online and easily abused.",
        "exploitation": "Attackers can access networked diagnostic tools, cameras, or routers still using defaults.",
        "client_impact": "Unauthorized system access and data leaks.",
        "compliance": "NIST 800-82 – Industrial system hardening guidance.",
        "help": "I can help audit credentials and enforce password change policies."
    },
    questions[4]: {
        "explanation": "Sensitive data like VINs, locations, and diagnostic reports need protection from eavesdropping or theft.",
        "exploitation": "Unencrypted databases or wireless transmission could be intercepted.",
        "client_impact": "Loss of trust, potential lawsuits, and vendor risk.",
        "compliance": "Data Privacy Best Practices.",
        "help": "I can help implement AES encryption and TLS-based transmission protocols."
    },
    questions[5]: {
        "explanation": "Telematics systems connect vehicles to external servers and can expose major attack surfaces.",
        "exploitation": "An attacker could compromise GPS or remote unlock features.",
        "client_impact": "Tracking, unauthorized control, or customer privacy breaches.",
        "compliance": "ISO/SAE 21434 – Risk analysis for interfaces.",
        "help": "I can assist with penetration testing and hardening of telematics paths."
    },
    questions[6]: {
        "explanation": "Technicians are on the front line—social engineering or unsafe USB practices can introduce threats.",
        "exploitation": "Tricked into plugging in rogue devices or clicking malicious links.",
        "client_impact": "Infection of shop systems or customer data theft.",
        "compliance": "NHTSA Cyber Readiness – Training for service personnel.",
        "help": "I can create practical training workshops for auto service environments."
    },
    questions[7]: {
        "explanation": "Without a plan, even a small breach can spiral into a major incident.",
        "exploitation": "Attackers stay hidden longer when there's no reporting structure.",
        "client_impact": "Delayed response, more damage, and possible insurance issues.",
        "compliance": "NHTSA & CISA guidelines for incident response.",
        "help": "I can help you build a simple reporting chain and response guide for your team."
    },
    questions[8]: {
        "explanation": "OTA updates offer convenience but can be hijacked if not validated.",
        "exploitation": "An attacker could inject malware into an OTA update.",
        "client_impact": "Widespread vulnerability, recall risk, or loss of remote features.",
        "compliance": "ISO/SAE 21434 – OTA update security.",
        "help": "I can assess your OTA process and help you implement secure update distribution."
    },
    questions[9]: {
        "explanation": "Cheap IoT devices can introduce vulnerabilities into otherwise secure systems.",
        "exploitation": "Devices like GPS trackers or Wi-Fi hotspots could be exploited as backdoors.",
        "client_impact": "Risk to client privacy, data breaches, or shop system access.",
        "compliance": "Auto industry IoT security guidance.",
        "help": "I can review vendor devices for known issues and recommend secure alternatives."
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        answers = request.form
        score = sum(1 for q in questions if answers.get(q) == "yes")
        total = len(questions)
        failed = []

        for question in questions:
            if answers.get(question) == "no":
                failed.append({
                    "question": question,
                    "explanation": explanations[question]["explanation"],
                    "exploitation": explanations[question]["exploitation"],
                    "client_impact": explanations[question]["client_impact"],
                    "compliance": explanations[question]["compliance"],
                    "help": explanations[question]["help"]
                })

        # Risk level
        if score >= 9:
            level = "LOW – Solid posture!"
        elif score >= 6:
            level = "MODERATE – Some risk exposure."
        else:
            level = "HIGH – High exposure, take action!"

        return render_template("results.html", score=score, total=total, level=level, failed_questions=failed)

    return render_template("index.html", questions=questions)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
