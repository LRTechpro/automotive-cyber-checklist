from flask import Flask, render_template, request, make_response
from io import BytesIO
from xhtml2pdf import pisa

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
    }
    # Remaining questions follow the same format with updated content
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/checklist', methods=['GET', 'POST'])
def checklist():
    if request.method == 'POST':
        answers = request.form
        score = sum(1 for q in questions if answers.get(q) == 'yes')

        if score >= 8:
            level = "LOW – Strong security posture."
        elif score >= 5:
            level = "MODERATE – Some concerns to address."
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
                    "compliance": details.get("compliance", "Compliance risk unknown."),
                    "help": details.get("help", "I can assist with strengthening this area.")
                })

        return render_template('result.html', score=score, total=len(questions), level=level,
                               answers=answers, questions=questions, failed_questions=failed_questions)

    return render_template('index.html', questions=questions)

@app.route('/download', methods=['POST'])
def download():
    answers = request.form
    score = sum(1 for q in questions if answers.get(q) == 'yes')

    if score >= 8:
        level = "LOW – Strong security posture."
    elif score >= 5:
        level = "MODERATE – Some concerns to address."
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
                "compliance": details.get("compliance", "Compliance risk unknown."),
                "help": details.get("help", "I can assist with strengthening this area.")
            })

    rendered = render_template("pdf_template.html", answers=answers, questions=questions,
                               score=score, level=level, failed_questions=failed_questions)
    pdf = BytesIO()
    pisa.CreatePDF(rendered, dest=pdf)

    response = make_response(pdf.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=cyber_audit_report.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)
