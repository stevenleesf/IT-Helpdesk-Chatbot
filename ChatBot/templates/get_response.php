<?php 
require_once("config.php");
$yourName = $conn->real_escape_string($_POST['your_name']);
$yourEmail = $conn->real_escape_string($_POST['your_email']);
$comments = $conn->real_escape_string($_POST['comments']);
$sql="INSERT INTO contact_form_info (name, email, phone, comments) VALUES ('".$yourName."','".$yourEmail."', '".$comments."')";
