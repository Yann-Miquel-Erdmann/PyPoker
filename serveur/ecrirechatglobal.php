<?php 
include "dbhandler.php";


    //$data = array("joueur1"=>"pseudo1", "texte"=>"text");

    //check si le pseudo est dans la base de données
    if(pseudo_existe($data["joueur1"]) == false){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    

    $stmt = $conn->prepare("INSERT INTO chat_global (joueur, texte) VALUES(?, ?);");
    $stmt->bind_param("ss", $data["joueur1"], $data["texte"]);
    $stmt->execute();
    
    $conn->close();
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));

?>
