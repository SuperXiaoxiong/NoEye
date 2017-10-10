<?php 
//http 隐藏信道

error_reporting(E_ERROR);
$g_link = false;

function GetMyConnection()
{
    global $g_link;
    if( $g_link )
        return $g_link;
    $g_link = mysql_connect( 'localhost', 'root', 'root') or die('Could not connect to server.' );
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


 function InsertVk($data){
     $con=GetMyConnection();
     $query = sprintf("insert into url_query(queried_key) values('%s')",
          mysql_real_escape_string($data)); 
     $result = mysql_query($query,$con);   
     CleanUpDB();
     
 }


if(isset($_GET["data"])){
    // 参数data所带的就是数据 
   
         
    InsertVk($_GET["data"]);

    die;
}

?>