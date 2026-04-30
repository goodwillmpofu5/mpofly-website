from flask import Flask, render_template_string, request, jsonify, url_for
from werkzeug.exceptions import HTTPException
import re
import os
import json
import traceback
import urllib.request
import urllib.error

app = Flask(__name__, static_folder="static")

# ==========================
# WEB3FORMS SETTINGS
# ==========================
# On Render, add this Environment Variable:
# Key: WEB3FORMS_ACCESS_KEY
# Value: your Web3Forms access key
WEB3FORMS_ACCESS_KEY = os.environ.get("WEB3FORMS_ACCESS_KEY")

# ==========================
# BUSINESS CONTACT DETAILS
# ==========================
BUSINESS_EMAIL = "goodwillmpofu5@gmail.com"
BUSINESS_CELLPHONE = "076 394 2737"
BUSINESS_WEBSITE = "https://www.mpofly.co.za"

# ==========================
# LOGO FILE
# ==========================
# Logo must be saved as: static/mpofly-logo.png
LOGO_FILENAME = "mpofly-logo.png"


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    if isinstance(error, HTTPException):
        return error

    print("Unexpected server error:")
    print(traceback.format_exc())

    return jsonify({
        "success": False,
        "error": str(error)
    }), 500


website_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mpofly Business Solutions</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #1f2937;
            background-color: #f3f6fb;
        }

        header {
            background-color: #001f4d;
            color: white;
            padding: 25px;
        }

        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 25px;
        }

        .business-title {
            text-align: left;
        }

        .business-title h1 {
            margin: 0;
            font-size: 2.8em;
            letter-spacing: 2px;
            color: white;
        }

        .business-title p {
            margin: 8px 0 0;
            color: #bfe7ff;
            font-weight: bold;
            font-size: 1.05em;
        }

        .header-logo {
            width: 145px;
            max-width: 35%;
            height: auto;
            border-radius: 8px;
        }

        nav {
            max-width: 1200px;
            margin: 22px auto 0 auto;
            text-align: center;
        }

        nav a {
            color: white;
            margin: 0 14px;
            text-decoration: none;
            font-weight: bold;
            transition: color 0.3s;
            cursor: pointer;
        }

        nav a:hover {
            color: #7db7ff;
        }

        .hero {
            background:
                linear-gradient(rgba(0, 31, 77, 0.86), rgba(0, 31, 77, 0.86)),
                url('https://via.placeholder.com/1200x450') no-repeat center center;
            background-size: cover;
            min-height: 430px;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            text-align: center;
            padding: 25px;
        }

        .hero-content {
            max-width: 900px;
        }

        .hero h1 {
            font-size: 3em;
            margin-bottom: 15px;
        }

        .hero p {
            font-size: 1.25em;
            line-height: 1.7;
            color: #e8f1ff;
        }

        .hero-button {
            display: inline-block;
            margin-top: 20px;
            padding: 13px 28px;
            background-color: #00aeea;
            color: white;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            cursor: pointer;
        }

        .hero-button:hover {
            background-color: #008fc4;
        }

        .container {
            max-width: 1200px;
            margin: 30px auto;
            padding: 25px;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 31, 77, 0.15);
        }

        section {
            margin: 35px 0;
        }

        h2 {
            font-size: 2em;
            color: #001f4d;
            border-bottom: 3px solid #001f4d;
            padding-bottom: 8px;
        }

        h3 {
            color: #001f4d;
        }

        p {
            line-height: 1.7;
            font-size: 1.05em;
        }

        .intro-box {
            background-color: #e8f1ff;
            border-left: 6px solid #001f4d;
            padding: 22px;
            border-radius: 8px;
        }

        .services-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 22px;
        }

        .service-card {
            background-color: #e8f1ff;
            border-left: 5px solid #001f4d;
            border-radius: 10px;
            padding: 22px;
            transition: transform 0.3s, box-shadow 0.3s, background-color 0.3s;
        }

        .service-card:hover {
            transform: translateY(-6px);
            background-color: #d6e8ff;
            box-shadow: 0 6px 18px rgba(0, 31, 77, 0.2);
        }

        .service-card h3 {
            margin-top: 0;
            font-size: 1.35em;
        }

        .service-card ul {
            padding-left: 20px;
            margin-bottom: 0;
        }

        .service-card li {
            margin-bottom: 9px;
            line-height: 1.5;
        }

        .highlight-section {
            background-color: #001f4d;
            color: white;
            padding: 28px;
            border-radius: 10px;
        }

        .highlight-section h2 {
            color: white;
            border-bottom: 3px solid #00aeea;
        }

        .highlight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 20px;
        }

        .highlight-box {
            background-color: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #00aeea;
        }

        .highlight-box h3 {
            color: #8de5ff;
            margin-top: 0;
        }

        .contact-box {
            background-color: #e8f1ff;
            border-left: 5px solid #001f4d;
            padding: 22px;
            border-radius: 8px;
        }

        .contact-link {
            color: #001f4d;
            font-weight: bold;
            cursor: pointer;
            text-decoration: underline;
        }

        .business-phone {
            font-weight: bold;
            color: #001f4d;
            font-size: 1.15em;
        }

        .business-website {
            font-weight: bold;
            color: #001f4d;
            text-decoration: underline;
        }

        footer {
            background-color: #001f4d;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 30px;
        }

        footer .footer-logo {
            width: 110px;
            max-width: 70%;
            height: auto;
            margin-bottom: 10px;
            border-radius: 8px;
        }

        footer p {
            margin: 5px 0;
        }

        .footer-link {
            color: #bfe7ff;
            font-weight: bold;
            text-decoration: none;
        }

        .footer-link:hover {
            color: white;
            text-decoration: underline;
        }

        .popup-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 31, 77, 0.78);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            padding: 15px;
        }

        .popup-box {
            background-color: white;
            width: 90%;
            max-width: 540px;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
            position: relative;
            max-height: 90vh;
            overflow-y: auto;
        }

        .popup-logo {
            width: 110px;
            max-width: 65%;
            display: block;
            margin: 0 auto 12px auto;
            border-radius: 8px;
        }

        .popup-box h2 {
            margin-top: 0;
            color: #001f4d;
            border-bottom: none;
            text-align: center;
        }

        .popup-phone {
            text-align: center;
            color: #001f4d;
            font-weight: bold;
            margin-bottom: 15px;
        }

        .close-btn {
            position: absolute;
            right: 18px;
            top: 12px;
            font-size: 28px;
            font-weight: bold;
            color: #001f4d;
            cursor: pointer;
        }

        .close-btn:hover {
            color: red;
        }

        form label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
            color: #001f4d;
        }

        form input,
        form textarea,
        form select {
            width: 100%;
            padding: 10px;
            margin-top: 6px;
            border: 1px solid #b5c7e6;
            border-radius: 6px;
            font-size: 15px;
            box-sizing: border-box;
        }

        form textarea {
            resize: none;
            height: 90px;
        }

        .submit-btn {
            margin-top: 20px;
            width: 100%;
            background-color: #001f4d;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .submit-btn:hover {
            background-color: #003c8f;
        }

        .message-box {
            display: none;
            margin-top: 15px;
            padding: 12px;
            border-radius: 6px;
            text-align: center;
            font-weight: bold;
        }

        .success-message {
            background-color: #dff6e3;
            color: #14532d;
        }

        .error-message {
            background-color: #ffe0e0;
            color: #8b0000;
        }

        .character-count {
            font-size: 13px;
            color: #555;
            text-align: right;
            margin-top: 4px;
        }

        @media (max-width: 768px) {
            header {
                text-align: center;
            }

            .header-content {
                flex-direction: column;
                text-align: center;
            }

            .business-title {
                text-align: center;
            }

            .business-title h1 {
                font-size: 2.3em;
            }

            .header-logo {
                width: 120px;
                max-width: 70%;
            }

            nav a {
                display: block;
                margin: 10px 0;
            }

            .hero h1 {
                font-size: 2.2em;
            }

            .hero p {
                font-size: 1.05em;
            }

            .popup-box {
                padding: 22px;
            }
        }
    </style>
