<?php 

include "dbhandler.php";

//check si le pseudo est dans la base de données
if(pseudo_existe($data["joueur1"]) == false){
    $reponse["erreur"] = true;
    $reponse["erreurs"][] = "le pseudonyme n'est pas dans la base de données";
    exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
}

// on met à jour les skins et les gemmes du joueur.
$stmt = $conn->prepare("UPDATE joueurs SET Gemmes = ?, skins = ? , skin_selectionne=? WHERE pseudo = ?;");
$stmt->bind_param("iiis",$data["gemmes"], $data["skins"],$data["skin_selectionne"],$data["joueur1"]);
$stmt->execute(); 

$conn->close();
exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
?>
