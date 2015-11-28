<?php 
//?vk=xxx&k  victime accessed
//?uk=xx  user visite
//condition md5(uk)==vk

error_reporting(E_ERROR);
$g_link = false;

function GetMyConnection()
{
    global $g_link;
    if( $g_link )
        return $g_link;
    $g_link = mysql_connect( 'localhost', 'noeyeuser', 'noeye_n033y3_') or die('Could not connect to server.' );
    mysql_select_db('noeye', $g_link) or die('Could not select database.');
    return $g_link;
}

function CleanUpDB()
{
    global $g_link;
    if( $g_link != false )
        mysql_close($g_link);
    $g_link = false;
}

 function QueryUk($uk){
     $con=GetMyConnection();
     $query = sprintf("SELECT prefixdata, lastaccess FROM dns_query
    WHERE  user_key='%s'",         
         mysql_real_escape_string($uk));
     
     // Perform Query
     $result = mysql_query($query,$con);
     while ($row = mysql_fetch_assoc($result)) {
             echo $row['prefixdata']."<------->";             
             echo $row['lastaccess']."<br/>"; ;        
     }
     
     $query = sprintf("SELECT queried_key, lastaccess FROM url_query
    WHERE  user_key='%s'",
         mysql_real_escape_string($uk));
      
     // Perform Query
     $result = mysql_query($query,$con);
     while ($row = mysql_fetch_assoc($result)) {
         echo $row['queried_key']."<------->";
         echo $row['lastaccess']."<br/>"; ;
     }
      
    
     CleanUpDB();
      
     
 }
 function InsertVk($k,$uk){
     $con=GetMyConnection();
     $query = sprintf("insert into url_query(queried_key,user_key) values('%s','%s')",
          mysql_real_escape_string($k),mysql_real_escape_string($uk)); 
     $result = mysql_query($query,$con);   
     CleanUpDB();
     
 }

if(isset($_GET['uk'])){
     $k=mysql_real_escape_string ($_GET['uk']);
    if(strlen($k)==32){
        QueryUk($k);
    }
    die;
}
if(isset($_GET['vk'])&& isset($_GET['k'])){
    // vk 48e59e6d39edfa5174a493dfc2daac49  -> uk A26AD089D4B88BFEDFD06DF26165AC94 
   
    if ($_GET['vk']=="48e59e6d39edfa5174a493dfc2daac49"){       
        InsertVk($_GET['k'],"A26AD089D4B88BFEDFD06DF26165AC94");
    }
    die;
}

?>