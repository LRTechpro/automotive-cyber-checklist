from flask import Flask, render_template, request, make_response
from flask_mail import Mail, Message
from xhtml2pdf import pisa
from io import BytesIO

app = Flask(__name__)

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

explanations = {
    "Do you use secure access control for diagnostic tools?": {
        "why": "Unauthorized access to diagnostic ports can let attackers reprogram ECUs or disable safety features.",
        "exploit": "An attacker could plug into the OBD-II port and alter vehicle behavior.",
        "impact": "Risk to driver safety, liability issues, and possible regulatory noncompliance.",
        "compliance": "NHTSA Cybersecurity Best Practices – Access control.",
        "help": "I can help implement authentication and logging controls for diagnostics."
    },
    "Are all software updates signed and verified?": {
        "why": "Unsigned updates can be tampered with to introduce malware into ECUs or infotainment systems.",
        "exploit": "A malicious update could compromise braking or acceleration modules.",
        "impact": "Severe safety risk, potential recalls, and reputational harm.",
        "compliance": "ISO/SAE 21434 – Secure update procedures.",
        "help": "I can help implement signed firmware and update validation checks."
    },
    "Is USB or external media access restricted in service bays?": {
        "why": "Uncontrolled USB use can allow malware to enter service systems or even connect to vehicle networks.",
        "exploit": "A technician could unintentionally install malware that spreads via CAN or Ethernet interfaces.",
        "impact": "Operational disruption, privacy violations, or vehicle control issues.",
        "compliance": "Automotive Cyber Best Practices – Removable media controls.",
        "help": "I can help create device policies and implement endpoint protection for service bays."
    },
    "Are default passwords changed on all automotive devices?": {
        "why": "Default credentials are commonly published online and easily abused.",
        "exploit": "Attackers can access networked diagnostic tools, cameras, or routers still using defaults.",
        "impact": "Unauthorized system access and data leaks.",
        "compliance": "NIST 800-82 – Industrial system hardening guidance.",
        "help": "I can help audit credentials and enforce password change policies."
    },
    "Is client vehicle data encrypted when stored or transmitted?": {
        "why": "Sensitive data like VINs, locations, and diagnostic reports need protection from eavesdropping or theft.",
        "exploit": "Unencrypted databases or wireless transmission could be intercepted.",
        "impact": "Loss of trust, potential lawsuits, and vendor risk.",
        "compliance": "GDPR/Data Privacy Best Practices.",
        "help": "I can help implement AES encryption and TLS-based transmission protocols."
    },
    "Are vehicle telematics interfaces audited for vulnerabilities?": {
        "why": "Telematics systems connect vehicles to external servers and can expose major attack surfaces.",
        "exploit": "An attacker could compromise GPS or remote unlock features.",
        "impact": "Tracking, unauthorized control, or customer privacy breaches.",
        "compliance": "ISO/SAE 21434 – Risk analysis for interfaces.",
        "help": "I can assist with penetration testing and hardening of telematics paths."
    },
    "Do technicians receive cybersecurity awareness training?": {
        "why": "Technicians are on the front line—social engineering or unsafe USB practices can introduce threats.",
        "exploit": "Tricked into plugging in rogue devices or clicking malicious links.",
        "impact": "Infection of shop systems or customer data theft.",
        "compliance": "NHTSA Cyber Readiness – Training for service personnel.",
        "help": "I can create practical training workshops for auto service environments."
    },
    "Is there a procedure for reporting and handling cyber incidents?": {
        "why": "Without a plan, even a small breach can spiral into a major incident.",
        "exploit": "Attackers stay hidden longer when there's no reporting structure.",
        "impact": "Delayed response, more damage, and possible insurance issues.",
        "compliance": "NHTSA & CISA guidelines for incident response.",
        "help": "I can help you build a simple reporting chain and response guide for your team."
    },
    "Are firmware updates done through secure OTA processes?": {
        "why": "OTA updates offer convenience but can be hijacked if not validated.",
        "exploit": "An attacker could inject malware into an OTA update.",
        "impact": "Widespread vulnerability, recall risk, or loss of remote features.",
        "compliance": "ISO/SAE 21434 – OTA update security.",
        "help": "I can assess your OTA process and help you implement secure update distribution."
    },
    "Are aftermarket IoT devices assessed before installation?": {
        "why": "Cheap IoT devices can introduce vulnerabilities into otherwise secure systems.",
        "exploit": "Devices like GPS trackers or Wi-Fi hotspots could be exploited as backdoors.",
        "impact": "Risk to client privacy, data breaches, or shop system access.",
        "compliance": "Auto industry IoT security guidance.",
        "help": "I can review vendor devices for known issues and recommend secure alternatives."
    }
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/checklist', methods=['GET', 'POST'])
def checklist():
    if request.method == 'POST':
        answers = request.form
        score = sum(1 for q in questions if answers.get(q) == 'yes')

        if score >= 9:
            level = "LOW – Strong security awareness!"
        elif score >= 5:
            level = "MODERATE – Some areas need work."
        else:
            level = "HIGH – High exposure, take action!"

        failed_questions = []
        for q in questions:
            if answers.get(q) != 'yes':
                details = explanations.get(q, {})
                failed_questions.append({
                    "question": q,
                    "explanation": details.get("why", "No explanation provided."),
                    "exploitation": details.get("exploit", "No data."),
                    "client_impact": details.get("impact", "No impact info."),
                    "compliance": details.get("compliance", "Compliance guidance unavailable."),
                    "help": details.get("help", "I can assist with strengthening this area.")
                })

        return render_template('result.html', score=score, total=len(questions), level=level,
                               answers=answers, questions=questions, failed_questions=failed_questions)

    return render_template('index.html', questions=questions)

@app.route('/download', methods=['POST'])
def download():
    answers = request.form
    score = sum(1 for q in questions if answers.get(q) == 'yes')

    if score >= 9:
        level = "LOW – Strong security awareness!"
    elif score >= 5:
        level = "MODERATE – Some areas need work."
    else:
        level = "HIGH – High exposure, take action!"

    failed_questions = []
    for q in questions:
        if answers.get(q) != 'yes':
            details = explanations.get(q, {})
            failed_questions.append({
                "question": q,
                "explanation": details.get("why", "No explanation provided."),
                "exploitation": details.get("exploit", "No data."),
                "client_impact": details.get("impact", "No impact info."),
                "compliance": details.get("compliance", "Compliance guidance unavailable."),
                "help": details.get("help", "I can assist with strengthening this area.")
            })

    rendered = render_template("pdf_template.html", answers=answers, questions=questions,
                               score=score, level=level, failed_questions=failed_questions)
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cyber_posture_report.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
