<?php 
    include "dbhandler.php";

    //$data = array("joueur1"=>"pseudo1", "date_heure"=>"2023-01-23 09:12:48");
    
    if(pseudo_existe($data["joueur1"]) == false){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    //requête 
    $stmt = $conn->prepare("SELECT * From invitations WHERE (joueur = ? or invite = ?);");
    $stmt->bind_param("ss", $data["joueur1"], $data["joueur1"]);
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
