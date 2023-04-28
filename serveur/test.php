<?php 
    $servername = "http://phpmyadmin.free.fr";
    $username = "lmn.eleve1";
    $password = "lmneleve1";
    $database = "lmn_eleve1";
    $conn = new mysqli($servername, $username, $password,$database, 3306);
    $conn->set_charset("utf8");

    $data = array("joueur1"=>"yann", "skins"=>1110,"gemmes"=>1001);

    //requête 
    $stmt = $conn->prepare("UPDATE joueurs SET Gemmes = ?, skins = ?  WHERE pseudo = ?;");
    $stmt->bind_param("sii",$data["joueur1"], $data["gemmes"], $data["skins"]);
    $stmt->execute(); 

    
?>