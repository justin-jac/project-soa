<?php

session_start();
$_SESSION['id_user'] = 0;


?>
<!doctype html>

<html lang="en">

<head>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
    <link rel="stylesheet" href="css/background2.css">

    <!-- Untuk DataTables -->
    <script src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap4.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.2/css/bootstrap.css">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap4.min.css">

    <!-- Online Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    </style>

    <!-- Local Font -->
    <link rel="stylesheet" href="font/Quicksand-VariableFont_wght.ttf">
    <link rel="stylesheet" href="font/static/Quicksand-Bold.ttf">
    <link rel="stylesheet" href="font/static/Quicksand-Light.ttf">
    <link rel="stylesheet" href="font/static/Quicksand-Medium.ttf">
    <link rel="stylesheet" href="font/static/Quicksand-Regular.ttf">
    <link rel="stylesheet" href="font/static/Quicksand-SemiBold.ttf">
    <!--  -->

    <link rel="stylesheet" href="css/login.css">
    <link rel="stylesheet" href="css/background2.css">

</head>

<body>

    <section>
        <div class="signin">
            <div class="content">
                <h2>Log In!</h2>
                <div class="form">

                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="email_input" placeholder="name@example.com">
                        <label for="floatingInput">Email</label>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="password_input" placeholder="Password">
                        <label for="floatingInput">Password</label>
                    </div>

                    <div class="links">
                        <a href="signup_staff.php">Signup as Staff</a>
                        <a href="signup_client.php">Signup as Client</a>
                    </div>

                    <div>
                        <center style="margin: 25px;">
                            <button type="button" class="btn btn-success" style="padding: 10px;background: #41EAD4;color: #000;font-weight: 600;font-size: 1.35em;letter-spacing: 0.05em;cursor: pointer;width:100%" onclick="login()">SIGN UP</button>
                        </center>
                    </div>

                </div>
            </div>
        </div>
    </section>

    <script>
    function login() {
        var username = $("#email_input").val(); // Get the entered username
        var password = $("#password_input").val(); // Get the entered password

        // Prepare the data object for the POST request
        var data = {
            "username": username,
            "password": password
        };

        // Perform AJAX POST request to the login URL
        $.ajax({
            type: "POST",
            url: "http://localhost:5520/organizer/login",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(response) {
                // Handle success response
                var id_user_get = response.id_user;
                var user_status = response.user_status;

                if (user_status === "Staff") {
                    // User is a staff, perform staff login action
                    alert("Staff login successful!");
                    window.location.href = "staff.php?id_user=" + id_user_get;

                    // Redirect to the desired staff page or perform any other staff action
                } else if (user_status === "Client") {
                    // User is a client, perform client login action
                    alert("Client login successful!");
                    window.location.href = "client.php?id_user=" + id_user_get;

                    // Redirect to the desired client page or perform any other client action
                } else {
                    // Invalid user status
                    alert("Invalid user status!");
                }
            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log("Login error: " + error);
                alert("Invalid username or password!");
            }
        });
    }
</script>
</body>

</html>
