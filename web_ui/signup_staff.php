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

                <h2>Sign Up as Staff</h2>

                <div class="form">

                    <div class="inputBox">

                        <input type="email" required> <i>Email</i>

                    </div>

                    <div class="inputBox">

                        <input type="text" required> <i>Nama</i>

                    </div>

                    <div class="inputBox">

                        <input type="password" required> <i>Password</i>

                    </div>



                    <div class="links">
                        <!-- <a href="#">Forgot Password</a>  -->
                        <a href="signup_client.php">Sign up as a Client?</a>
                    </div>

                    <div class="inputBox">

                        <form action="login.php" method="post">
                            <!-- Your form inputs here -->
                            <input type="submit" value="Sign Up">

                        </form>

                    </div>

                </div>

            </div>

        </div>

    </section> <!-- partial -->

</body>

</html>