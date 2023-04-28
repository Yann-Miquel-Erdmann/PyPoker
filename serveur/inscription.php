<?php
    include "dbhandler.php";

    //$data = array("joueur1"=>"pseudo1", "mdp"=>"123456");

    // on vérifie que le joueur n'existe pas déjà dans la base de données
    if(pseudo_existe($data["joueur1"]) == true){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "il existe deja un compte avec ce pseudonyme";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

  
    //on ajoute le joueur à la base de données avec sont mot de passe encrypté
    $stmt = $conn->prepare("INSERT INTO joueurs(pseudo, mdp) VALUES(?,?);");
    $stmt->bind_param("ss", $data["joueur1"], $data["mdp"]);
    $stmt->execute();
    $conn->close();
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
?>
