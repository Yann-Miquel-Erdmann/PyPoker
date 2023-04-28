<?php 
include "dbhandler.php";

$partie =ingame($data["joueur1"], true);

$stmt =$conn->prepare("DELETE from parties where `name_partie` = ?");
$stmt->bind_param("s", $partie);
$stmt->execute();

$stmt =$conn->query("DROP TABLE IF EXISTS {$partie}");


exit(json_encode($reponse, true));