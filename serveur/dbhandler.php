<?php 
mysqli_report(MYSQLI_REPORT_OFF);
    // exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    $reponse = array("erreur"=>false, "erreurs"=>[], "resultat"=>[]);

    
    $json = file_get_contents('php://input');
    $data = json_decode($json,true);
    if(empty($data)){
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "il n'y a pas de données dans le json";
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }


    $servername = "CONFIDENTIEL";
    $username = "CONFIDENTIEL";
    $password = "CONFIDENTIEL";
    $database = "CONFIDENTIEL";
    $conn = new mysqli($servername, $username, $password,$database, 3306);
    $conn->set_charset("utf8");
    
    if ($conn->connect_error) {
        $reponse["erreur"] = true;
        $reponse["erreurs"][] = "erreur de connection à la base de données: " . $conn->connect_error;
        exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
    }

    //check si le pseudo est dans la base de données
    function pseudo_existe($pseudo){
        global $conn;
        $stmt = $conn->prepare("SELECT COUNT(1) as nombre FROM joueurs WHERE Pseudo = ?");
        $stmt->bind_param("s", $pseudo );
        $stmt->execute();
        $result = $stmt->get_result();
        if ($result->fetch_assoc()["nombre"] == 1){
            return true;
        }else{
            return false;
        }
    }
    
    function ingame($pseudo, $getgame = false){
        global $reponse,$conn;

        $param1 = "{$pseudo}§%";
        $param2 = "%§{$pseudo}";
        $stmt = $conn->prepare("SELECT `name_partie` FROM `parties` WHERE (name_partie LIKE ? or name_partie LIKE ?)
        ");
        $stmt->bind_param("ss", $param1, $param2);
        $stmt->execute();
        $result = $stmt->get_result();
        if ($getgame){
            if (mysqli_num_rows($result) >0) {
                $game = $result->fetch_assoc()["name_partie"];
                return $game;
                
            };
            return "";
            
        }else{
            if (mysqli_num_rows($result) >0) {
                $reponse["erreur"] = true;
                $reponse["erreurs"][] = "le joueur {$pseudo} est déjà en partie attendez qu'il finisse";
                exit(json_encode($reponse,JSON_UNESCAPED_UNICODE));
            }
        }
            
    }
?>