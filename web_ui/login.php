<!doctype html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <link rel="stylesheet" href="css/login.css">
    <link rel="stylesheet" href="css/background2.css">

</head>

<body> <!-- partial:index.partial.html -->

    <section>

        <div class="signin">

            <div class="content">

                <h2>Log In</h2>

                <div class="form">

                    <div class="inputBox">

                        <input type="text" required> <i>Username</i>

                    </div>

                    <div class="inputBox">

                        <input type="password" required> <i>Password</i>

                    </div>

                    <div class="links">
                        <a href="signup_staff.php">Signup as Staff</a>
                        <a href="signup_client.php">Signup as Client</a>
                    </div>

                    <div class="inputBox">

                        <form action="index.php" method="post">
                            <!-- Your form inputs here -->
                            <input type="submit" value="Login">

                        </form>

                    </div>

                </div>

            </div>

        </div>

    </section> <!-- partial -->

</body>

</html>