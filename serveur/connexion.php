<?php 
include "dbhandler.php";
    

// $data = array("joueur1"=>"pseudo", "mdp"=>"12345");

// on vérifie que le pseudo existe
if(pseudo_existe($data["joueur1"]) == false){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}


// si le pseudo existe on regarde si le hash du mot de passe correspond
$stmt = $conn->prepare("SELECT if (mdp = ?,1,0) as bon FROM joueurs WHERE pseudo = ?;");
$stmt->bind_param("ss", $data["mdp"], $data["joueur1"] );
$stmt->execute();
$result = $stmt->get_result();
if ($result){
    if($result->fetch_assoc()["bon"] != 1){ // les hashs sont différents le mot de passse n'est pas bon
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudo ou le mot de passe est incorrect";
    }
}else{ // les hashs sont les mêmes le mot de passse est bon
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "la requête n'a pas donné de reponse";
}


$conn->close();
exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));