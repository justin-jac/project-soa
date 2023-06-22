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
    <!--  -->

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

<body> <!-- partial:index.partial.html -->

    <section>

        <div class="signin">

            <div class="content">

                <h2>Sign Up as Client</h2>

                <div class="form">
                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="email_input" placeholder="name@example.com">
                        <label for="floatingInput">Email</label>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="nama_input" placeholder="Nama">
                        <label for="floatingInput">Nama</label>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="password" class="form-control" id="password_input" placeholder="Password">
                        <label for="floatingInput">Password</label>
                    </div>

                    <div class="form-floating mb-3">
                        <input type="text" class="form-control" id="contact_input" placeholder="Contact Person">
                        <label for="floatingInput">Contact Person</label>
                    </div>

                    <div class="links">
                        <a href="signup_staff.php">Sign up as a Staff?</a>
                    </div>

                    <div>

                        <center style="margin: 25px;">
                            <a href="index.php">
                                <button type="button" class="btn btn-success" style="padding: 10px;background: #41EAD4;color: #000;font-weight: 600;font-size: 1.35em;letter-spacing: 0.05em;cursor: pointer;width:100%" onclick="createClient()">SIGN UP</button>
                            </a>
                        </center>

                    </div>

                </div>

            </div>

        </div>

    </section> <!-- partial -->

</body>

</html>


<script>
    // Function to send a POST request to create a new order
    function createClient() {
        var orderData = {
            "email": $("#email_input").val(),
            "nama": $("#nama_input").val(),
            "contact_person": $("#contact_input").val(),
            "password": $("#password_input").val()
            // "email": "123",
            // "nama": "321",
            // "contact_person": "321",
            // "password": "345"
        };

        alert(JSON.stringify(orderData))

        $.ajax({
            type: "POST",
            url: "http://localhost:5500/organizer/client",
            async: false,
            data: JSON.stringify(orderData),
            contentType: "application/json",
            // success: function(response) {
            //     // Handle success response
            //     alert("Order created successfully!");
            // },
            // error: function(xhr, status, error) {
            //     // Handle error response
            //     alert("Failed to create order: " + error);
            // }
        });
    }
</script>