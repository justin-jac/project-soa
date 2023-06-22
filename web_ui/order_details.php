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
    <title>STAFF LIST</title>

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
            <!-- <h1 style="margin: 3%;font-family:Quicksand;">STAFF TABLE MANAGEMENT</h1> -->
        </center>

        <table id="example" class="table table-striped table-bordered" style="width: 100%; color: <?= $dark ?>">

            <thead>
                <tr>
                    <th>Id</th>
                    <th>Email</th>
                    <th>Nama</th>
                    <th>Password (Sementara)</th>
                    <th></th>
                </tr>
            </thead>

            <tbody id="staffList">

            </tbody>

        </table>
        <center style="margin: 25px;">
            <a href="staff_add.php">
                <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>">ADD USER</button>
            </a>
        </center>
    </div>
</body>

</html>

<script>
    function getStaffList() {
        $.ajax({
            type: "GET",
            url: "http://localhost:5540/organizer/event",
            success: function(response) {
                // Handle success response

                var staffs = response;
                var staffList = $("#staffList");
                staffList.empty();

                for (var i = 0; i < staffs.length; i++) {
                    var staff = staffs[i];
                    var staffRow = createStaffRow(staff);
                    staffList.append(staffRow);
                }

            },
            error: function(xhr, status, error) {
                // Handle error response
                console.log("Failed to retrieve staff list: " + error);
            }
        });
    }

    // Call the function to retrieve and display the staff list when the page loads
    $(document).ready(function() {
        getStaffList();
    });

    // Function to dynamically create the staff rows
    function createStaffRow(staff) {
        var staffRow = $("<tr id='staff-row-" + staff.id_event + "'></tr>");
        staffRow.append("<td>" + staff.id_event + "</td>");
        staffRow.append("<td><input type='text' class='email-staff' value='" + staff.event_name + "' disabled></td>");
        staffRow.append("<td><input type='text' class='nama-staff' value='" + staff.event_description + "' disabled></td>");
        staffRow.append("<td><input type='text' class='password-staff' value='" + staff.sub_total + "' disabled></td>");

        // staffRow.append('<td><center><button type="button" class="btn btn-info edit-order" onclick="editOrder(' + staff.id_order + ')">EDIT</button><button type="button" class="btn btn-success save-order" style="display:none" onclick="saveOrder(' + staff.id + ')">SAVE</button><button type="button" class="btn btn-danger" onclick="deleteStaff(' + staff.id + ')">DELETE</button></center></td>');

        // var actionsCell = $("<td></td>");
        // actionsCell.append("<button class='edit-staff' onclick='editOrder(" + staff.idOrder + ")'>Edit</button>");
        // actionsCell.append("<button class='save-staff' onclick='saveOrder(" + staff.idOrder + ")' style='display:none'>Save</button>");
        // actionsCell.append("<button class='delete-staff' onclick='deleteOrder(" + staff.idOrder + ")'>Delete</button>");
        // staffRow.append(actionsCell);

        return staffRow;
    }

    // Edit button click event handler
    function editOrder(orderId) {
        var orderRow = $("#staff-row-" + orderId);

        // Enable input fields for editing
        // orderRow.find(".id-client").prop("disabled", false);
        orderRow.find(".email-staff").prop("disabled", false);
        orderRow.find(".nama-staff").prop("disabled", false);
        orderRow.find(".password-staff").prop("disabled", false);

        orderRow.find(".edit-order").hide();
        orderRow.find(".save-order").show();
    }


    // Save button click event handler
    function saveOrder(orderId) {
        var orderRow = $("#staff-row-" + orderId);

        // Disable input fields
        orderRow.find(".email-staff").prop("disabled", true);
        orderRow.find(".nama-staff").prop("disabled", true);
        orderRow.find(".password-staff").prop("disabled", true);

        orderRow.find(".save-order").hide();
        orderRow.find(".edit-order").show();

        // Retrieve the updated order data
        var updatedOrderData = {
            // idClient: orderRow.find(".id-client").val(),
            // namaOrder: orderRow.find(".nama-order").val(),
            // deskripsiOrder: orderRow.find(".deskripsi-order").val(),
            // tanggalOrder: formatDate(orderRow.find(".tanggal-order").val()),
            // totalHargaOrder: orderRow.find(".total-harga-order").val(),
            // statusOrder: orderRow.find(".status-order").val()
            "email": orderRow.find(".email-staff").val(),
            "nama": orderRow.find(".nama-staff").val(),
            "password": orderRow.find(".password-staff").val()
        };

        // Send a PUT request to update the order
        $.ajax({
            type: "PUT",
            url: "http://localhost:5510/organizer/staf/" + orderId,
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
    function deleteStaff(staffId) {
        if (confirm("Are you sure you want to delete this order?")) {
            $.ajax({
                type: "DELETE",
                url: "http://localhost:5510/organizer/staf/" + staffId,
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