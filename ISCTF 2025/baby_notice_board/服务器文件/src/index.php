<?php
include('connection.php');
session_start();
 ?>
<html>
	<head>
		<title>Online Notice Board</title>
		<link rel="stylesheet" href="css/bootstrap.css"/>
		<script src="js/jquery_library.js"></script>
<script src="js/bootstrap.min.js"></script>
	</head>
	<body>
			<nav class="navbar navbar-default navbar-fixed-top" style="background:#000">
  <div class="container">

  <ul class="nav navbar-nav navbar-left">
    <li><a href="index.php"><strong>Online Notice Board</strong></a></li>


	  <li><a href="index.php?option=about"><span class="glyphicon glyphicon-user"></span> About</a></li>



	<li><a href="index.php?option=contact"><span class="glyphicon glyphicon-phone"></span>Contact</a></li>

	</ul>


<ul class="nav navbar-nav navbar-right">
      <li><a href="index.php?option=New_user"><span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
      <li><a href="index.php?option=login"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
    </ul>



</div>
</nav>

<div class="container-fluid">
	<!-- slider -->
<div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-example-generic" data-slide-to="1"></li>
    <li data-target="#carousel-example-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner" role="listbox">
    <div class="item active">
      <img src="images/sitePHP.jpg" alt="...">
      <div class="carousel-caption">
        ...
      </div>
    </div>
    <div class="item">
      <img src="images/notice.jpg" alt="...">
      <div class="carousel-caption">
        ...
      </div>
    </div>

	 <div class="item">
      <img src="images/notice2.jpg" alt="...">
      <div class="carousel-caption">
        ...
      </div>
    </div>
    ...
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
    <span class="sr-only">Previous</span>
  </a>
  <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
    <span class="sr-only">Next</span>
  </a>
</div>
<!-- slider end-->
</div>


<div class="container">
	<div class="row">
	<!-- container -->
		<div class="col-sm-8">
		<?php
		@$opt=$_GET['option'];

		if($opt!="")
		{
			if($opt=="about")
			{
			include('about.php');
			}
			else if($opt=="contact")
			{
			include('contact.php');
			}

			else if($opt=="New_user")
			{
			include('registration.php');
			}


			else if($opt=="login")
			{
			include('login.php');
			}
		}
		else
		{
		echo "<h2><b>'WELCOME USER TO OUR ONLINE NOTICE BOARD'</b></h2>
		<i> <b> Join us today and get connected. Register now to get each and every updates of your college! </b></i>";
		}
		?>



		</div>
	<!-- container -->

		<div class="col-sm-4">
			<div class="panel panel-default">
  <div class="panel-heading"><b>LATEST NEWS</b></div>
  <div class="panel-body">
    ... College now uses Google Apps for Education for fast and easy collaboration. The products that we use includes Gmail, Calendar, Docs and more.With Google Apps for Education, everything is automatically saved in the cloud – 100% powered by the web. This means that emails, documents, calendar and sites can be accessed – and edited – on almost any mobile device or tablet. Anytime, anywhere.
  </div>
</div>

		</div>
	</div>

</div>



<br/>
<br/>
<br/>
<br/>

<!-- footer-->

			<nav class="navbar navbar-default navbar-bottom" style="background:black">
  <div class="container">

  <ul class="nav navbar-nav navbar-left">
    <li><a href="https://code-projects.org/"> Brought To You By Code-Projects</a></li>

	</ul>




</div>
</nav>
<!-- footer-->

	</body>
</html>
