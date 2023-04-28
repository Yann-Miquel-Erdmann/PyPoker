<?php 
include "dbhandler.php";

    //$data = array("joueur1"=>"pseudo", "date_heure"=>"2022-01-23 09:12:48");

    //check si le pseudo est dans la base de données
    if(pseudo_existe($data["joueur1"]) == false){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    //requête 
    $stmt = $conn->prepare("SELECT * From chat_global WHERE dateheure > ?;");
    $stmt->bind_param("s",  $data["date_heure"] );
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
