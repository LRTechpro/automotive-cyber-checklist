<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automotive Cybersecurity Checklist</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f2f5f7;
            color: #333;
            padding: 20px;
        }
        .container {
            background: #ffffff;
            max-width: 800px;
            margin: auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.08);
        }
        h1 {
            color: #0077cc;
            margin-bottom: 10px;
        }
        p.description {
            font-size: 1em;
            margin-bottom: 20px;
        }
        .question-block {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #fdfdfd;
            border-left: 5px solid #0077cc;
            border-radius: 8px;
        }
        .question-block label {
            font-weight: bold;
        }
        .submit-btn {
            display: block;
            margin: 20px auto 0;
            background-color: #0077cc;
            color: white;
            padding: 12px 25px;
            font-size: 1em;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        .submit-btn:hover {
            background-color: #005fa3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-list-check"></i> Automotive Cybersecurity Checklist</h1>
        <p class="description">
            This interactive checklist is designed to help small to mid-sized automotive aftermarket companies critically evaluate their current cybersecurity practices when working with modern connected vehicles.
        </p>
        <form method="POST">
            {% for question in questions %}
                <div class="question-block">
                    <label><i class="fas fa-question-circle"></i> {{ question }}</label><br>
                    <input type="radio" name="{{ question }}" value="yes" required> Yes
                    <input type="radio" name="{{ question }}" value="no"> No
                </div>
            {% endfor %}
            <button type="submit" class="submit-btn"><i class="fas fa-shield-halved"></i> Submit Assessment</button>
        </form>
    </div>
</body>
</html>