</head>

<body>
    <header>
        <div class="header-content">
            <div class="business-title">
                <h1>MPOFLY</h1>
                <p>Fueling Innovation, Powering Success</p>
            </div>

            <img src="{{ logo_url }}" alt="Mpofly Logo" class="header-logo">
        </div>

        <nav>
            <a href="#about">About Us</a>
            <a href="#services">Services</a>
            <a href="#why-us">Why Mpofly</a>
            <a onclick="openPopup()">Contact</a>
        </nav>
    </header>

    <div class="hero">
        <div class="hero-content">
            <h1>Balance. Compliance. Financial Clarity.</h1>
            <p>
                Mpofly provides accounting, company support, tender support, payroll administration,
                data analysis, report writing, and business advisory services to help individuals,
                SMEs, and organisations operate with confidence.
            </p>
            <a class="hero-button" onclick="openPopup()">Request a Consultation</a>
        </div>
    </div>

    <div class="container">
        <section id="about">
            <h2>About Mpofly</h2>

            <div class="intro-box">
                <p>
                    Founded on a strong foundation of precision, professionalism, and trust,
                    Mpofly has evolved from a dynamic accounting firm into a multifaceted
                    business solutions powerhouse.
                </p>

                <p>
                    We offer integrated services across accounting, tax compliance, company
                    support, tenders, payroll, data analysis, report writing, and business
                    support. Our goal is to deliver clarity, strategy, and excellence across
                    diverse client needs.
                </p>
            </div>
        </section>

        <section id="services">
            <h2>Our Services</h2>

            <div class="services-grid">
                <div class="service-card">
                    <h3>Accounting Services</h3>
                    <ul>
                        <li>VAT Registration</li>
                        <li>Annual Return Filing</li>
                        <li>Financial Projections and Budgeting</li>
                        <li>Financial Statements</li>
                        <li>Issuance of Accountant Letters</li>
                        <li>PAYE, UIF and SDL support</li>
                        <li>SARS Objections Handling</li>
                        <li>Tax Clearance Certificates</li>
                        <li>Employee and Individual Tax Registration</li>
                        <li>SARS Representative Updates</li>
                        <li>Individual Income Tax Return Filing</li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3>Company Support Services</h3>
                    <ul>
                        <li>COIDA Registration</li>
                        <li>Letter of Good Standing</li>
                        <li>Central Supplier Database Registration</li>
                        <li>CIDB Registration</li>
                        <li>Beneficial Ownership Filing</li>
                        <li>Company Address Change with CIPC</li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3>Tender Support Services</h3>
                    <ul>
                        <li>Administrative Support for Tender Submissions</li>
                        <li>Professional Data Analysis</li>
                        <li>Taxation Query Management</li>
                        <li>Strategic and Technical Report Writing</li>
                        <li>Custom Automation App Development</li>
                        <li>Stakeholder Engagement and Communication</li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3>Payroll Administration</h3>
                    <ul>
                        <li>Preparation and Issuance of Payslips</li>
                        <li>Monthly UIF Returns</li>
                        <li>COIDA Return of Earnings</li>
                        <li>Employee Leave Management Systems</li>
                        <li>Issuing of IRP5 and IT3(a) Documents</li>
                        <li>Comprehensive Employee Record Maintenance</li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3>Business Intelligence and Analysis</h3>
                    <ul>
                        <li>Advanced Data Analysis</li>
                        <li>Strategic Report Writing</li>
                        <li>Business Intelligence Support</li>
                        <li>Financial Insight and Decision Support</li>
                        <li>Projection and Budget Analysis</li>
                    </ul>
                </div>

                <div class="service-card">
                    <h3>Human Resource and Talent Solutions</h3>
                    <ul>
                        <li>Human Resource Support</li>
                        <li>Employee Records Support</li>
                        <li>Talent and Workforce Administration</li>
                        <li>Leave Management Support</li>
                        <li>Employment Compliance Support</li>
                    </ul>
                </div>
            </div>
        </section>

        <section class="highlight-section" id="why-us">
            <h2>Why Work With Mpofly?</h2>

            <p>
                We are more than an accounting firm. We are your strategic financial and
                business support partner. We simplify complexity, help you meet obligations,
                and position your business for sustainable growth.
            </p>

            <div class="highlight-grid">
                <div class="highlight-box">
                    <h3>Designed For</h3>
                    <p>SMEs needing reliable services.</p>
                    <p>Professionals requiring tax clarity.</p>
                    <p>Entities navigating complex compliance.</p>
                </div>

                <div class="highlight-box">
                    <h3>What Sets Us Apart?</h3>
                    <p>Deep financial insight and experience.</p>
                    <p>SARS-savvy support and tax advisory.</p>
                    <p>Timely submissions and compliance updates.</p>
                    <p>Tailored projections for your business model.</p>
                </div>
            </div>
        </section>

        <section id="contact">
            <h2>Contact Us</h2>

            <div class="contact-box">
                <p>
                    Let us talk numbers that work for you. If you would like to learn more
                    about our services or schedule a consultation, please
                    <span class="contact-link" onclick="openPopup()">contact us</span>.
                </p>

                <p>
                    Business cellphone:
                    <span class="business-phone">076 394 2737</span>
                </p>

                <p>
                    Website:
                    <a href="{{ business_website }}" target="_blank" class="business-website">
                        www.mpofly.co.za
                    </a>
                </p>
            </div>
        </section>
    </div>

    <footer>
        <img src="{{ logo_url }}" alt="Mpofly Logo" class="footer-logo">
        <p>&copy; 2026 Mpofly. All rights reserved.</p>
        <p>Business Cellphone: 076 394 2737</p>
        <p>
            Website:
            <a href="{{ business_website }}" target="_blank" class="footer-link">
                www.mpofly.co.za
            </a>
        </p>
    </footer>

    <div class="popup-overlay" id="contactPopup">
        <div class="popup-box">
            <span class="close-btn" onclick="closePopup()">&times;</span>

            <img src="{{ logo_url }}" alt="Mpofly Logo" class="popup-logo">

            <h2>Contact Mpofly</h2>

            <p class="popup-phone">
                Business Cellphone: 076 394 2737
            </p>

            <form id="contactForm">
                <label for="fullname">Full Name</label>
                <input
                    type="text"
                    id="fullname"
                    name="fullname"
                    maxlength="50"
                    required
                    placeholder="Enter your full name"
                >

                <label for="email">Email Address</label>
                <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    placeholder="example@email.com"
                >

                <label for="cellphone">Cellphone</label>
                <input
                    type="text"
                    id="cellphone"
                    name="cellphone"
                    maxlength="10"
                    required
                    placeholder="Enter your 10-digit cellphone number"
                    oninput="this.value = this.value.replace(/[^0-9]/g, '')"
                >

                <label for="service">Service Required</label>
                <select id="service" name="service" required>
                    <option value="">Select a service</option>
                    <option value="Accounting Services">Accounting Services</option>
                    <option value="Company Support Services">Company Support Services</option>
                    <option value="Tender Support Services">Tender Support Services</option>
                    <option value="Payroll Administration">Payroll Administration</option>
                    <option value="Business Intelligence and Analysis">Business Intelligence and Analysis</option>
                    <option value="Human Resource and Talent Solutions">Human Resource and Talent Solutions</option>
                    <option value="Other">Other</option>
                </select>

                <label for="message">How can Mpofly help you?</label>
                <textarea
                    id="message"
                    name="message"
                    maxlength="100"
                    required
                    placeholder="Type your message here"
                    oninput="updateCharacterCount()"
                ></textarea>

                <div class="character-count">
                    <span id="charCount">0</span>/100 characters
                </div>

                <button type="submit" class="submit-btn">Submit</button>

                <div class="message-box success-message" id="successMessage">
                    Thank you. Your message has been sent successfully.
                </div>

                <div class="message-box error-message" id="errorMessage">
                    Sorry, your message could not be sent. Please try again.
                </div>
            </form>
        </div>
    </div>

    <script>
        function openPopup() {
            document.getElementById("contactPopup").style.display = "flex";
        }

        function closePopup() {
            document.getElementById("contactPopup").style.display = "none";
        }

        function updateCharacterCount() {
            const message = document.getElementById("message");
            const charCount = document.getElementById("charCount");
            charCount.textContent = message.value.length;
        }

        document.getElementById("contactForm").addEventListener("submit", async function(event) {
            event.preventDefault();

            const fullname = document.getElementById("fullname").value.trim();
            const email = document.getElementById("email").value.trim();
            const cellphone = document.getElementById("cellphone").value.trim();
            const service = document.getElementById("service").value.trim();
            const message = document.getElementById("message").value.trim();

            const successMessage = document.getElementById("successMessage");
            const errorMessage = document.getElementById("errorMessage");

            successMessage.style.display = "none";
            errorMessage.style.display = "none";

            const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;

            if (fullname.length === 0 || fullname.length > 50) {
                alert("Full name is required and must not exceed 50 characters.");
                return;
            }

            if (!emailPattern.test(email)) {
                alert("Please enter a valid email address.");
                return;
            }

            if (!/^\\d{10}$/.test(cellphone)) {
                alert("Cellphone number must contain exactly 10 numeric digits.");
                return;
            }

            if (service.length === 0) {
                alert("Please select the service you need.");
                return;
            }

            if (message.length === 0 || message.length > 100) {
                alert("Message is required and must not exceed 100 characters.");
                return;
            }

            try {
                const response = await fetch("/send-message", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        fullname: fullname,
                        email: email,
                        cellphone: cellphone,
                        service: service,
                        message: message
                    })
                });

                const result = await response.json();

                if (result.success) {
                    successMessage.textContent = "Thank you. Your message has been sent successfully.";
                    successMessage.style.display = "block";

                    setTimeout(function() {
                        document.getElementById("contactForm").reset();
                        document.getElementById("charCount").textContent = "0";
                        successMessage.style.display = "none";
                        closePopup();
                    }, 2500);
                } else {
                    errorMessage.textContent = "Error: " + result.error;
                    errorMessage.style.display = "block";
                }

            } catch (error) {
                errorMessage.textContent = "Error: " + error.message;
                errorMessage.style.display = "block";
            }
        });

        window.onclick = function(event) {
            const popup = document.getElementById("contactPopup");

            if (event.target === popup) {
                closePopup();
            }
        }
    </script>
