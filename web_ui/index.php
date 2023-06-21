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
            <h1 style="margin: 3%;font-family:Quicksand;">STAFF TABLE MANAGEMENT</h1>
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

            <tbody id="orderlist">
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
                        <center>
                            <button type="button" class="btn btn-info" style="margin-right:50px; background-color: <?= $p3 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>">EDIT</button>
                        </center>
                    </td>
                </tr>
            </tbody>

        </table>
        <!-- <center style="margin: 25px;">
            <button type="button" class="btn btn-success" style="background-color: <?= $p2 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>">ADD USER</button>
        </center> -->
    </div>
</body>

</html>

<script>
    function getStaffList() {
        $.ajax({
            type: "GET",
            url: "http://localhost:5500/organizer/staf",
            success: function(response) {
                // Handle success response

                var staffs = response;
                var staffList = $("#staffList");
                staffList.empty();

                for (var i = 0; i < staffs.length; i++) {
                    var staff = staffs[i];
                    var orderRow = createStaffRow(staff);
                    staffList.append(orderRow);
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
        var orderRow = $("<tr id='staff-row-" + staff.new_staff_id + "'></tr>");
        orderRow.append("<td>" + staff.new_staff_id + "</td>");
        orderRow.append("<td><input type='text' class='id-client' value='" + staff.new_staff_id + "' disabled></td>");
        orderRow.append("<td><input type='text' class='nama-staff' value='" + staff.staffName + "' disabled></td>");
        orderRow.append("<td><input type='text' class='password-staff' value='" + staff.staffPass + "' disabled></td>");

        // orderRow.append('<center><button type="button" class="btn btn-info" style="margin-right:50px; background-color: <?= $p3 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>">EDIT</button></center>');

        // var actionsCell = $("<td></td>");
        // actionsCell.append("<button class='edit-staff' onclick='editOrder(" + staff.idOrder + ")'>Edit</button>");
        // actionsCell.append("<button class='save-staff' onclick='saveOrder(" + staff.idOrder + ")' style='display:none'>Save</button>");
        // actionsCell.append("<button class='delete-staff' onclick='deleteOrder(" + staff.idOrder + ")'>Delete</button>");
        // orderRow.append(actionsCell);

        return orderRow;
    }
</script>

<!-- <tr>
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
        <center>
            <button type="button" class="btn btn-info" style="margin-right:50px; background-color: <?= $p3 ?>; border-color: <?= $dark ?>; color: <?= $dark ?>">EDIT</button>
        </center>
    </td>
</tr> -->