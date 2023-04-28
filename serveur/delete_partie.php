<?php 
include "dbhandler.php";

// on vérifie que le joueur soit dans une partie
$partie =ingame($data["joueur1"], true);

// on supprime la partie dans laquelle est le joueur
$stmt =$conn->prepare("DELETE from parties where `name_partie` = ?");
$stmt->bind_param("s", $partie);
$stmt->execute();

$stmt =$conn->query("DROP TABLE IF EXISTS {$partie}");


exit(json_encode($reponse, true));