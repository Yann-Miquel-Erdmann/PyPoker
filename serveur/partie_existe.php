<?php
include "dbhandler.php";



$reponse["resultat"][] = ingame($data["joueur1"], true);

$conn->close();
exit(json_encode($reponse, true));


?>



/home/yann_me/.config/filezilla/queue.sqlite3