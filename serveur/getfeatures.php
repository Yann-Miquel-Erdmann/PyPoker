<?php 
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
include "dbhandler.php";

    //$data = array("joueur1"=>"joueur1");

    //check si le pseudo est dans la base de données
    if(pseudo_existe($data["joueur1"]) == false){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    // on récupère les informations du joueur mais pas son mot de passe qui reste dans la base de données
    $stmt = $conn->prepare("SELECT Gemmes, skins, skin_selectionne FROM joueurs WHERE pseudo = ?;");
    $stmt->bind_param("s", $data["joueur1"]);
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
