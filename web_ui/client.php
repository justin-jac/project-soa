<?php
include 'css/colpal.php';
?>


<style>
    #example_wrapper {
        background: white;
        padding: 50px;
        border-color: black;
        border-radius: 20px;
        border-style: solid;
    }
</style>

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
                <input type="text" class="form-control" id="nama_input" placeholder="Nama">
                <label for="floatingInput">Nama</label>
            </div>

            <div class="form-floating">
                <textarea class="form-control" placeholder="Leave a comment here" id="description_input" style="height: 100px"></textarea>
                <label for="floatingTextarea2">Deskripsi</label>
            </div>

            <div style="margin: 15px 0px 15px 0px;">
                <label>Date</label>
                <input type="date" name="party" min="2000-01-01" id="date_input">
            </div>

            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="price_input" placeholder="Nama">
                <label for="floatingInput">Price</label>
            </div>

        </div>

        <center style="margin: 25px;">
            <a href="client.php">
                <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>; font-weight:500;" onclick="createOrder()">SUBMIT FORM</button>
            </a>
        </center>
    </div>

    <!-- TABLE -->

    <div class="container">
        <center>
            <!-- <h1 style="margin: 3%;font-family:Quicksand;">order TABLE MANAGEMENT</h1> -->
        </center>

        <table id="example" class="table table-striped table-bordered" style="width: 100%; color: <?= $dark ?>">

            <thead>
                <tr>
                    <th>Id</th>
                    <th>Nama Order</th>
                    <th>Description Order</th>
                    <th>Order Date</th>
                    <th>Order Price</th>
                </tr>
            </thead>

            <tbody id="orderList">
                <tr>
                    <td style="color:<?= $dark ?>">
                        id
                    </td>
                    <td style="color:<?= $dark ?>">
                        email
                    </td>
                    <td style="color:<?= $dark ?>">
                        nama
                    </td>
                    <td style="color:<?= $dark ?>">
                        password
                    </td>
                    <td style="color:<?= $dark ?>">

                    </td>
                </tr>
            </tbody>

        </table>
        <center style="margin: 55px;">
        </center>
    </div>
    <!--  -->
</body>

</html>


<script>
    function getOrderList() {
        $.ajax({
            type: "GET",
            url: "http://localhost:5530/organizer/order",
            success: function(response) {
                var client_id_temp = 1

                // Handle success response

                var orders = response;
                var orderList = $("#orderList");
                orderList.empty();

                for (var i = 0; i < orders.length; i++) {
                    var order = orders[i];
                    if (order.id_client == client_id_temp) {
                        var orderRow = createOrderRow(order);
                        orderList.append(orderRow);
                    }
                }

            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log("Failed to retrieve order list: " + error);
            }
        });
    }

    // Call the function to retrieve and display the order list when the page loads
    $(document).ready(function() {
        getOrderList();
    });

    // Function to dynamically create the order rows
    function createOrderRow(order) {
        var orderRow = $("<tr id='order-row-" + order.id_order + "'></tr>");
        orderRow.append("<td>" + order.id_order + "</td>");
        orderRow.append("<td><input type='text' class='nama-order' value='" + order.order_name + "' disabled></td>");
        orderRow.append("<td><input type='text' class='desc-order' value='" + order.order_description + "' disabled></td>");
        orderRow.append("<td><input type='text' class='date-order' value='" + order.order_date + "' disabled></td>");
        orderRow.append("<td><input type='text' class='price-order' value='" + order.total_price + "' disabled></td>");

        // orderRow.append('<td><center><button type="button" class="btn btn-info edit-order" onclick="editOrder(' + order.id_order + ')">EDIT</button><button type="button" class="btn btn-success save-order" style="display:none" onclick="saveOrder(' + order.id_order + ')">SAVE</button><button type="button" class="btn btn-danger" onclick="deleteorder(' + order.id_order + ')">DELETE</button></center></td>');

        orderRow.append('<td><center><button type="button" class="btn btn-info edit-order" onclick="viewDetails(' + order.id_order + ')">VIEW DETAILS</button></center></td>');

        // var actionsCell = $("<td></td>");
        // actionsCell.append("<button class='edit-order' onclick='editOrder(" + order.idOrder + ")'>Edit</button>");
        // actionsCell.append("<button class='save-order' onclick='saveOrder(" + order.idOrder + ")' style='display:none'>Save</button>");
        // actionsCell.append("<button class='delete-order' onclick='deleteOrder(" + order.idOrder + ")'>Delete</button>");
        // orderRow.append(actionsCell);

        return orderRow;
    }

    function viewDetails() {
        $.ajax({
            type: "GET",
            url: "http://localhost:5530/organizer/order",
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

    // Function to send a POST request to create a new order
    function createOrder() {
        var orderData = {
            // "email": $("#email_input").val(),
            // "nama": $("#nama_input").val(),
            // "password": $("#password_input").val(),

            // "id_client": $("#nama_input").val(),
            "id_client": 1,
            "order_name": $("#nama_input").val(),
            "order_description": $("#description_input").val(),
            "order_date": $("#date_input").val(),
            "total_price": $("#price_input").val(),
            "status": "Pending"
        };

        alert(JSON.stringify(orderData))

        $.ajax({
            type: "POST",
            url: "http://localhost:5530/organizer/order",
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