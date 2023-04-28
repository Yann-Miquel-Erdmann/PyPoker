<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
include "dbhandler.php";

//$data = array("joueur1"=>"joueur1", "partie"=>"joueur1§joueur2", "action"=>"mise", "texte"=>"","mise"=>50);

if(pseudo_existe($data["joueur1"]) == false){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}


if(ingame($data["joueur1"],true) != $data["partie"]){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "cette partie n'existe pas";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}

$stmt = $conn->prepare("INSERT INTO {$data["partie"]} (player, mise, Action_, texte) VALUES(?, ?, ?, ?);");
$stmt->bind_param("siss", $data["joueur1"],$data["mise"], $data["action"],$data["texte"]);
$stmt->execute();

$conn->close();
exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));


?>
