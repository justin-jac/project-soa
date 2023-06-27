<?php
include 'css/colpal.php';
if (isset($_GET['id_order'])) {
    $id_order = $_GET['id_order'];

    // Store it in the session if required
    // $_SESSION['id_user']
    // echo ($_SESSION['id_user']);
} else {
    // Handle the case when id_user is not provided
}

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
    <title>EVENT LIST</title>

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
            <h1 style="margin: 3%;font-family:Quicksand;">ORDER'S EVENT MANAGEMENT</h1>
        </center>

        <table id="example" class="table table-striped table-bordered" style=" color: <?= $dark ?>">

            <thead>
                <tr>
                    <th>Id</th>
                    <th>Event Name</th>
                    <th>Description</th>
                    <th>Sub Total Price</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th></th>
                </tr>
            </thead>

            <tbody id="orderList">

            </tbody>

        </table>
        <div style="width:50px"></div>
        <center style="margin: 25px;">
            <a href="order_details.php?id_order=" <?= $id_order ?>></a>
            <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>; font-weight: 500;">ADD EVENT</button>
        </center>
    </div>
</body>

</html>

<script>
    // Call the function to retrieve and display the order list when the page loads
    $(document).ready(function() {
        getOrderList();
    });

    function getOrderList() {
        $.ajax({
            type: "GET",
            url: "http://localhost:5530/organizer/order",
            success: function(response) {

                // Handle success response
                var order_id = 1;

                var orders = response;
                var orderList = $("#orderList");
                orderList.empty();

                for (var i = 0; i < orders.length; i++) {
                    var order = orders[i];

                    if (order.id_order === order_id) {
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

    // Function to dynamically create the order rows
    function createOrderRow(order) {
        var orderRow = $("<tr id='order-row-" + order.id_order + "'></tr>");
        orderRow.append("<td> <input style='width:50px' type='text' class='id-event' value='" + order.id_order + "' disabled></td>");
        orderRow.append("<td> <input type='text' class='name-event' value='" + order.order_name + "' disabled></td>");
        orderRow.append("<td> <input type='text' class='description-event' value='" + order.order_description + "' disabled></td>");
        orderRow.append("<td> <input type='text' class='date-event' value='" + order.order_date + "' disabled></td>");
        orderRow.append("<td> <input type='text' class='price-event' value='" + order.total_price + "' disabled></td>");
        orderRow.append("<td> <input type='text' class='status-event' value='" + order.status + "' disabled></td>");

        orderRow.append('<td><center><button type="button" class="btn btn-info" style=" background-color: <?= $p3 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>;font-weight:500;">EDIT</button><button type="button" class="btn btn-danger" style="background-color: <?= $p1 ?>; border-color: <?= $light ?>; color: <?= $light ?>; font-weight:500;">DELETE</button></center></td>');

        return orderRow;
    }
</script>