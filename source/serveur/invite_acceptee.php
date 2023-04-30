<?php 
    include "dbhandler.php";

    //$data = array("joueur1"=>"joueur4");
    
    if (pseudo_existe($data["joueur1"])){
        //si l'inviatation a été acceptée il existe une partie avec le nom du joueur
        $reponse["resultat"][] = ingame($data["joueur1"],true);
    }else{
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
    }
    $conn->close();
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    
    
