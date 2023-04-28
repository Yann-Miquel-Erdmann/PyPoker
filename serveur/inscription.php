<?php
    include "dbhandler.php";

    //$data = array("joueur1"=>"pseudo1", "mdp"=>"123456");

    
    if(pseudo_existe($data["joueur1"]) == true){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "il existe deja un compte avec ce pseudonyme";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    // exit($data["mdp"]);
    
    $stmt = $conn->prepare("INSERT INTO joueurs(pseudo, mdp) VALUES(?,?);");
    $stmt->bind_param("ss", $data["joueur1"], $data["mdp"]);
    $stmt->execute();
    $conn->close();
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
?>
