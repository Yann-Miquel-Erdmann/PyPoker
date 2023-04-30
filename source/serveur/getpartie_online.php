<?php
include "dbhandler.php";

//$data = array("joueur1"=>"joueur1","partie"=>"joueur1§joueur2", "date_heure"=>"2022-01-23 09:12:48");

//check si le pseudo est dans la base de données
if(pseudo_existe($data["joueur1"]) == false){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}

// si la partie dans laquelle est le joueur est différente de la partie donnée
if(ingame($data["joueur1"],true) != $data["partie"]){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "cette partie n'existe pas";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}


// on récupère les nouevelles actions dans la partie
$stmt = $conn->prepare("SELECT player, Action_, mise, texte, dateheure  FROM {$data["partie"]} WHERE dateheure > ? ;");
$stmt->bind_param("s", $data["date_heure"] );
$stmt->execute();
$result = $stmt->get_result();  
if ($result){
    while($row = $result->fetch_assoc()) {
        $reponse["resultat"][] = $row;
    }
}else{
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "la requête n'a pas donné de reponse";
}

$conn->close();
exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));


?>
