<?php
include 'css/colpal.php';

session_start();

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
    <title>ORDER DETAIL LIST</title>

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
            <h1 style="margin: 3%;font-family:Quicksand;">ORDER DETAILS</h1>
        </center>

        <table id="example" class="table table-striped table-bordered" style="width: 100%; color: <?= $dark ?>">

            <thead>
                <tr>
                    <th>Id</th>
                    <th>Event Name</th>
                    <th>Description</th>
                    <th>Sub Total Price</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                </tr>
            </thead>

            <tbody id="staffList">

            </tbody>

        </table>

    </div>
    <div class="container">
        <center>
            <h1 style="margin: 3%;font-family:Quicksand;">EVENT INPUT FORM</h1>
        </center>

        <div id="board">

            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="nama_input" placeholder="Nama">
                <label for="floatingInput">Event name</label>
            </div>

            <div class="form-floating">
                <textarea class="form-control" placeholder="Leave a comment here" id="description_input" style="height: 100px"></textarea>
                <label for="floatingTextarea2">Deskripsi</label>
            </div>

            <div class="form-floating mb-3" style="margin-top: 20px;">
                <input type="number" class="form-control" id="price_input" placeholder="Nama">
                <label for="floatingInput">Sub Total Price</label>
            </div>

            <div style="margin: 15px 0px 15px 0px;">
                <label>Start Time</label><br>
                <input type="time" id="start_input">
            </div>

            <div style="margin: 15px 0px 15px 0px;">
                <label>End Time</label><br>
                <input type="time" id="end_input">
            </div>

        </div>

        <center style="margin: 25px;">
            <a href='order_list_view.php'>
                <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>; font-weight:500;" onclick="createOrder()">SUBMIT FORM</button>
            </a>
        </center>
    </div>
</body>

</html>

<script>
    // Function to send a POST request to create a new order
    function createOrder() {
        var orderData = {
            "id_staffPIC": <?= $_SESSION['id_user'] ?>,
            "event_name": $("#nama_input").val(),
            "event_description": $("#description_input").val(),
            "sub_total": $("#price_input").val(),
            "start_time": $("#start_input").val(),
            "end_time": $("#end_input").val(),
            // "id_event": orderId
        };

        alert(JSON.stringify(orderData))

        $.ajax({
            type: "POST",
            url: "http://localhost:5540/organizer/event/order/<?= $_GET['id_order'] ?>",
            async: false,
            data: JSON.stringify(orderData),
            contentType: "application/json",
        });
    }

    // Call the function to retrieve and display the staff list when the page loads
    $(document).ready(function() {
        getStaffList();
    });

    function getStaffList() {

        $.ajax({
            type: "GET",
            url: "http://localhost:5540/organizer/event/order/<?= $_GET['id_order'] ?>",
            success: function(response) {
                // Handle success response

                // var order_id = 1;

                var staffs = response;
                var staffList = $("#staffList");
                staffList.empty();

                for (var i = 0; i < staffs.length; i++) {
                    var staff = staffs[i];
                    // if (staff.id_order === order_id) {
                    var staffRow = createStaffRow(staff);
                    staffList.append(staffRow);
                    // }
                }

            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log("Failed to retrieve staff list: " + error);
            }
        });
    }

    // Function to dynamically create the staff rows
    function createStaffRow(staff) {
        var staffRow = $("<tr id='staff-row-" + staff.id_event + "'></tr>");
        staffRow.append("<td>" + staff.id_event + "</td>");
        staffRow.append("<td><input type='text' class='name-staff' value='" + staff.event_name + "' disabled></td>");
        staffRow.append("<td><input type='text' class='description-staff' value='" + staff.event_description + "' disabled></td>");
        staffRow.append("<td><input style='width:100px' type='text' class='sub_total-staff' value='" + staff.sub_total + "' disabled></td>");
        staffRow.append("<td><input style='width:100px' type='text' class='start_time-staff' value='" + staff.start_time + "' disabled></td>");
        staffRow.append("<td><input style='width:100px' type='text' class='end_time-staff' value='" + staff.end_time + "' disabled></td>");

        staffRow.append('<td><center><button type="button" class="btn btn-info edit-order" onclick="editOrder(' + staff.id_event + ')">EDIT</button><button type="button" class="btn btn-success save-order" style="display:none" onclick="saveOrder(' + staff.id_event + ')">SAVE</button><button type="button" class="btn btn-danger" onclick="deleteStaff(' + staff.id_event + ')">DELETE</button></center></td>');


        return staffRow;
    }

    // Edit button click event handler
    function editOrder(orderId) {
        var orderRow = $("#staff-row-" + orderId);

        // Enable input fields for editing
        // orderRow.find(".id-client").prop("disabled", false);
        orderRow.find(".name-staff").prop("disabled", false);
        orderRow.find(".description-staff").prop("disabled", false);
        orderRow.find(".sub_total-staff").prop("disabled", false);
        orderRow.find(".start_time-staff").prop("disabled", false);
        orderRow.find(".end_time-staff").prop("disabled", false);

        orderRow.find(".edit-order").hide();
        orderRow.find(".save-order").show();
    }

    // Save button click event handler
    function saveOrder(orderId) {
        var orderRow = $("#staff-row-" + orderId);

        // Disable input fields
        orderRow.find(".name-staff").prop("disabled", true);
        orderRow.find(".description-staff").prop("disabled", true);
        orderRow.find(".sub_total-staff").prop("disabled", true);
        orderRow.find(".start_time-staff").prop("disabled", true);
        orderRow.find(".end_time-staff").prop("disabled", true);

        orderRow.find(".save-order").hide();
        orderRow.find(".edit-order").show();

        // Retrieve the updated order data
        var updatedOrderData = {
            "id_staffPIC": <?= $_SESSION['id_user'] ?>,
            "event_name": orderRow.find(".name-staff").val(),
            "event_description": orderRow.find(".description-staff").val(),
            "sub_total": orderRow.find(".sub_total-staff").val(),
            "start_time": orderRow.find(".start_time-staff").val(),
            "end_time": orderRow.find(".end_time-staff").val(),
            "id_event": orderId

        };

        // Send a PUT request to update the order
        $.ajax({
            type: "PUT",
            url: "http://localhost:5540/organizer/event/order/" + orderId,
            data: JSON.stringify(updatedOrderData),
            contentType: "application/json",
            success: function(response) {
                // Handle success response
                alert("Order updated successfully!");
            },
            error: function(xhr, status, error) {
                // Handle error response
                alert("Failed to update order: " + error);
            }
        });
    }
    // Delete button click event handler
    function deleteStaff(eventId) {
        if (confirm("Are you sure you want to delete this order?")) {
            // Retrieve the updated order data
            var updatedOrderData = {
                "id_event": eventId
            }
            $.ajax({
                type: "DELETE",
                url: "http://localhost:5540/organizer/event/order/" + eventId,
                data: JSON.stringify(updatedOrderData),
                contentType: "application/json",
                success: function(response) {
                    // Handle success response
                    alert("Order deleted successfully!");
                    getStaffList(); // Refresh the order list
                },
                error: function(xhr, status, error) {
                    // Handle error response
                    alert("Failed to delete order: " + error);
                }
            });
        }
    }
</script>