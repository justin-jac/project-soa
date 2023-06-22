<?php
include 'css/colpal.php';
?>

<html lang="en">
<!doctype html>

<head>


    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ORDER INPUT FORM</title>

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

    <script>
        $(document).ready(function() {
            $('#example').DataTable();
        });
    </script>
    <!--  -->

</head>

<body style="background-color:<?= $light ?>; font-family:Quicksand; color:<?= $dark ?>">
    <div class="container">
        <center>
            <h1 style="margin: 3%;font-family:Quicksand;">ORDER INPUT FORM</h1>
        </center>

        <div id="board">

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

        </div>

        <center style="margin: 25px;">
            <a href="staff.php">
                <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>; font-weight:500;" onclick="createStaff()">SUBMIT FORM</button>
            </a>
        </center>
    </div>
</body>

</html>

<script>
    // Function to send a POST request to create a new order
    function createStaff() {
        var orderData = {
            "email": $("#email_input").val(),
            "nama": $("#nama_input").val(),
            "password": $("#password_input").val(),
        };

        alert(JSON.stringify(orderData))

        $.ajax({
            type: "POST",
            url: "http://localhost:5510/organizer/staf",
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