</body>
</html>
"""


@app.route("/")
def home():
    logo_url = url_for("static", filename=LOGO_FILENAME)
    return render_template_string(
        website_html,
        logo_url=logo_url,
        business_website=BUSINESS_WEBSITE
    )


@app.route("/send-message", methods=["POST"])
def send_message():
    try:
        data = request.get_json(silent=True)

        if data is None:
            return jsonify({
                "success": False,
                "error": "No form data received."
            })

        fullname = data.get("fullname", "").strip()
        email = data.get("email", "").strip()
        cellphone = data.get("cellphone", "").strip()
        service = data.get("service", "").strip()
        message = data.get("message", "").strip()

        valid_services = [
            "Accounting Services",
            "Company Support Services",
            "Tender Support Services",
            "Payroll Administration",
            "Business Intelligence and Analysis",
            "Human Resource and Talent Solutions",
            "Other"
        ]

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if len(fullname) == 0 or len(fullname) > 50:
            return jsonify({
                "success": False,
                "error": "Invalid full name. Maximum is 50 characters."
            })

        if not re.match(email_pattern, email):
            return jsonify({
                "success": False,
                "error": "Invalid email address."
            })

        if not cellphone.isdigit() or len(cellphone) != 10:
            return jsonify({
                "success": False,
                "error": "Invalid cellphone number. It must be exactly 10 digits."
            })

        if service not in valid_services:
            return jsonify({
                "success": False,
                "error": "Invalid service selected."
            })

        if len(message) == 0 or len(message) > 100:
            return jsonify({
                "success": False,
                "error": "Invalid message. Maximum is 100 characters."
            })

        if not WEB3FORMS_ACCESS_KEY:
            return jsonify({
                "success": False,
                "error": "Web3Forms access key is missing. Add WEB3FORMS_ACCESS_KEY in Render Environment Variables."
            })

        web3forms_payload = {
            "access_key": WEB3FORMS_ACCESS_KEY,
            "subject": "New Mpofly Contact Form Message",
            "from_name": "Mpofly Website",
            "email": email,
            "name": fullname,
            "phone": cellphone,
            "service_required": service,
            "message": message,
            "business_cellphone": BUSINESS_CELLPHONE,
            "business_website": BUSINESS_WEBSITE,
            "to_email": BUSINESS_EMAIL
        }

        request_data = json.dumps(web3forms_payload).encode("utf-8")

        web3forms_request = urllib.request.Request(
            "https://api.web3forms.com/submit",
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(web3forms_request, timeout=30) as response:
            response_body = response.read().decode("utf-8")
            web3forms_response = json.loads(response_body)

        if web3forms_response.get("success"):
            return jsonify({"success": True})

        return jsonify({
            "success": False,
            "error": web3forms_response.get("message", "Web3Forms could not send the message.")
        })

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print("Web3Forms HTTP error:")
        print(error_body)

        return jsonify({
            "success": False,
            "error": error_body
        }), 500

    except Exception as e:
        print("Contact form sending error:")
        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=False)S