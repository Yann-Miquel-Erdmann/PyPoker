<?php 
include "dbhandler.php";


if ($data["action"] == "accept"){
    if (pseudo_existe($data["joueur1"]) == false or pseudo_existe($data["joueur2"]) == false) {
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "un des pseudonymes n'est pas dans la base de données";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }
    
    
    // verifie si il existe déjà une partie entre ces deux joueurs
    ingame($data["joueur1"]);
    ingame($data["joueur2"]);
    
    // crée la base de données 
    $conn->query(
        "CREATE TABLE IF NOT EXISTS `{$data["joueur1"]}§{$data["joueur2"]}` (
            `Id` int(11) NOT NULL auto_increment,
            `player` varchar(20) collate utf8_general_ci,
            `mise` int(11) default NULL,
            `Action_` varchar(10) collate utf8_general_ci NOT NULL,
            `texte` varchar(255) collate utf8_general_ci default NULL,
            `dateheure` timestamp NOT NULL default CURRENT_TIMESTAMP,
            PRIMARY KEY  (`Id`),
            KEY `{$data["joueur1"]}§{$data["joueur2"]}` (`player`)
          ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci AUTO_INCREMENT=1;"
    );

    $stmt = $conn->prepare("INSERT INTO `{$data["joueur1"]}§{$data["joueur2"]}`(Action_, mise) VALUES ('random',?);");
    $stmt->bind_param("i",rand(0,getrandmax()));
    $stmt->execute();

    $name = "{$data["joueur1"]}§{$data["joueur2"]}";

    $stmt = $conn->prepare("INSERT INTO `lmn_eleve1`.`parties` (`name_partie`) VALUES (? );");
    $stmt->bind_param("s", $name);
    $stmt->execute();


}

// on supprime l'invitation
$stmt = $conn->prepare("DELETE FROM invitations WHERE joueur=? AND invite=?;");
$stmt->bind_param("ss", $data["joueur2"], $data["joueur1"] );
$stmt->execute();
$result = $stmt->get_result();



$conn->close();
exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));


