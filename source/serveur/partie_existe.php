<?php
include "dbhandler.php";


// on regarde si le joueur est dans une partie et si oui on renvoie le nom de cette partie
$reponse["resultat"][] = ingame($data["joueur1"], true);

$conn->close();
exit(json_encode($reponse, true));


?>



/home/yann_me/.config/filezilla/queue.sqlite3