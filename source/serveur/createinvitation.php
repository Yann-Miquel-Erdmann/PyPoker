<?php

    include "dbhandler.php";

    //$data = array("joueur1"=>"pseudo1", "joueur2"=>"pseudo2");

    // on vérifie que le pseudo existe
    if(pseudo_existe($data["joueur1"]) == false){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }


    // on vérifie que le joueur n'ait pas déjà invité l'autre joueur
    $stmt = $conn->prepare("SELECT if(count(1) >= 1, 1, 0) AS existe FROM  invitations WHERE (joueur LIKE ? or joueur LIKE ?) and (invite LIKE  ? or invite LIKE ?)");
    $stmt->bind_param("ssss", $data['joueur1'], $data['joueur2'],$data['joueur1'], $data['joueur2']);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($result){
        if ($result->fetch_assoc()["existe"] == 1){
            $reponse["erreur"] = true;
            $reponse["erreurs"][] = "une invitation existe deja entre ces deux joueurs";
            exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
        }
    }else{
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "la requête n'a pas donné de reponse";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));

    }
    

    // on crée l'invitation
    $stmt = $conn->prepare("INSERT INTO invitations(joueur, invite) VALUES(?,?);");
    $stmt->bind_param("ss", $data["joueur1"], $data["joueur2"] );
    $stmt->execute();
    $conn->close();
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));

?>
